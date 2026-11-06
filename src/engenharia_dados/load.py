
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from engenharia_dados.config import get_env_variable
from engenharia_dados.transform import transform_weather_data


def load_weather_data(df: pd.DataFrame) -> None:
    if df.empty:
        print("Nenhum registro para carregar.")
        return

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
        with engine.begin() as connection:
            connection.execute(text("""
                CREATE TEMP TABLE weather_data_staging
                (LIKE weather_data)
                ON COMMIT DROP
            """))

            df.to_sql(
                name="weather_data_staging",
                con=connection,
                if_exists="append",
                index=False,
            )

            result = connection.execute(text("""
                INSERT INTO weather_data (
                    city_id, city, country, latitude, longitude,
                    temperature, feels_like, humidity, pressure,
                    wind_speed, weather_description, timestamp
                )
                SELECT DISTINCT ON (city_id, timestamp)
                    city_id, city, country, latitude, longitude,
                    temperature, feels_like, humidity, pressure,
                    wind_speed, weather_description, timestamp
                FROM weather_data_staging
                ORDER BY city_id, timestamp
                ON CONFLICT (city_id, timestamp)
                DO NOTHING
            """))

            inserted = result.rowcount

        print("Carga no PostgreSQL concluida!")
        print(f"Registros recebidos: {len(df)}")
        print(f"Registros novos inseridos: {inserted}")
        print(f"Registros ignorados: {len(df) - inserted}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    df = transform_weather_data()
    load_weather_data(df)
