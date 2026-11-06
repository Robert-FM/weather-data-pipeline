
import json
from pathlib import Path

import pandas as pd


def transform_weather_data(
    input_path: str = "data/weather_data.json",
) -> pd.DataFrame:
    """
    Transforma os dados JSON da OpenWeatherMap
    em um DataFrame estruturado.

    Args:
        input_path: Caminho do arquivo JSON.

    Returns:
        DataFrame com os dados meteorológicos.
    """

    # Carrega os dados extraídos
    with Path(input_path).open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    # Extrai os campos do JSON
    weather_data = {
        "city_id": data["id"],
        "city": data["name"],
        "country": data["sys"]["country"],
        "latitude": data["coord"]["lat"],
        "longitude": data["coord"]["lon"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "weather_description": data["weather"][0]["description"],
        "timestamp": pd.to_datetime(
            data["dt"],
            unit="s",
            utc=True,
        ),
    }

    # Converte para DataFrame
    df = pd.DataFrame([weather_data])

    return df


if __name__ == "__main__":
    df = transform_weather_data()

    print("\nDados transformados com sucesso!\n")
    print(df.to_string(index=False))
    print("\nTipos de dados:")
    print(df.dtypes)
