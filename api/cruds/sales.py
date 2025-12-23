# sessionはSQLを実行したり、データベースとの通信を行うための一時的な接続
from tokenize import group
from sqlalchemy.orm import Session
from api.models.sales import Sales as SalesModel
from api.schemas.sales import PostSalesIn, PutSalesIn, GetSalesOut, GetSalesDetailOut, GetPurchaseDetailsOut, GetYearSalesOut, GetSalesTrendMonth, GetSalesTrendOut, GetTopSalesOut
from fastapi import HTTPException
from sqlalchemy import select, extract
from datetime import date
from api.models.users import Users
from api.models.purchase_details import PurchaseDetails as PurchaseDetailsModel
from datetime import datetime
from sqlalchemy import func
from api.models.client import Client as ClientModel
from sqlalchemy.orm import joinedload
from api.constants.status import SalesStatus
from collections import defaultdict


def create_sales(db: Session, sales_in: PostSalesIn, current_user: Users):

    # ① client_id がログイン中の会社に属しているか確認
    client = db.query(ClientModel).filter(
        ClientModel.client_id == sales_in.client_id,
        ClientModel.company_id == current_user.company_id
    ).first()

    if not client:
        raise HTTPException(
            status_code=403,
            detail="このclient_idはあなたの会社に属していません。"
        )

    # ---- 年ごとの採番処理 ----
    year = datetime.now().strftime("%y")  # 例: 2025年 → "25"

    # 同年の最大sales_numberを取得
    prefix = f"J{year}"
    max_num_query = select(func.max(SalesModel.sales_number)).where(
        SalesModel.sales_number.like(f"{prefix}%"))
    max_sales_number = db.scalar(max_num_query)

    if max_sales_number:
        # 既存の最大番号をインクリメント
        last_seq = int(max_sales_number[-6:])  # 末尾6桁を取り出して数値化
        new_seq = last_seq + 1
    else:
        # 当年初の登録
        new_seq = 1

    # 新しいsales_numberを生成
    new_sales_number = f"{prefix}{new_seq:06d}"  # 6桁ゼロ埋め
    print("🟢 新しい販売番号:", new_sales_number)

    # 仕入金額を計算
    total_supply_price = sum(
        d.supply_price * d.qty for d in sales_in.purchase_details
    )

    # 粗利を計算
    gross_profit = sales_in.sales_price - total_supply_price

    # 粗利率を計算
    gross_profit_rate = (
        gross_profit / sales_in.sales_price
        if sales_in.sales_price > 0 else 0
    )

    # dumpは「型付きのもの」→「辞書」などに変換する動き。
    # 例user = User(name="たろう", age=30) → user.model_dump() → {"name":"たろう", "age":30}
    sales = SalesModel(
        sales_number=new_sales_number,
        gross_profit=gross_profit,
        total_supply_price=total_supply_price,
        gross_profit_rate=gross_profit_rate,
        created_by_user_id=current_user.user_id,
        updated_by_user_id=current_user.user_id,
        company_id=current_user.company_id,
        **sales_in.model_dump(exclude={"purchase_details"})  # ← ネスト部分は別で処理
    )
    print("🟢 sales", sales)
    try:

        print("🟢 sales2")
        db.add(sales)
        print("🟢 sales3")
        db.flush()
        print("🟢 sales4", sales.sales_id)
        # 作成したsalesインスタンスをセッションに追加（まだDBには反映されていない）
    # 子テーブル登録
        for d in sales_in.purchase_details:
            pd = PurchaseDetailsModel(
                sales_id=sales.sales_id,
                supplier_name=d.supplier_name,
                product_name=d.product_name,
                supply_price=d.supply_price,
                qty=d.qty,
                due_date=d.due_date,
                company_id=current_user.company_id,
                created_by_user_id=current_user.user_id,
                updated_by_user_id=current_user.user_id,
            )
            db.add(pd)
        db.commit()  # セッションをコミットしてDBに永続化
        db.refresh(sales)  # コミットによって生成されたIDなどを含め、最新の状態でインスタンスを再取得
        return sales  # 作成されたsales（DBに保存済み）を返却
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_sales(db: Session, current_user: Users):
    try:
        query = (
            select(SalesModel).
            options(joinedload(SalesModel.client)).
            filter(SalesModel.company_id == current_user.company_id))

        query = query.order_by(SalesModel.sales_id.desc())
        result = db.execute(query)
        sales = result.scalars().all()

        sales_out = []
        for sale in sales:
            sales_out.append(
                GetSalesOut(
                    sales_id=sale.sales_id,
                    sales_number=sale.sales_number,
                    sales_name=sale.sales_name,
                    client_name=sale.client.client_name,
                    order_date=sale.order_date,
                    sales_price=sale.sales_price,
                    status=sale.status
                )
            )
        return sales_out
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_sales_detail(db: Session, sales_id: int, current_user: Users):
    try:
        query = (
            select(SalesModel).
            join(ClientModel).
            filter(SalesModel.sales_id == sales_id).
            filter(SalesModel.company_id == current_user.company_id).
            options(joinedload(SalesModel.purchase_details))
        )
        result = db.execute(query).unique()
        sales = result.scalar_one_or_none()
        if not sales:
            db.rollback()
            raise HTTPException(status_code=404, detail="task not found")

        # 仕入明細を取得
        purchase_details_out = []
        for purchase_detail in sales.purchase_details:
            purchase_details_out.append(
                GetPurchaseDetailsOut(
                    purchase_id=purchase_detail.purchase_id,
                    supplier_name=purchase_detail.supplier_name,
                    product_name=purchase_detail.product_name,
                    qty=purchase_detail.qty,
                    supply_price=purchase_detail.supply_price,
                    due_date=purchase_detail.due_date
                )
            )

        # 仕入明細を代入
        sales_out = GetSalesDetailOut(
            sales_id=sales.sales_id,
            sales_name=sales.sales_name,
            sales_price=sales.sales_price,
            client_name=sales.client.client_name,
            order_date=sales.order_date,
            sales_date=sales.sales_date,
            status=sales.status,
            sales_note=sales.sales_note,
            purchase_details=purchase_details_out
        )

        return sales_out
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

