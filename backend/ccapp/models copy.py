from django.db import models

class User(models.Model):  # ← This is essential
    id = models.CharField(primary_key=True, max_length=100)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50, default='Manager')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
