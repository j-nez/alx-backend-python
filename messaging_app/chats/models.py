import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'

    userid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    #first_name = models.CharField(max_length=20)
    #last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
    created_at= models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
    related_name='sent_messages')
    message_body = models.TextField()
    sent_At = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name ='coversations')
    created_at = models.DateTimeField(auto_now_add=True)