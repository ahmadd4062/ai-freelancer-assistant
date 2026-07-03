from django.db import models
from django.contrib.auth.models import User

class Proposal(models.Model):
    TONE_CHOICES = [
        ('professional', 'Professional'),
        ('casual', 'Casual'),
        ('friendly', 'Friendly'),
        ('persuasive', 'Persuasive'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    
    # Input fields
    client_name = models.CharField(max_length=200)
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    skills = models.TextField(help_text="Comma separated skills")
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    timeline = models.CharField(max_length=100)
    tone = models.CharField(max_length=20, choices=TONE_CHOICES, default='professional')
    
    # AI Generated content
    generated_content = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.project_title} - {self.client_name}"
    
    def get_skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    
    class Meta:
        ordering = ['-created_at']