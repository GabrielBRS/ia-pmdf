import os
from pathlib import Path
from dotenv import load_dotenv


def setAmbienteSistema(ambiente):
    base_path = Path(__file__).resolve().parent
    env_file = f"env-{ambiente}.env"
    env_path = base_path / env_file

    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
        os.environ["IAPMDF_ENV_ACTIVE"] = ambiente
        print(f"⚙️ [IAPMDF] Ambiente '{ambiente.upper()}' ativado. Configs de: {env_file}")
    else:
        if ambiente != "dev":
            raise FileNotFoundError(f"ERRO CRÍTICO: Configuração {env_file} obrigatória não encontrada!")

        print(f"⚠️ [IAPMDF] Aviso: Arquivo {env_file} não encontrado. Usando defaults de dev.")
        os.environ["IAPMDF_ENV_ACTIVE"] = "dev"