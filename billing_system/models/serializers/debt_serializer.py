from rest_framework import serializers

from billing_system.models.debt import Debt


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = ['name', 'government_id', 'email', 'debt_amount', 'debt_due_date', 'debt_id']
