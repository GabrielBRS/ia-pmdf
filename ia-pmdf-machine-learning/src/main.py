import mimetypes
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import fitz
import re

mimetypes.init()
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

app = FastAPI(title="IA PMDF - Inteligência Policial")

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "resources" / "web"
INDEX_FILE = WEB_DIR / "index.html"

print(f"--> [IAPMDF] Servindo interface de: {WEB_DIR}")

@app.get("/")
async def serve_index():
    if not INDEX_FILE.exists():
        raise HTTPException(status_code=404, detail="Interface index.html não encontrada")
    return FileResponse(INDEX_FILE)


@app.post("/api/v1/analisar-documento")
async def analisar_documento(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas PDFs são aceitos.")

    conteudo = await file.read()
    try:

        with fitz.open(stream=conteudo, filetype="pdf") as doc:
            texto = "".join([pagina.get_text() for pagina in doc])

        nup = re.search(r"(\d{5}\.\d{6}/\d{4}-\d{2})", texto)

        return {
            "filename": file.filename,
            "metadados": {
                "numero_processo": nup.group(0) if nup else "Não identificado",
                "tipo_documento": "Ofício" if "OFÍCIO" in texto.upper() else "Decisão" if "DECISÃO" in texto.upper() else "Outros"
            },
            "preview": texto[:500]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")
