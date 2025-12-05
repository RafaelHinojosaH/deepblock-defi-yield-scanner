import requests
from src.core.logger import get_logger


logger = get_logger("telegram-client")


def send_telegram_message(
    bot_token: str,
    chat_id: str,
    text: str,
    disable_web_page_preview: bool = False,
) -> None:
    if not bot_token or not chat_id:
        logger.warning("No hay TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID configurados.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": disable_web_page_preview,
    }

    resp = requests.post(url, json=payload, timeout=20)
    if not resp.ok:
        logger.error("Error enviando mensaje a Telegram: %s - %s", resp.status_code, resp.text)
    else:
        logger.info("Mensaje enviado a Telegram correctamente.")