#期間内の売上金額を取得
def get_sales_trend(db: Session, start_date: date, end_date: date, current_user: Users, client_id: int):

    # ① client_id がログイン中の会社に属しているか確認
    client = db.query(ClientModel).filter(
        ClientModel.client_id == client_id,
        ClientModel.company_id == current_user.company_id
    ).first()

    if not client:
        raise HTTPException(
            status_code=403,
            detail="このclient_idはあなたの会社に属していません。"
        )
    try:
        query = (
            # どの列を集計するか明示
            select(
                # labelはこれは「クエリ結果でこの列をどんな名前で呼ぶか」を指定するもの
                extract('year', SalesModel.sales_date).label('year'),
                extract('month', SalesModel.sales_date).label('month'),
                func.sum(SalesModel.sales_price).label('month_sales_price')
            ).
            # 会社IDでフィルタ
            filter(SalesModel.company_id == current_user.company_id).
            # クライアントIDでフィルタ
            filter(SalesModel.client_id == client_id).
            # orderdateがstart_dateとend_dateの間のものを取得
            filter(SalesModel.sales_date >= start_date).
            filter(SalesModel.sales_date <= end_date).
            # ステータスが売上済みのものを取得
            filter(SalesModel.status == SalesStatus.SOLD).
            # 年と月をグループ化
            # extractでorder_dateからyearを取り出してlabelをyearにする、extractでorder_dateからmonthを取り出してlabelをmonthにする
            group_by(
                extract('year', SalesModel.sales_date),
                extract('month', SalesModel.sales_date)
            ).
            # 年と月で並び替え
            order_by(
                extract('year', SalesModel.sales_date),
                extract('month', SalesModel.sales_date)
            )
        )
        result = db.execute(query).all()

        # step1: SQL結果を year → month → sales に変換
        raw = defaultdict(dict)

        for row in result:
            year = int(row.year)
            month = int(row.month)
            raw[year][month] = int(row.month_sales_price or 0)

        # step2: 空の月も埋める
        output = []

        start_year = start_date.year
        end_year = end_date.year

        for year in range(start_year, end_year + 1):
            # 年の開始月・終了月を決める
            month_start = 1
            month_end = 12

            if year == start_year:
                month_start = start_date.month
            if year == end_year:
                month_end = end_date.month

            months_data = []

            for month in range(month_start, month_end + 1):
                total = raw[year].get(month, 0)
                months_data.append(
                    GetSalesTrendMonth(month=month, total_sales_price=total)
                )

            output.append(GetSalesTrendOut(year=year, data=months_data))

        return output

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# 1年間の売上金額を取得
def get_year_sales(db: Session, year: int, current_user: Users):

    try:
        query = (
            select(
                func.sum(SalesModel.sales_price).label("total_sales_price"),
                extract('month', SalesModel.sales_date).label("month"),
            )
            .filter(SalesModel.company_id == current_user.company_id)
            .filter(extract('year', SalesModel.sales_date) == year)
            .filter(SalesModel.status == SalesStatus.SOLD)
            .group_by(extract('month', SalesModel.sales_date))
            .order_by(extract('month', SalesModel.sales_date).asc())
        )

        rows = db.execute(query).all()

        # ① rows を dict に変換する → {1: 1000, 12: 3000} のように
        month_price_map = {
            int(row.month): int(row.total_sales_price or 0)
            for row in rows
        }

        # ② 1〜12 を必ず作成する
        result = []
        for m in range(1, 13):
            result.append(
                GetYearSalesOut(
                    month=m,
                    total_sales_price=month_price_map.get(m, 0)
                )
            )

        return result

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def update_sales(db: Session, sales_id: int, sales_in: PutSalesIn, current_user: Users):

    # --- ② 売上・粗利計算 ---
    total_supply_price = sum(
        d.supply_price * d.qty for d in sales_in.purchase_details)
    gross_profit = sales_in.sales_price - total_supply_price
    gross_profit_rate = gross_profit / \
        sales_in.sales_price if sales_in.sales_price > 0 else 0

    # --- ③ sales本体を更新 ---
    sales = db.scalar(select(SalesModel).filter(
        SalesModel.sales_id == sales_id))
    if not sales:
        raise HTTPException(status_code=404, detail="sales not found")

    sales.sales_name = sales_in.sales_name
    sales.sales_price = sales_in.sales_price
    sales.order_date = sales_in.order_date
    sales.sales_date = sales_in.sales_date
    sales.status = sales_in.status
    sales.sales_note = sales_in.sales_note
    sales.gross_profit = gross_profit
    sales.total_supply_price = total_supply_price
    sales.gross_profit_rate = gross_profit_rate
    sales.updated_by_user_id = current_user.user_id

    # --- ④ 差分更新（仕入明細） ---

    # データベース内の仕入明細を取得
    existing_details = db.query(PurchaseDetailsModel).filter(
        PurchaseDetailsModel.sales_id == sales_id
    ).all()

    # 既存の仕入明細を辞書に変換
    # existing_dict = {
    #     1: d1,
    #     2: d2
    # }
    existing_dict = {
        # d1 = {purchase_id=1, product_name="A", qty=10}のような型にする
        d.purchase_id: d for d in existing_details
        if d.purchase_id is not None
    }
    # existing_ids = {1, 2}
    existing_ids = set(existing_dict.keys())
    print("🟢 existing_ids", existing_ids)

    # リクエスト側の仕入明細を取得
    # request_ids = {1, 2}
    request_ids = {
        d.purchase_id for d in sales_in.purchase_details
        if d.purchase_id is not None
    }
    print("🟢 request_ids", request_ids)

    # ④-1 削除：リクエストに含まれない既存IDをDBから削除
    delete_ids = existing_ids - request_ids
    print("🟢 delete_ids", delete_ids)

    # 差分が存在する場合は削除
    if delete_ids:
        db.query(PurchaseDetailsModel).filter(
            PurchaseDetailsModel.purchase_id.in_(delete_ids),
            PurchaseDetailsModel.company_id == current_user.company_id
        ).delete(synchronize_session=False)

    # ④-2 追加・更新：リクエスト側をループ
    for d in sales_in.purchase_details:
        # リクエストに含まれるIDが既存IDに存在する場合は更新
        if d.purchase_id and d.purchase_id in existing_dict:
            # --- 更新処理 ---
            pd = existing_dict[d.purchase_id]
            pd.supplier_name = d.supplier_name
            pd.product_name = d.product_name
            pd.supply_price = d.supply_price
            pd.qty = d.qty
            pd.due_date = d.due_date
            pd.updated_by_user_id = current_user.user_id

        else:
            # --- 新規作成 ---
            pd = PurchaseDetailsModel(
                sales_id=sales.sales_id,
                supplier_name=d.supplier_name,
                product_name=d.product_name,
                supply_price=d.supply_price,
                qty=d.qty,
                due_date=d.due_date,
                created_by_user_id=current_user.user_id,
                updated_by_user_id=current_user.user_id,
                company_id=current_user.company_id,
            )
            db.add(pd)

    db.commit()
    db.refresh(sales)
    return sales


