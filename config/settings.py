import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import List


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


@dataclass
class Settings:
    env: str
    telegram_bot_token: str
    telegram_chat_id: str

    min_tvl_usd: float
    max_apy: float
    preferred_chains: List[str]
    top_n: int


def _parse_list(value: str) -> List[str]:
    if not value:
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


def get_settings() -> Settings:
    env_path = os.path.join(BASE_DIR, ".env")
    load_dotenv(env_path)

    return Settings(
        env=os.getenv("ENV", "local"),
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        min_tvl_usd=float(os.getenv("MIN_TVL_USD", "500000")),
        max_apy=float(os.getenv("MAX_APY", "250")),
        preferred_chains=_parse_list(
            os.getenv("PREFERRED_CHAINS", "Ethereum,Arbitrum,Base,Solana")
        ),
        top_n=int(os.getenv("TOP_N", "10")),
    )

