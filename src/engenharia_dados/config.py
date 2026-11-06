
import os
from pathlib import Path

from dotenv import load_dotenv


# Caminho do arquivo .env
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"

# URL da API
OPENWEATHER_BASE_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)


def load_environment() -> None:
    """Carrega as variáveis de ambiente do projeto."""
    load_dotenv(dotenv_path=ENV_PATH)


def get_env_variable(name: str) -> str:
    """Retorna uma variável de ambiente obrigatória."""
    load_environment()

    value = os.getenv(name)

    if not value:
        raise ValueError(
            f"Variável de ambiente '{name}' não configurada."
        )

    return value
