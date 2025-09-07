from ccapp.models import ChatUser

print("Hi Django from script")

for u in ChatUser.objects.all():
    print(u.id, u.chat_id, u.name, u.created_at)
