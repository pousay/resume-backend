from __future__ import annotations

from datetime import timezone

from app.schema import Contact
from app.services.telegram import TelegramService


class NotificationService:
    def __init__(self, telegram: TelegramService):
        self.telegram = telegram

    async def notify_new_contact(self, contact: Contact) -> None:
        created_at = contact.created_at

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        message = f"""
<b>📨 New Contact</b>

<b>👤 Name</b>
{self._escape(contact.name)}

<b>💬 Message</b>
{self._escape(contact.message)}

<b>🌐 IP Address</b>
<code>{self._escape(contact.ip_address)}</code>

<b>🖥 User-Agent</b>
<code>{self._escape(contact.user_agent)}</code>

<b>🕒 Time (UTC)</b>
<code>{created_at.strftime("%Y-%m-%d %H:%M:%S")}</code>
""".strip()

        await self.telegram.send_message(message)

    @staticmethod
    def _escape(text: str) -> str:
        """
        Escape HTML special characters since we're using parse_mode="HTML".
        """
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
