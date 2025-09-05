# ccapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

# Users ===============================
class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, phone=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, full_name, phone, password, **extra_fields)

class ChatUser(models.Model):
    name = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name    

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50, default='Manager')
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    chat_user = models.ForeignKey(ChatUser, on_delete=models.DO_NOTHING, related_name="chat_user_ref", null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

# Contracts ==========================
class Contract(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts_user')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
# Subcontractors ==============================
class Subcontractor(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="subcontractors"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Construction Sites ==============================
# class ConstructionSite(models.Model):
#     name = models.CharField(max_length=255)
#     contact_person = models.CharField(max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=50, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name="subcontractors"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# RFQs =============================================

class RFQ(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Relations
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rfqs_user")  
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE, related_name="rfqs_subcontractor")

    # Example field: estimated cost
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"RFQ {self.id} - {self.title}"
    

# Payments =======================================

class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING, related_name="rel_contract")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('checked', 'Checked'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    execute_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment {self.id} {self.contract}"
    
    #  Messages ======================================
    
    
class MessageList(models.Model):
    sender = models.ForeignKey(ChatUser, related_name="sent_messages", on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey(ChatUser, related_name="received_messages", on_delete=models.DO_NOTHING)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.text[:20]}"
    

    

