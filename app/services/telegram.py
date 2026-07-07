from __future__ import annotations
import httpx


class TelegramService:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    async def send_message(
        self,
        text: str,
        parse_mode: str = "HTML",
        disable_notification: bool = False,
    ) -> bool:
        """
        Sends a message to the configured Telegram chat.

        Returns:
            True if Telegram accepted the message.
            False otherwise.
        """

        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_notification": disable_notification,
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)

        if response.status_code != 200:
            return False

        data = response.json()

        return data.get("ok", False)
