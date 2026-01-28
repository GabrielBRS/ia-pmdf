ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates tini procps nano less iputils-ping \
 && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash app
WORKDIR /app

COPY ../requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install "jupyterlab==4.*"

COPY --chown=app:app ../notebooks .

ENV PYTHONPATH=/app \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    PYTHONFAULTHANDLER=1 \
    SHELL=/bin/bash TERM=xterm-256color

EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -fsS http://localhost:8888/api || exit 1

USER app

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["bash", "-lc", "jupyter lab \
  --ServerApp.ip=0.0.0.0 \
  --ServerApp.port=8888 \
  --ServerApp.root_dir=/app \
  --ServerApp.allow_remote_access=True \
  --ServerApp.token='' \
  --ServerApp.password='' \
  --ServerApp.terminals_enabled=True \
  --ServerApp.terminado_settings='{\"shell_command\":[\"/bin/bash\"]}'"]
