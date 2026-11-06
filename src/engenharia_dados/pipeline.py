
from engenharia_dados.extract import extract_weather_data
from engenharia_dados.transform import transform_weather_data
from engenharia_dados.load import load_weather_data


def run_pipeline() -> None:
    """Executa o pipeline ETL de dados meteorológicos."""

    print("\nIniciando pipeline ETL...\n")

    # Etapa 1: Extração
    print("[1/3] Extraindo dados meteorológicos...")
    extract_weather_data()

    # Etapa 2: Transformação
    print("\n[2/3] Transformando os dados...")
    df = transform_weather_data()

    # Etapa 3: Carregamento
    print("\n[3/3] Carregando dados no PostgreSQL...")
    load_weather_data(df)

    print("\nPipeline ETL executado com sucesso!")


if __name__ == "__main__":
    run_pipeline()
