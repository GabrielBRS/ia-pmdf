import os
import io
import boto3
import psutil
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv


def load_unified_env():
    base_path = Path(__file__).resolve().parents[2]
    env_path = base_path / 'properties' / 'environments' / 'env-dev.env'

    if not env_path.exists():
        env_path = Path.home() / 'iapmdf' / 'properties' / 'environments' / 'env-dev.env'

    load_dotenv(env_path)


def log_system_resources():
    mem = psutil.virtual_memory()
    print(f"📊 [IA PMDF RAM] Usada: {mem.used / (1024 ** 3):.2f}GB | Disp: {mem.available / (1024 ** 3):.2f}GB")
    print(f"📊 [IA PMDF CPU] Uso: {psutil.cpu_percent()}%")


def get_s3_client():
    load_unified_env()
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'sa-east-1')
    )


def upload_to_s3(df, area, nome_arquivo, camada, extensao='parquet'):
    try:
        s3 = get_s3_client()
        bucket_name = 'ortzion-parquet-datasource'
        file_name = f"{nome_arquivo}.{extensao}"
        file_key = f"{area}/dev/{camada}/{extensao}/{file_name}"

        log_system_resources()

        if isinstance(df, pd.DataFrame):
            buffer = io.BytesIO()
            if extensao == 'parquet':
                df.to_parquet(buffer, index=False, compression='gzip')
            elif extensao == 'csv':
                df.to_csv(buffer, index=False)
            buffer.seek(0)
            s3.upload_fileobj(buffer, bucket_name, file_key)
        else:
            s3.upload_file(Filename=str(df), Bucket=bucket_name, Key=file_key)

        print(f"✅ S3: {file_name} enviado para {file_key}")
        log_system_resources()

    except Exception as e:
        print(f"❌ Erro no upload S3: {str(e)}")


def read_from_s3(area, nome_arquivo, camada, tipo_arquivo='parquet'):
    try:
        s3 = get_s3_client()
        bucket_name = 'ortzion-parquet-datasource'
        file_key = f"{area}/dev/{camada}/{tipo_arquivo}/{nome_arquivo}.{tipo_arquivo}"

        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        body = response['Body'].read()

        if tipo_arquivo == 'parquet':
            return pd.read_parquet(io.BytesIO(body))
        elif tipo_arquivo == 'csv':
            return pd.read_csv(io.BytesIO(body))
        elif tipo_arquivo == 'npy':
            return np.load(io.BytesIO(body))

        return body
    except Exception as e:
        print(f"❌ Erro na leitura S3: {str(e)}")
        return None