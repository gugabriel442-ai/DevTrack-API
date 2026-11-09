
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text

load_dotenv(".env.aiven")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "devtrack_db")
DB_SSL_CA = os.getenv("DB_SSL_CA")

if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_SSL_CA]):
    raise ValueError("Confira as variáveis do arquivo .env.aiven.")

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    query={"charset": "utf8mb4"},
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"ssl": {"ca": DB_SSL_CA}},
)

try:
    with engine.connect() as connection:
        resultado = connection.execute(
            text("SELECT DATABASE()")
        ).scalar()

        print("Conexão com a Aiven realizada com sucesso!")
        print(f"Banco conectado: {resultado}")

except Exception as erro:
    print("Não foi possível conectar à Aiven.")
    print(f"Detalhes: {erro}")

finally:
    engine.dispose()
