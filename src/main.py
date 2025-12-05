from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime, timezone
import json
import sys

from config.settings import get_settings
from src.core.logger import get_logger
from src.sources.defillama_client import fetch_all_pools
from src.core.filters import apply_filters
from src.core.scoring import rank_pools
from src.core.formatting import format_pools_for_telegram
from src.core.telegram_client import send_telegram_message


logger = get_logger("defi-yield-scanner")

# 📁 Rutas base del proyecto
ROOT_DIR = Path(__file__).resolve().parents[1]
STORAGE_DIR = ROOT_DIR / "storage"
PROCESSED_DIR = STORAGE_DIR / "processed"

# 📊 Carpeta del dashboard DeepBlockAI
DASHBOARD_DATA_DIR = ROOT_DIR.parent / "deepblockai-dashboard" / "data"

# 🔗 Integración opcional con un writer del dashboard (si existe)
DASHBOARD_PATH = ROOT_DIR.parent / "deepblockai-dashboard"
if DASHBOARD_PATH.exists():
    sys.path.append(str(DASHBOARD_PATH))
    try:
        from writer import save_bot_payload  # type: ignore
    except Exception:
        save_bot_payload = None
else:
    save_bot_payload = None


def _build_dashboard_items(pools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items = []
    for p in pools:
        items.append(
            {
                "project": p.get("project"),
                "symbol": p.get("symbol"),
                "chain": p.get("chain"),
                "tvlUsd": float(p.get("tvlUsd") or 0.0),
                "apy": float(p.get("apy") or 0.0),
                "apyBase": p.get("apyBase"),
                "apyReward": p.get("apyReward"),
                "score": p.get("defiYieldScore", 0.0),
                "url": p.get("url") or f"https://defillama.com/yields/pool/{p.get('pool')}",
            }
        )
    return items


def _save_json_for_dashboard(items: List[Dict[str, Any]]) -> None:
    """
    Guarda el resultado en:
      - storage/processed/defi-yield_YYYYMMDD_HHMMSS.json      (histórico interno)
      - ../deepblockai-dashboard/data/defi-yield-latest.json   (consumido por el dashboard)
    """
    try:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)

        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

        internal_path = PROCESSED_DIR / f"defi-yield_{ts}.json"
        dashboard_path = DASHBOARD_DATA_DIR / "defi-yield-latest.json"

        # Guardar histórico interno
        with internal_path.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        # Copiar/actualizar archivo del dashboard
        dashboard_path.write_text(internal_path.read_text(encoding="utf-8"), encoding="utf-8")

        logger.info(f"💾 JSON guardado en {internal_path}")
        logger.info(f"📊 JSON actualizado para dashboard en {dashboard_path}")
    except Exception as e:
        logger.error(f"❌ Error guardando JSON para dashboard: {e}")


def run():
    settings = get_settings()
    logger.info("🚀 Iniciando defi-yield-scanner (env=%s)", settings.env)

    # 1) Pools brutos desde DeFiLlama
    pools_raw = fetch_all_pools()

    # 2) Filtros de riesgo / parámetros
    pools_filtered = apply_filters(pools_raw, settings)

    if not pools_filtered:
        logger.warning("No hay pools tras filtros; no se envía mensaje.")
        send_telegram_message(
            settings.telegram_bot_token,
            settings.telegram_chat_id,
            "⚠️ No se encontraron yields que cumplan los filtros de riesgo hoy.",
        )
        return

    # 3) Ranking con scoring
    ranked = rank_pools(pools_filtered, settings)

    # 4) Top N
    top_n = ranked[: settings.top_n]

    # 5) Items para dashboard
    dashboard_items = _build_dashboard_items(top_n)

    # 6) Guardar JSON para dashboard + histórico
    _save_json_for_dashboard(dashboard_items)

    # 7) Integración opcional con writer.py del dashboard (si existe)
    if save_bot_payload:
        try:
            save_bot_payload("defi-yield-scanner", dashboard_items)
            logger.info("🧩 Payload enviado a writer.save_bot_payload")
        except Exception as e:
            logger.error("❌ Error llamando a save_bot_payload: %s", e)

    # 8) Formateo mensaje Telegram
    text = format_pools_for_telegram(top_n)

    # 9) Telegram
    send_telegram_message(
        settings.telegram_bot_token,
        settings.telegram_chat_id,
        text,
        disable_web_page_preview=False,
    )


if __name__ == "__main__":
    run()

