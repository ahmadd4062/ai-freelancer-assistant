from django.db import models
from django.contrib.auth.models import User

class CoverLetter(models.Model):
    TONE_CHOICES = [
        ('professional', 'Professional'),
        ('enthusiastic', 'Enthusiastic'),
        ('confident', 'Confident'),
        ('humble', 'Humble'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coverletters')
    
    # Input fields
    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    experience = models.TextField(help_text="Describe your relevant experience")
    skills = models.TextField(help_text="Comma separated skills")
    portfolio_url = models.URLField(blank=True, null=True)
    tone = models.CharField(max_length=20, choices=TONE_CHOICES, default='professional')
    
    # AI Generated content
    generated_content = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
    def get_skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    
    class Meta:
        ordering = ['-created_at']