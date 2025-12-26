import uuid
from django.db import models
from django.utils import timezone



class Conversation(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField('accounts.Profile')
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey( Conversation,related_name='messages',on_delete=models.CASCADE )
    sender       = models.ForeignKey( 'accounts.Profile',on_delete=models.CASCADE )
    body         = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']



class MessageRead(models.Model):
    message = models.ForeignKey( Message,related_name='reads',on_delete=models.CASCADE )
    profile = models.ForeignKey( 'accounts.Profile',on_delete=models.CASCADE )
    read_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('message', 'profile')





