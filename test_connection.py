from sqlalchemy import text

from app.database.session import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE()"))
        database = result.scalar_one()

except Exception as error:
    print("Não foi possível conectar ao MySQL.")
    print(f"Detalhes: {error}")