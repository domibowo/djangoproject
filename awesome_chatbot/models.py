from django.db import models

# Create your models here.
class ChatBotModel(models.Model):
    message_request = models.TextField()
    bot_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']