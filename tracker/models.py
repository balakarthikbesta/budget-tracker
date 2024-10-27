from django.db import models

# Create your models here.
from django.db import models

class Expense(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit')
    ]

    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES, default='debit')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.transaction_type})"
