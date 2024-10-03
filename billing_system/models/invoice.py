from django.db import models

from billing_system.models.commons import NoPrefixOnTableName
from billing_system.models.debt import Debt


class InvoiceStatus(models.TextChoices):
    PENDING = 'pending'
    SENT = 'sent'
    PAID = 'paid'


class Invoice(models.Model, metaclass=NoPrefixOnTableName):

    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending', choices=InvoiceStatus.choices)

    def __str__(self):
        return f"Invoice {self.debt.name} - Status: {self.status}"
