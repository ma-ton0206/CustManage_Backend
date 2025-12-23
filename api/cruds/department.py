# sessionはSQLを実行したり、データベースとの通信を行うための一時的な接続
from sqlalchemy.orm import Session
from api.models.department import Department as DepartmentModel
from fastapi import HTTPException
from sqlalchemy import select
from api.schemas.department import PutDepartmentIn, PostDepartmentIn, UpdateDepartmentNameIn
from api.models.users import Users
from typing import List
# GET


def get_departments(db: Session, client_id: int, current_user: Users):
    try:
        query = (select(DepartmentModel).filter(
            DepartmentModel.client_id == client_id).filter(
            DepartmentModel.company_id == current_user.company_id))
        result = db.execute(query)
        departments = result.scalars().all()
        tree_data = build_tree(departments, parent_id=0)
        return tree_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def build_tree(departments: List[DepartmentModel], parent_id: int = 0):
    tree = []
    for dept in departments:
        # 親部署IDが0の場合はルートノード
        if dept.parent_department_id == parent_id:
            # 子部署を再帰的に取得してchildrenに追加
            children = build_tree(departments, dept.department_id)
            # ノードを作成
            node = {
                "department_id": dept.department_id,
                "parent_department_id": dept.parent_department_id,
                "department_name": dept.department_name,
                "children": children
            }
            print("node: ", node)
            tree.append(node)
    return tree

# PUT


def update_department(db: Session, client_id: int, departments_in: PutDepartmentIn, current_user: Users):
    try:
        # # 現在のDB上の部署一覧を取得
        # existing_departments = db.query(DepartmentModel).filter(
        #     DepartmentModel.client_id == client_id).all()
        # existing_ids = {d.department_id for d in existing_departments}

        # # フロントから送られたidを収集
        # incoming_ids = {
        #     d.department_id for d in departments_in if d.department_id}

        # # --- 削除すべきidを特定 ---
        # ids_to_delete = existing_ids - incoming_ids
        # if ids_to_delete:
        #     db.query(DepartmentModel).filter(DepartmentModel.department_id.in_(ids_to_delete)).delete()

        # 部署IDが存在しない場合は新規作成(insert)
        if not departments_in.department_id:
            department = DepartmentModel(
                client_id=client_id,
                company_id=current_user.company_id,
                department_name=departments_in.department_name,
                parent_department_id=departments_in.parent_department_id,
                created_by_user_id=current_user.user_id
            )
            db.add(department)
            db.commit()
            db.refresh(department)
            return department

        # 部署IDが存在する場合は更新(update)
        else:
            query = (select(DepartmentModel).filter(
                DepartmentModel.client_id == client_id).filter(
                    DepartmentModel.company_id == current_user.company_id))
            result = db.execute(query)
            department = result.scalar_one_or_none()
            if not department:
                db.rollback()
                raise HTTPException(
                    status_code=404, detail="department not found")

            department.department_name = departments_in.department_name
            department.parent_department_id = departments_in.parent_department_id

            db.commit()
            db.refresh(department)
        return department
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# delete
def delete_departments(db: Session, client_id: int, department_id: int, current_user: Users):
    try:
        query = (select(DepartmentModel).filter(
            DepartmentModel.client_id == client_id).filter(
            DepartmentModel.department_id == department_id).filter(
            DepartmentModel.company_id == current_user.company_id)
        )
        result = db.execute(query)
        department = result.scalar_one_or_none()
        if not department:
            db.rollback()
            raise HTTPException(status_code=404, detail="department not found")
        db.delete(department)
        db.commit()
        return department
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# POST
def create_departments(db: Session, client_id: int, departments_in: PostDepartmentIn, current_user: Users):
    try:
        department = DepartmentModel(
            client_id=client_id,
            department_name=departments_in.department_name,
            parent_department_id=departments_in.parent_department_id,
            created_by_user_id=current_user.user_id,
            company_id=current_user.company_id,
        )
        db.add(department)
        db.commit()
        db.refresh(department)
        return department
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# PATCH
def update_department_name(db: Session, client_id: int, department_id: int, department_name_in: UpdateDepartmentNameIn, current_user: Users):
    try:
        query = (select(DepartmentModel).filter(
            DepartmentModel.client_id == client_id).filter(
            DepartmentModel.department_id == department_id).filter(
            DepartmentModel.company_id == current_user.company_id)
        )
        result = db.execute(query)
        department = result.scalar_one_or_none()
        if not department:
            db.rollback()
            raise HTTPException(status_code=404, detail="department not found")
        department.department_name = department_name_in.department_name
        db.commit()
        db.refresh(department)
        return department
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
