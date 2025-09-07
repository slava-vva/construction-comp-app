# chat_app/telegram_utils.py
import requests
from django.conf import settings
from .models import ChatUser, MessageList
# from telegram_bot import get_or_create_chat_user
from .telegram_bot import get_or_create_chat_user

BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"
print(BASE_URL)

def fetch_updates(offset=None):
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 10, "offset": offset}
    resp = requests.get(url, params=params)
    return resp.json()

def process_updates(updates):
    for update in updates.get("result", []):
        message = update.get("message")
        if not message:
            continue

        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        user = message["from"]

        # Create/find ChatUser
        chat_user_id = get_or_create_chat_user(user.get("username"))
        # chat_user, _ = ChatUser.objects.get_or_create(
        #     chat_id=chat_id,
        #     defaults={"name": user.get("username") or f"tg_{chat_id}"}
        # )

        # Store message (receiver = manager id 2 for now)
        MessageList.objects.create(
            sender_id=chat_user_id,
            receiver_id=2,
            text=text
        )

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    resp = requests.post(url, json=payload)
    return resp.json()
