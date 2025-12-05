from typing import List, Dict, Any


def format_pools_for_telegram(pools: List[Dict[str, Any]]) -> str:
    if not pools:
        return "⚠️ No se encontraron yields que cumplan los filtros de riesgo hoy."

    lines = []
    lines.append("💰 *Top Yields verificados hoy*")
    lines.append("")
    rank = 1

    for p in pools:
        symbol = p.get("symbol") or "N/A"
        project = p.get("project") or "N/A"
        chain = p.get("chain") or "N/A"
        tvl = float(p.get("tvlUsd") or 0.0)
        apy = float(p.get("apy") or 0.0)
        apy_base = p.get("apyBase")
        apy_reward = p.get("apyReward")
        score = p.get("defiYieldScore", 0.0)
        url = p.get("url") or f"https://defillama.com/yields/pool/{p.get('pool')}"

        lines.append(f"*#{rank}* — `{symbol}` en *{project}* ({chain})")
        lines.append(f"TVL: `${tvl:,.0f}` · APY: *{apy:.2f}%* · Score: `{score:.1f}`")

        if apy_base is not None or apy_reward is not None:
            base_str = f"{float(apy_base):.2f}%" if apy_base is not None else "-"
            rew_str = f"{float(apy_reward):.2f}%" if apy_reward is not None else "-"
            lines.append(f"Base: {base_str} · Rewards: {rew_str}")

        if url:
            lines.append(f"[Ver pool en DeFiLlama]({url})")

        lines.append("")

        rank += 1

    lines.append("DeepBlockAI — defi-yield-scanner")
    return "\n".join(lines)

