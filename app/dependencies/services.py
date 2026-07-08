from app.config import settings
from app.services import NotificationService, TelegramService

telegram: TelegramService = TelegramService(
    bot_token=settings.BOT_TOKEN,
    chat_id=settings.CHAT_ID,
)

notifier: NotificationService = NotificationService(telegram)


def get_notifier() -> NotificationService:
    return notifier
