from __future__ import annotations

from datetime import timezone

from app.schema import Contact
from app.services.telegram import TelegramService


class NotificationService:
    def __init__(self, telegram: TelegramService):
        self.telegram = telegram

    async def notify_new_contact(self, contact: Contact, i: int = 1) -> None:
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

        try:
            await self.telegram.send_message(message)
        except Exception as e:
            print(f"[{i}] Failed to send notification: {e}")
            if i > 5:
                print(f"Maximum Retries")
                return

            await self.notify_new_contact(contact, i + 1)

    @staticmethod
    def _escape(text: str) -> str:
        """
        Escape HTML special characters since we're using parse_mode="HTML".
        """
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
