# sessionはSQLを実行したり、データベースとの通信を行うための一時的な接続
from sqlalchemy.orm import Session
from api.models.client import Client as ClientModel
from api.schemas.client import PostClientIn, PutClientIn, GetClientOut
from fastapi import HTTPException
from sqlalchemy import select
from api.models.users import Users
from api.models.department import Department as DepartmentModel


def create_client(db: Session, client_in: PostClientIn, current_user: Users):
    # dumpは「型付きのもの」→「辞書」などに変換する動き。
    # 例user = User(name="たろう", age=30) → user.model_dump() → {"name":"たろう", "age":30}
    client = ClientModel(
        user_id=current_user.user_id,
        company_id=current_user.company_id,
        created_by_user_id=current_user.user_id,
        updated_by_user_id=current_user.user_id,
        **client_in.model_dump(),
    )
    # 作成したtaskインスタンスをセッションに追加（まだDBには反映されていない）
    try:
        db.add(client)
        db.flush()

        # ② 最上位部署を自動作成
        top_department = DepartmentModel(
            department_name=client_in.client_name,  # クライアント名を部署名にする
            client_id=client.client_id,             # 紐付け
            company_id=current_user.company_id,
            parent_department_id=0,                 # 一番上
            created_by_user_id=current_user.user_id,
            updated_by_user_id=current_user.user_id,
        )

        db.add(top_department)

        db.commit()  # セッションをコミットしてDBに永続化
        db.refresh(client)  # コミットによって生成されたIDなどを含め、最新の状態でインスタンスを再取得

        return client  # 作成されたclient（DBに保存済み）を返却
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_clients(db: Session, current_user: Users):
    try:
        query = (select(ClientModel).filter(
            ClientModel.company_id == current_user.company_id,
            ClientModel.user_id == current_user.user_id
        ))
        query = query.order_by(ClientModel.client_id.asc())

        result = db.execute(query)
        clients = result.scalars().all()
        return clients
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_client_detail(db: Session, client_id: int, current_user: Users):
    try:
        query = (select(ClientModel).filter(
            ClientModel.client_id == client_id).filter(
            ClientModel.company_id == current_user.company_id))
        result = db.execute(query)
        client = result.scalar_one_or_none()
        if not client:
            db.rollback()
            raise HTTPException(status_code=404, detail="client not found")
        return client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def update_client(db: Session, client_id: int, client_in: PutClientIn, current_user: Users):
    query = (select(ClientModel).filter(
        ClientModel.client_id == client_id).filter(
        ClientModel.company_id == current_user.company_id))
    result = db.execute(query)
    client = result.scalar_one_or_none()  # i件だけ or noneを出す。2以上はエラーになる。
    if not client:
        db.rollback()
        raise HTTPException(status_code=404, detail="client not found")
    # db内のtaskを引数のtask_inに更新し、taskをreturnすることでdbの最新情報を取得する。
    client.client_name = client_in.client_name
    client.industry = client_in.industry
    client.client_phone = client_in.client_phone
    client.client_address = client_in.client_address
    client.updated_by_user_id = current_user.user_id
    try:
        db.commit()
        db.refresh(client)
        return client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def delete_client(db: Session, client_id: int, current_user: Users):
    query = (select(ClientModel).filter(
        ClientModel.client_id == client_id).filter(
        ClientModel.company_id == current_user.company_id))
    result = db.execute(query)
    client = result.scalar_one_or_none()
    if not client:
        db.rollback()
        raise HTTPException(status_code=404, detail="client not found")
    try:
        db.delete(client)
        db.commit()
        return client
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
