import uuid

from django.db import models


class Debt(models.Model):
    name = models.CharField(max_length=255)
    government_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    debt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    debt_due_date = models.DateField()
    debt_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.name} - {self.debt_amount}"


class Invoice(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Invoice {self.debt.name} - Status: {self.status}"
