from sqlalchemy import create_engine
# 非同期のSQLAlchemyをインポート
from sqlalchemy.orm import sessionmaker, declarative_base, Session
# ormからsessionmakerとdeclarative_baseをインポート
import os

#DB_URL ="postgresql+psycopg2://<ユーザー名>:<パスワード>@<ホスト名>:<ポート>/<データベース名>"
DB_URL = os.getenv(
    "DATABASE_URL"
    # "postgresql+psycopg2://postgres:postgres@db:5432/CustManage"
)
engine = create_engine(DB_URL, echo=True)
# engineを作成してDBとの接続設定をしている。
# echo=Trueは、SQLの実行結果をconsoleに表示する設定

session_local = sessionmaker(
    # sessionmakerで接続口を作成。一時的なデータベースとの通信を可能にするオブジェクトを作成している。
    # autocommit=False, autoflush=Falseは、データベースに対する変更を即時に反映させない設定
    # bind=async_engineは、作成したengineを使ってデータベースとの通信を行う設定
    # class_=AsyncSessionは、非同期のセッションを作成する設定
    autocommit=False, autoflush=False, bind=engine, class_=Session
)

Base = declarative_base()
# 基底クラスを作成している。modelsでインポートされる。
# Base を継承したmodelクラスだけが、SQLAlchemy に「DBテーブル」として登録される。


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
