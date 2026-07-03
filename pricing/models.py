from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class PricingHistory(models.Model):
    COMPLEXITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    URGENCY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('very_urgent', 'Very Urgent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pricing_history')
    
    # Input fields
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_hours = models.DecimalField(max_digits=10, decimal_places=2)
    complexity = models.CharField(max_length=20, choices=COMPLEXITY_CHOICES, default='medium')
    urgency = models.CharField(max_length=20, choices=URGENCY_CHOICES, default='normal')
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # AI Suggestions
    suggested_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    recommended_delivery = models.CharField(max_length=100, blank=True, null=True)
    market_analysis = models.TextField(blank=True, null=True)
    service_tips = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Pricing - {self.user.username} - {self.created_at}"
    
    def calculate_base_price(self):
        """Calculate base price without AI"""
        return self.hourly_rate * self.estimated_hours
    
    def calculate_complexity_multiplier(self):
        multipliers = {'low': 1.0, 'medium': 1.3, 'high': 1.6}
        return multipliers.get(self.complexity, 1.0)
    
    def calculate_urgency_multiplier(self):
        multipliers = {'normal': 1.0, 'urgent': 1.2, 'very_urgent': 1.5}
        return multipliers.get(self.urgency, 1.0)
    
    def calculate_suggested_price(self):
        """Calculate suggested price with multipliers"""
        base = self.calculate_base_price()
        complexity_mult = self.calculate_complexity_multiplier()
        urgency_mult = self.calculate_urgency_multiplier()
        total = (base * complexity_mult * urgency_mult) + self.additional_charges + self.tax
        return total
    
    class Meta:
        ordering = ['-created_at']