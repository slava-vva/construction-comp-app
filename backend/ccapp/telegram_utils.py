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

from .serializers import MessageListSerializer
# from rest_framework.response import Response

def send_message(chat_id, chat_user_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    resp = requests.post(url, json=payload)
    if resp.status_code == 200:
        # Save in DB after successful send
        msg = MessageList.objects.create(
            receiver_id=chat_user_id,
            sender_id=2,  # manager/system/etc.
            text=text
        )
        serializer = MessageListSerializer(msg)
        return serializer.data
        # return resp.json()
    else:
        # log error if needed
        return {"error": resp.text, "status": resp.status_code}
    

# store last update_id to avoid duplicates
LAST_UPDATE_ID = 0

def poll_updates():
    global LAST_UPDATE_ID

    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 10, "offset": LAST_UPDATE_ID + 1}  # only new updates
    resp = requests.get(url, params=params)
    data = resp.json()

    if not data.get("ok"):
        return {"ok": False, "error": data}

    results = data.get("result", [])
    saved = []
    
    for update in results:
        LAST_UPDATE_ID = update["update_id"]

        message = update.get("message")
        if not message:
            continue

        chat_id = message["chat"]["id"]
        username = message["from"].get("username") or f"tg_{chat_id}"
        text = message.get("text", "")

        # ensure user exists
        # chat_user_id = get_or_create_chat_user(username))
        chat_user, _ = ChatUser.objects.get_or_create(
            chat_id=chat_id,
            defaults={"name": username}
        )

        # store message (sender = this telegram user, receiver = manager/system)
        msg = MessageList.objects.create(
            sender=chat_user,
            receiver_id=2,  # manager/system
            text=text
        )
        saved.append(msg.id)

    return {"ok": True, "saved": saved, "count":len(saved)}
