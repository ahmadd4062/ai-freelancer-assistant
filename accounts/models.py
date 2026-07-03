from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Professional Information
    skills = models.TextField(max_length=500, blank=True, null=True, help_text="Comma separated skills")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    portfolio_url = models.URLField(blank=True, null=True)
    
    # AI Credits (start with 100 free credits)
    ai_credits = models.IntegerField(default=100)
        
    # Theme preference
    theme = models.CharField(max_length=10, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])
    
    # Notification settings
    email_notifications = models.BooleanField(default=True)

    # API Key (for AI services)
    api_key = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []

# Signal to automatically create Profile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()