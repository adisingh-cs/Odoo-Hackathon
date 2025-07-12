from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    """Conversations between users."""
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        participant_names = [user.get_full_name() or user.email for user in self.participants.all()]
        return f"Conversation: {' & '.join(participant_names)}"
    
    def get_other_participant(self, user):
        """Get the other participant in a two-person conversation."""
        return self.participants.exclude(id=user.id).first()


class Message(models.Model):
    """Individual messages in conversations."""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.email}: {self.content[:50]}..."


class PlatformMessage(models.Model):
    """Platform-wide announcements and messages."""
    MESSAGE_TYPES = [
        ('announcement', 'Announcement'),
        ('update', 'Platform Update'),
        ('maintenance', 'Maintenance Notice'),
        ('feature', 'New Feature'),
        ('general', 'General Message'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='announcement')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.message_type}"


class UserMessageRead(models.Model):
    """Track which users have read which platform messages."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='read_messages')
    platform_message = models.ForeignKey(PlatformMessage, on_delete=models.CASCADE, related_name='read_by')
    read_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'platform_message']
    
    def __str__(self):
        return f"{self.user.email} read {self.platform_message.title}" 