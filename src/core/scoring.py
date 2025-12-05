from typing import List, Dict, Any
from math import log10

from src.core.logger import get_logger
from config.settings import Settings


logger = get_logger("defi-scoring")


def compute_score(pool: Dict[str, Any], settings: Settings) -> float:
    apy = float(pool.get("apy") or 0.0)
    apy_base = float(pool.get("apyBase") or 0.0)
    apy_reward = float(pool.get("apyReward") or 0.0)
    tvl_usd = float(pool.get("tvlUsd") or 0.0)

    # 1) Normalizar APY [0, 1] en función del MAX_APY
    apy_score = min(apy / settings.max_apy, 1.0)

    # 2) Bonus por TVL usando log10 (para que 1M sea mejor que 100k, etc.)
    tvl_floor = max(tvl_usd, settings.min_tvl_usd)
    tvl_score = min(log10(tvl_floor) / 8.0, 1.0)  # 10^8 ~ 100M

    # 3) Preferimos apyBase sobre apyReward (más sostenible)
    base_weight = 0.6 if apy > 0 else 0.0
    if apy > 0:
        base_ratio = apy_base / apy if apy > 0 else 0
    else:
        base_ratio = 0.0

    sustainability_score = base_ratio  # 0–1

    # Mezcla final
    total_score = (
        0.5 * apy_score +
        0.3 * tvl_score +
        0.2 * sustainability_score
    )

    return round(total_score * 100, 2)  # en escala 0–100


def rank_pools(pools: List[Dict[str, Any]], settings: Settings) -> List[Dict[str, Any]]:
    logger.info("Calculando score para %s pools", len(pools))
    enriched = []
    for p in pools:
        p = dict(p)  # copia
        p["defiYieldScore"] = compute_score(p, settings)
        enriched.append(p)

    sorted_pools = sorted(enriched, key=lambda x: x["defiYieldScore"], reverse=True)
    logger.info("Top score máximo: %.2f", sorted_pools[0]["defiYieldScore"] if sorted_pools else 0.0)
    return sorted_pools

