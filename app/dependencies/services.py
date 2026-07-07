from app.config import settings
from app.services import NotificationService, TelegramService


def get_notifier() -> NotificationService:
    telegram = TelegramService(
        bot_token=settings.BOT_TOKEN,
        chat_id=settings.CHAT_ID,
    )

    return NotificationService(telegram)
