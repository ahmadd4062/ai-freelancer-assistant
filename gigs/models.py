from django.db import models
from django.contrib.auth.models import User

class GigDescription(models.Model):
    EXPERIENCE_CHOICES = [
        ('entry', 'Entry Level'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs')
    
    # Input fields
    service_category = models.CharField(max_length=200)
    skills = models.TextField(help_text="Comma separated skills")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='intermediate')
    delivery_time = models.CharField(max_length=100)
    features = models.TextField(help_text="Key features of your service")
    revisions = models.IntegerField(default=1)
    
    # AI Generated content
    generated_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True, help_text="SEO keywords for your gig")
    faq_suggestions = models.TextField(blank=True, null=True, help_text="Suggested FAQs")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.service_category} - {self.user.username}"
    
    def get_skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    
    def get_features_list(self):
        if self.features:
            return [feature.strip() for feature in self.features.split(',')]
        return []
    
    class Meta:
        ordering = ['-created_at']