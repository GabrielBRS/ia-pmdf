import datetime
from src.core.document_processor import IAPMDFEngine
from src.infraestructure.database import AuditRepository

class AnaliseDocumentoService:
    def __init__(self):
        self.ai_core = IAPMDFEngine()
        self.audit = AuditRepository()

    async def executar_analise_fluxo(self, pdf_content: bytes, filename: str, user_ctx: dict):

        texto_bruto = self.ai_core.converter_bytes_para_texto(pdf_content)

        entidades = self.ai_core.extrair_entidades_inteligentes(texto_bruto)

        analise_risco = self.ai_core.calcular_score_fraude(texto_bruto, entidades)

        await self.audit.registrar_acao(
            usuario=user_ctx['user_id'],
            ip=user_ctx['ip'],
            acao="ANALISE_IA_IAPMDF",
            detalhes={
                "arquivo": filename,
                "nup": entidades["nup"],
                "score": analise_risco['score'],
                "hash": entidades["hash_conteudo"]
            }
        )

        return {
            "status": "Processado",
            "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "analise": analise_risco,
            "metadados_extraidos": entidades
        }