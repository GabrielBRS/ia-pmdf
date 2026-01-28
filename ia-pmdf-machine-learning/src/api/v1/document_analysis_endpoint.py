import router
from fastapi import UploadFile, Depends, File

from src.services.document_service import AnaliseDocumentoService


@router.post("/analisar-documento")
async def analisar_documento(
        file: UploadFile = File(...),
        service: AnaliseDocumentoService = Depends()
):
    user_context = {"user_id": "analista_cgint_01", "ip": "10.0.0.50"}
    conteudo = await file.read()
    resultado = await service.executar_analise_fluxo(conteudo, file.filename, user_context)
    return resultado