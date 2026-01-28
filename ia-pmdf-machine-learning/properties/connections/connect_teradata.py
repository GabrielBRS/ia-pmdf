import os
import teradatasql
from dotenv import load_dotenv
from pathlib import Path

def load_unified_env():

    base_path = Path(__file__).resolve().parents[2]
    env_path = base_path / 'properties' / 'environments' / 'env-dev.env'

    if not env_path.exists():
        env_path = Path.home() / 'iapmdf' / 'properties' / 'environments' / 'env-dev.env'

    load_dotenv(env_path)

def get_teradata_config():
    load_unified_env()
    return {
        'host': os.getenv('TERADATA_HOST'),
        'user': os.getenv('TERADATA_USER'),
        'password': os.getenv('TERADATA_PASSWORD'),
        'logmech': os.getenv('TERADATA_LOGMECH', 'LDAP')
    }

def conectar_teradata():
    try:
        config = get_teradata_config()
        conn = teradatasql.connect(**config)
        print("✅ Conexão estabelecida com a base de dados do IA PMDF.")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar no Teradata: {str(e)}")
        raise