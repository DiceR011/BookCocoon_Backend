# api/migrate_db.py
from sqlalchemy import create_engine
from api.db import Base  # 共通のBaseをインポート
from api.models.book import Book  # Bookモデルをインポート
from api.models.progress import Progress  # Progressモデルをインポート

DB_URL = "mysql+pymysql://root@db:3306/demo?charset=utf8"
engine = create_engine(DB_URL, echo=True)

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()
