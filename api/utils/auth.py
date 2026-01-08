from passlib.context import CryptContext
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from datetime import datetime, timedelta
from jose import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.db import get_db
from api.models.users import Users
from api.schemas.user import ActivateUserIn
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import resend

bearer_scheme = HTTPBearer()


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# トークンを取り出す依存関数
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


# data: トークンに含めるデータ。emailを含める {"sub": "taro@example.com"}
# expires_delta: トークンの有効期限。60分
def create_access_token(data: dict, expires_delta: timedelta = None):
    # dataをコピーして、to_encodeに代入
    to_encode = data.copy()
    # 有効期限を設定
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    # 有効期限をto_encodeに追加
    to_encode.update({"exp": int(expire.timestamp())})
    # トークンを生成
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ユーザー認証依存関数
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     # token = request.cookies.get("token")
#     print("get_current_userのtoken:", token)

#     if not token:
#         raise HTTPException(status_code=401, detail="Token missing")
#     print("tokenがある")
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_email = payload.get("sub")
#         print("user_email:", user_email)
#         if user_email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         print("user_emailがある")
#         user = db.query(Users).filter(Users.user_email == user_email).first()
#         if user is None:
#             raise HTTPException(status_code=401, detail="User not found")
#         return user

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # ← ここで Bearer Token が取れる

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload.get("sub")

    if user_email is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(Users).filter(Users.user_email == user_email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# # ユーザーが所属の企業を取得する依存関数
# def verify_company_access(
#     target_company_id: uuid.UUID,  # 操作対象の会社ID
#     current_user: Users = Depends(get_current_user)
# ):
#     if current_user.company_id != target_company_id:
#         raise HTTPException(status_code=403, detail="Access denied")
#     return True

# 仮登録用トークンを生成する関数
def create_activation_token(user: Users):
    expire = datetime.utcnow() + timedelta(hours=1)  # 有効期限1h
    payload = {
        "sub": str(user.user_email),
        "company_id": str(user.company_id),
        "exp": expire
    }
    # 第一引数:ペイロード、第二引数:シークレットキー、第三引数:アルゴリズム
    # 戻り値:トークン
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def send_activation_email(user_email: str, token: str):
    # 仮登録用メール送信関数
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "").strip()

    if not RESEND_API_KEY:
        raise RuntimeError("RESEND_API_KEY is not set")

    print("📩 send_activation_email():", user_email, type(user_email))

    resend.api_key = RESEND_API_KEY

    activation_link = f"https://custmanage-frontend.vercel.app/registerComplete?token={token}"

    try:
        print("--------------------------------メール送信開始--------------------------------")

        response = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [user_email],
            "subject": "【CustManage】アカウント登録のお知らせ",
            "html": f"""
            <hr>
            {user_email} 様<br><br>
            以下のリンクからアカウント登録を完了してください。<br>
            このリンクは24時間有効です。<br><br>
            <a href="{activation_link}">{activation_link}</a><br><br>
            <hr>
            CustManageチーム
            """
        })

        print("send response:", response)
        print("--------------------------------メール送信成功--------------------------------")
        return response

    except Exception as e:
        print("❌ メール送信エラー:", e)
        raise HTTPException(status_code=500, detail=str(e))


# 本登録用エンドポイントを叩くと、ユーザーが本登録される
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def activate_user(db: Session, user_in: ActivateUserIn):
    try:
        payload = jwt.decode(user_in.token, SECRET_KEY, algorithms=[ALGORITHM])

        user = db.query(Users).filter(
            Users.user_email == user_in.user_email).filter(
            Users.company_id == payload.get("company_id")).filter(
            Users.is_active == False).first()

        if not user:
            raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

        user.user_password = pwd_context.hash(user_in.user_password)
        user.user_name = user_in.user_name
        user.is_active = True
        db.commit()
        db.refresh(user)

        return {"message": "アカウントが有効化されました。ログインしてください。"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="無効または期限切れのトークンです")
    finally:
        db.close()

# フロントは// URLのクエリパラメータからトークンを取得
  # const token = new URLSearchParams(window.location.search).get("token");　でgetする