def delete_sales(db: Session, sales_id: int, current_user: Users):
    try:
        query = (
            select(SalesModel).
            filter(SalesModel.sales_id == sales_id).
            filter(SalesModel.company_id == current_user.company_id))
        result = db.execute(query)
        sales = result.scalar_one_or_none()
        if not sales:
            db.rollback()
            raise HTTPException(status_code=404, detail="task not found")

        db.delete(sales)
        db.commit()
        return sales
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_top_sales(db: Session, current_user: Users, year: int):

    try:
        query = (
            select(
                ClientModel.client_name.label("client_name"),
                func.sum(SalesModel.sales_price).label("total_sales_price"),
            )
            .join(ClientModel, SalesModel.client_id == ClientModel.client_id)
            .filter(SalesModel.company_id == current_user.company_id)
            .filter(extract('year', SalesModel.sales_date) == year)
            .filter(SalesModel.status == SalesStatus.SOLD)
            .group_by(ClientModel.client_name)
            .order_by(func.sum(SalesModel.sales_price).desc())
            .limit(3)
        )

        rows = db.execute(query).all()

        # rows 例：
        # [("AAA工業", 12345678), ("BBB商事", 9876543), ...]

        result = [
            GetTopSalesOut(
                client_name=row.client_name,
                total_sales_price=int(row.total_sales_price or 0),
            )
            for row in rows
        ]

        return result

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
