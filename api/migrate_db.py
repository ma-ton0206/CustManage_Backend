from sqlalchemy import create_engine
from api.database.db import Base

# モデルを全部読み込んで Base.metadata に登録
from api.models import users, task, company, client, sales, contact, department, purchase_details

#DB_URL ="postgresql+psycopg2://<ユーザー名>:<パスワード>@<ホスト名>:<ポート>/<データベース名>"
DB_URL = "postgresql+psycopg2://postgres:postgres@db:5432/CustManage"

engine = create_engine(DB_URL, echo=True)


def reset_database():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
