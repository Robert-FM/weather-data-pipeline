
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from engenharia_dados.config import get_env_variable


def test_connection() -> None:
    """Testa a conexão com o PostgreSQL."""

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=get_env_variable("POSTGRES_USER"),
        password=get_env_variable("POSTGRES_PASSWORD"),
        host=get_env_variable("POSTGRES_HOST"),
        port=int(get_env_variable("POSTGRES_PORT")),
        database=get_env_variable("POSTGRES_DB"),
    )

    engine = create_engine(database_url)

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), version()")
        )

        database, version = result.fetchone()

        print("Conexão realizada com sucesso!")
        print(f"Banco de dados: {database}")
        print(f"PostgreSQL: {version.split(',')[0]}")

    engine.dispose()


if __name__ == "__main__":
    test_connection()
