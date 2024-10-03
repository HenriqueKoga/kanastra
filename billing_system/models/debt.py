from django.db import models

from billing_system.models.commons import NoPrefixOnTableName


class Debt(models.Model, metaclass=NoPrefixOnTableName):
    name = models.CharField(max_length=255)
    government_id = models.CharField(max_length=20)
    email = models.EmailField()
    debt_amount = models.DecimalField(max_digits=10, decimal_places=2)
    debt_due_date = models.DateField()
    debt_id = models.CharField(unique=True, db_index=True, primary_key=True)

    def __str__(self):
        return f"{self.name} - {self.debt_amount}"
