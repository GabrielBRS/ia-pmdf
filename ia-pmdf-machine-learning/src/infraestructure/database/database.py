import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IAPMDF_AUDIT")


class AuditRepository:

    async def registrar_acao(self, usuario: str, ip: str, acao: str, detalhes: dict):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "usuario_id": usuario,
            "ip_origem": ip,
            "evento": acao,
            "payload": detalhes
        }

        logger.info(f"AUDIT_LOG_SUCCESS: {log_entry}")
        return True