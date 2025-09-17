import os
import django

# 1. Tell Django which settings to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ccback.settings")

# 2. Setup Django
django.setup()

# 3. Now you can import models
from ccapp.models import ChatUser

print("Hi Django from script")

i = 1
for u in ChatUser.objects.all():
    if u.chat_id is None:
        u.chat_id = i
        u.save()
        i += i
    print(u.id, u.chat_id, u.name, u.created_at)

# n_chat = ChatUser.objects.get(id=9)
# n_chat.delete()
n_chat, c_chat = ChatUser.objects.get_or_create(name="slava_1", chat_id=12321344, user_id=21321344)

print(n_chat)
print(c_chat)