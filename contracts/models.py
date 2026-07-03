from django.db import models
from django.contrib.auth.models import User

class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts')
    
    # Client Details
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    client_company = models.CharField(max_length=200, blank=True, null=True)
    
    # Freelancer Details
    freelancer_name = models.CharField(max_length=200)
    freelancer_email = models.EmailField()
    
    # Project Details
    project_title = models.CharField(max_length=200)
    project_scope = models.TextField()
    timeline = models.CharField(max_length=200)
    
    # Financial Terms
    payment_terms = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Terms & Conditions
    terms_conditions = models.TextField()
    
    # AI Generated Contract
    generated_contract = models.TextField(blank=True, null=True)
    
    # Contract Number
    contract_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Dates
    created_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Status
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent to Client'),
        ('signed', 'Signed'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generate contract number if not set
        if not self.contract_number:
            import datetime
            year = datetime.datetime.now().year
            count = Contract.objects.filter(created_at__year=year).count() + 1
            self.contract_number = f"CTR-{year}-{count:04d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.contract_number} - {self.client_name}"
    
    class Meta:
        ordering = ['-created_at']