# sessionはSQLを実行したり、データベースとの通信を行うための一時的な接続
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select
from api.schemas.contact import PutContactIn, DeleteContactIn, PostContactIn
from api.models.contact import Contact as ContactModel
from api.models.department import Department as DepartmentModel
from api.models.users import Users


def get_contacts(db: Session, client_id: int, department_id: int, current_user: Users):
    try:
        query = (select(ContactModel).join(DepartmentModel).filter(
            DepartmentModel.client_id == client_id
        ).filter(
            ContactModel.department_id == department_id
        ).filter(
            ContactModel.company_id == current_user.company_id))
        result = db.execute(query)
        contacts = result.scalars().all()
        return contacts
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def update_contact(db: Session, client_id: int, department_id: int, contacts_in: PutContactIn, current_user: Users):

    # 担当者IDが存在しない場合は新規作成(insert)
    if not contacts_in.contact_id:
        try:
            contact = ContactModel(
                department_id=department_id,
                contact_name=contacts_in.contact_name,
                role=contacts_in.role,
                contact_email=contacts_in.contact_email,
                contact_phone=contacts_in.contact_phone,
                created_by_user_id=current_user.user_id
            )
            db.add(contact)
            db.commit()
            db.refresh(contact)
            return contact
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

    # 担当者IDが存在する場合は更新(update)
    else:
        try:
            query = (select(ContactModel).join(DepartmentModel).filter(
                DepartmentModel.client_id == client_id).filter(
                ContactModel.department_id == department_id).filter(
                ContactModel.contact_id == contacts_in.contact_id).filter(
                ContactModel.company_id == current_user.company_id))
            result = db.execute(query)
            contact = result.scalar_one_or_none()
            if not contact:
                db.rollback()
                raise HTTPException(
                    status_code=404, detail="contact not found")
            contact.contact_name = contacts_in.contact_name
            contact.role = contacts_in.role
            contact.contact_email = contacts_in.contact_email
            contact.contact_phone = contacts_in.contact_phone
            db.commit()
            db.refresh(contact)
            return contact
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()


def delete_contact(db: Session, client_id: int, department_id: int, contact_id: int, current_user: Users):
    try:
        query = (select(ContactModel).join(DepartmentModel).filter(
            DepartmentModel.client_id == client_id).filter(
            ContactModel.department_id == department_id).filter(
            ContactModel.contact_id == contact_id).filter(
            ContactModel.company_id == current_user.company_id))
        result = db.execute(query)
        contact = result.scalar_one_or_none()

        if contact is None:
            db.rollback()
            raise HTTPException(status_code=404, detail="contact not found")

        db.delete(contact)
        db.commit()
        return contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# POST
def create_contact(db: Session, client_id: int, department_id: int, contacts_in: PostContactIn, current_user: Users):
    try:
        contact = ContactModel(
            department_id=department_id,
            contact_name=contacts_in.contact_name,
            role=contacts_in.role,
            contact_email=contacts_in.contact_email,
            contact_phone=contacts_in.contact_phone,
            created_by_user_id=current_user.user_id,
            company_id=current_user.company_id,
        )
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
