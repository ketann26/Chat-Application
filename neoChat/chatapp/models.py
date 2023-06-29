from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.sender.username}-{self.thread_name}' if self.sender else f'{self.message}-{self.thread_name}'
    
    def get_last_30_messages(self,thread_name):
        pass
