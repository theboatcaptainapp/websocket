from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    """owner, opponent, last_active"""
    name = models.CharField(max_length=100)
    last_active = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """conversation, sender, body"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200, default='')
    time_sent = models.DateTimeField(auto_now_add=True)
