from typing import List, Dict, Any
from src.core.logger import get_logger
from config.settings import Settings


logger = get_logger("defi-filters")


def _safe_float(value, default=None):
    try:
        return float(value)
    except Exception:
        return default


def apply_filters(pools: List[Dict[str, Any]], settings: Settings) -> List[Dict[str, Any]]:
    """
    Aplica filtros de:
    - TVL mínimo
    - APY máximo
    - Cadenas preferidas (si están configuradas)
    """
    logger.info("Aplicando filtros a %s pools", len(pools))

    preferred_chains_lower = {c.lower() for c in settings.preferred_chains}

    filtered = []
    for p in pools:
        tvl_usd = _safe_float(p.get("tvlUsd"), 0.0)
        apy = _safe_float(p.get("apy"), None)

        if tvl_usd is None or tvl_usd < settings.min_tvl_usd:
            continue

        if apy is None:
            # si no hay apy total, intenta apyBase + apyReward
            apy_base = _safe_float(p.get("apyBase"), None)
            apy_reward = _safe_float(p.get("apyReward"), 0.0)
            if apy_base is None:
                continue
            apy = apy_base + (apy_reward or 0.0)

        # APY razonable
        if apy <= 0 or apy > settings.max_apy:
            continue

        chain = (p.get("chain") or "").lower()
        if preferred_chains_lower and chain not in preferred_chains_lower:
            continue

        filtered.append(p)

    logger.info("Pools tras filtros: %s", len(filtered))
    return filtered

