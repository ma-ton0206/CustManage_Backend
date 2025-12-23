from fastapi import APIRouter, Depends
from typing import List
from api.database.db import get_db
from api.schemas.user import PostUserIn, PostUserOut, GetUserOut, PutUserIn, PutUserOut, DeleteUserOut, LoginUserIn, LoginUserOut, AdminCreateUserOut, AdminCreateUserIn, ActivateUserIn, ActivateUserOut
from api.cruds.user import create_user, get_users, update_user, delete_user, login_user, create_user_for_company, get_me
from sqlalchemy.orm import Session
from api.utils.auth import get_current_user, activate_user
from api.models.users import Users
import uuid

router = APIRouter()


@router.post("/api/users", response_model=PostUserOut)
def create_user_endpoint(
        user_data: PostUserIn,
        db: Session = Depends(get_db),
        # current_user: Users = Depends(get_current_user)
):
    print("CREATE USER 実行前")
    return create_user(db, user_data)


# @router.get("/api/users", response_model=List[GetUserOut])
# def get_users_endpoint(
#     db: Session = Depends(get_db),
#     current_user: Users = Depends(get_current_user),
# ):
#     print("✅ current_user:", current_user.user_email)
#     return get_users(db, current_user)


@router.put("/api/users/{user_id}", response_model=PutUserOut)
def update_user_endpoint(
    user_id: uuid.UUID,
    user_data: PutUserIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return update_user(db, user_id, user_data, current_user)


@router.delete("/api/users/{user_id}", response_model=DeleteUserOut)
def delete_user_endpoint(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return delete_user(db, user_id, current_user)


@router.post("/api/users/login",response_model=LoginUserOut)
def login_user_endpoint(
    user_data: LoginUserIn,
    db: Session = Depends(get_db),
):
    return login_user(db, user_data)


# 仮登録用エンドポイント
@router.post("/api/users/register", response_model=AdminCreateUserOut)
def create_user_for_company_endpoint(
    user_in: AdminCreateUserIn,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return create_user_for_company(db, user_in, current_user)


# 本登録用エンドポイント
@router.patch("/api/users/activate", response_model=ActivateUserOut)
def activate_user_endpoint(
    user_in: ActivateUserIn,
    db: Session = Depends(get_db)
):
    return activate_user(db, user_in)

@router.get("/api/users/me", response_model=GetUserOut)
def get_me_endpoint(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    return get_me(db, current_user)