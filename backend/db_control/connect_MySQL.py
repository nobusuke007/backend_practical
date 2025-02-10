from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

import pymysql
pymysql.install_as_MySQLdb #pymysqlのインポート

# 環境変数の読み込み
load_dotenv()

# 環境変数の値をデバッグ出力
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
print(f"SSL_CA: {os.getenv('SSL_CA')}")

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SSL_CA = os.getenv("SSL_CA")  #SSL認証の構文を追加

# MySQLのURL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca={SSL_CA}"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)
