from passlib.context import CryptContext
from api.models.users import Users
from api.schemas.user import PostUserIn, PutUserIn, AdminCreateUserIn, AdminCreateUserOut, ActivateUserIn, LoginUserIn
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select
from api.utils.auth import create_access_token
from api.utils.auth import create_activation_token, send_activation_email
from fastapi.security import OAuth2PasswordRequestForm
import uuid
from api.constants.status import UserRole
from fastapi import Response
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(
        db: Session,
        user_data: PostUserIn,
        # current_user: Users
):
    # hashed_pw = pwd_context.hash(user_data.user_password)
    raw_password = user_data.user_password
    password_bytes = raw_password.encode("utf-8")[:72]
    safe_password = password_bytes.decode("utf-8", errors="ignore")
    hashed_pw = pwd_context.hash(safe_password)
    company_id = user_data.company_id

    user = Users(
        user_name=user_data.user_name,
        user_email=user_data.user_email,
        user_password=hashed_pw,
        company_id=company_id,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_users(
    db: Session,
    current_user: Users,  # ← ★これで認証ユーザーを取得
):
    try:
        query = (
            select(Users).
            filter(Users.is_active == True).
            filter(Users.company_id == current_user.company_id))
        result = db.execute(query)
        users = result.scalars().all()
        return users
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def update_user(db: Session, user_id: int, user_data: PutUserIn, current_user: Users):
    try:
        query = (
            select(Users).
            filter(Users.user_id == user_id).
            filter(Users.company_id == current_user.company_id))
        result = db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            db.rollback()
            raise HTTPException(status_code=404, detail="user not found")
        user.user_name = user_data.user_name
        user.user_email = user_data.user_email
        user.user_password = pwd_context.hash(user_data.user_password)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def delete_user(db: Session, user_id: int, current_user: Users):
    try:
        query = (
            select(Users).
            filter(Users.user_id == user_id).
            filter(Users.company_id == current_user.company_id))
        result = db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            db.rollback()
            raise HTTPException(status_code=404, detail="user not found")
        user.is_active = False
        user.updated_by_user_id = current_user.user_id
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def login_user(db: Session, user_data: LoginUserIn):
    try:
        print("●1:user_data:", user_data)
        query = (
            select(Users).
            filter(Users.user_email == user_data.user_email).
            filter(Users.is_active == True))
        result = db.execute(query)
        print("●2:result:", result)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        print("●3:user:", user)
        if not pwd_context.verify(user_data.user_password, user.user_password):
            raise HTTPException(status_code=401, detail="パスワードが間違っています")
        print("●4:user.user_password:", user.user_password)
        access_token = create_access_token(data={"sub": user.user_email})

        print("●5:access_token:", access_token)

        return {
            "token": access_token,
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_email": user.user_email,
            "user_role": user.user_role,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# 仮登録用エンドポイントを叩くと、ユーザーが作成される
def create_user_for_company(db: Session, user_in: AdminCreateUserIn, current_user: Users):

    try:
        # ユーザーデータを取得
        user = db.query(Users).filter(
            Users.company_id == current_user.company_id).first()

        # 期限切れの場合はどうする？？メールアドレスはDBに残るから、再度送信する？？

        # メールアドレス重複チェック
        if user.user_email == user_in.user_email:
            raise HTTPException(status_code=403, detail="すでに登録されているメールアドレスです")

        new_user = Users(
            user_email=user_in.user_email,
            company_id=current_user.company_id,
            user_role=user_in.user_role,
            created_by_user_id=current_user.user_id,
            is_active=False,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # # トークン生成してメール送信
        token = create_activation_token(new_user)
        send_activation_email(user_in.user_email, token)

        return {
            "message": "仮登録が完了しました。メールをご確認ください。",
            "user_email": new_user.user_email,
            "user_role": new_user.user_role,
            "token": token,  # ✅ フロントが利用できるように返す
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


def get_me(db: Session, current_user: Users):
    try:
        query = (
            select(Users).
            filter(Users.user_id == current_user.user_id))
        result = db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
        return {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_email": user.user_email,
            "user_role": user.user_role,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()