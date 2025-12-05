from typing import List, Dict, Any
import requests

from src.core.logger import get_logger


logger = get_logger("defillama-client")

YIELDS_URL = "https://yields.llama.fi/pools"


def fetch_all_pools(timeout: int = 20) -> List[Dict[str, Any]]:
    """
    Descarga TODOS los pools de yields.llama.fi/pools.
    La respuesta suele ser: { "status": "success", "data": [ {pool...}, ...] }
    """
    logger.info("Consultando pools de DeFiLlama...")
    resp = requests.get(YIELDS_URL, timeout=timeout)
    resp.raise_for_status()
    payload = resp.json()

    # soportamos ambas formas posibles por si cambia el formato:
    if isinstance(payload, dict) and "data" in payload:
        data = payload.get("data", [])
    elif isinstance(payload, list):
        data = payload
    else:
        logger.warning("Formato inesperado de respuesta DeFiLlama; usando payload tal cual.")
        data = payload

    logger.info("DeFiLlama devolvió %s pools", len(data))
    return data

