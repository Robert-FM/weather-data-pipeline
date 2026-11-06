
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from engenharia_dados.config import get_env_variable
from engenharia_dados.transform import transform_weather_data


def load_weather_data(df: pd.DataFrame) -> None:
    """
    Carrega os dados meteorológicos
    em uma tabela PostgreSQL.
    """

    # Configura a conexão com o banco
    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=get_env_variable("POSTGRES_USER"),
        password=get_env_variable("POSTGRES_PASSWORD"),
        host=get_env_variable("POSTGRES_HOST"),
        port=int(get_env_variable("POSTGRES_PORT")),
        database=get_env_variable("POSTGRES_DB"),
    )

    engine = create_engine(database_url)

    try:
        # Insere os dados no PostgreSQL
        with engine.begin() as connection:
            df.to_sql(
                name="weather_data",
                con=connection,
                if_exists="append",
                index=False,
            )

        print("Dados carregados no PostgreSQL com sucesso!")
        print(f"Registros inseridos: {len(df)}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    df = transform_weather_data()
    load_weather_data(df)
