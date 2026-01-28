import uvicorn
import os
import sys
from pathlib import Path

raiz_projeto = Path(__file__).resolve().parent.parent

if str(raiz_projeto) not in sys.path:
    sys.path.insert(0, str(raiz_projeto))

from properties.environments import setAmbienteSistema

if __name__ == "__main__":
    tipoAmbiente = "dev"
    ambiente = os.getenv("IAPMDF_ENV_ACTIVE", tipoAmbiente)
    try:
        setAmbienteSistema(ambiente)
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8000,
            reload=(ambiente == tipoAmbiente),
            app_dir=str(raiz_projeto)
        )
    except Exception as e:
        print(f"💥 Falha catastrófica no startup: {e}")
        sys.exit(1)