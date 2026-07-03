from django.db import models
from django.contrib.auth.models import User

class ClientReply(models.Model):
    TONE_CHOICES = [
        ('professional', 'Professional'),
        ('friendly', 'Friendly'),
        ('formal', 'Formal'),
        ('casual', 'Casual'),
        ('persuasive', 'Persuasive'),
        ('apologetic', 'Apologetic'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    
    # Input fields
    client_message = models.TextField()
    tone = models.CharField(max_length=20, choices=TONE_CHOICES, default='professional')
    
    # AI Generated reply
    generated_reply = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reply to {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-created_at']