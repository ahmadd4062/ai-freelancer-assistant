from django.db import models
from django.contrib.auth.models import User

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    
    # Client Details
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    client_address = models.TextField(blank=True, null=True)
    
    # Project Details
    project_title = models.CharField(max_length=200)
    project_description = models.TextField()
    
    # Services
    services = models.TextField(help_text="List of services provided")
    
    # Financial Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Dates
    due_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Invoice number (auto-generated)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate total amount
        self.total_amount = self.amount + self.tax
        
        # Generate invoice number if not set
        if not self.invoice_number:
            import datetime
            year = datetime.datetime.now().year
            count = Invoice.objects.filter(created_at__year=year).count() + 1
            self.invoice_number = f"INV-{year}-{count:04d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.invoice_number} - {self.client_name}"
    
    class Meta:
        ordering = ['-created_at']