
import json
import os
from pathlib import Path

import requests

from engenharia_dados.config import (
    OPENWEATHER_BASE_URL,
    get_env_variable,
)


def extract_weather_data(city: str = "Recife") -> dict:
    """
    Extrai dados meteorológicos da API OpenWeatherMap
    e salva a resposta em um arquivo JSON.

    Args:
        city (str): Nome da cidade para consulta.

    Returns:
        dict: Dados meteorológicos retornados pela API.
    """

    # Recupera a chave da API
    api_key = get_env_variable("OPENWEATHER_API_KEY")

    # Parâmetros da requisição
    params = {
        "q": f"{city},BR",
        "appid": api_key,
        "units": "metric",
        "lang": "pt_br",
    }

    # Realiza a requisição HTTP
    response = requests.get(
        OPENWEATHER_BASE_URL,
        params=params,
        timeout=30,
    )

    # Verifica se houve erro HTTP
    response.raise_for_status()

    # Converte a resposta para JSON
    data = response.json()

    # Define o caminho do arquivo de saída
    # Utiliza WEATHER_DATA_PATH quando configurada
    output_path = Path(
        os.getenv(
            "WEATHER_DATA_PATH",
            "data/weather_data.json",
        )
    )

    # Cria o diretório caso não exista
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Salva os dados em JSON
    with output_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print(
        f"Dados meteorológicos de {city} "
        "extraídos com sucesso!"
    )
    print(f"Arquivo salvo em: {output_path}")

    return data


if __name__ == "__main__":
    extract_weather_data()
