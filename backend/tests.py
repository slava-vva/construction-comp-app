import os
import django

# 1. Tell Django which settings to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ccback.settings")

# 2. Setup Django
django.setup()

# 3. Now you can import models
from ccapp.models import ChatUser

print("Hi Django from script")

for u in ChatUser.objects.all():
    print(u.id, u.chat_id, u.name, u.created_at)

