import logging

import pandas as pd
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Debt
from .serializers import DebtSerializer
from .tasks import process_debt


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer

    def create(self, request, *args, **kwargs):
        # Processar arquivo CSV
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            debt_id = row['debtId']
            # Verificar se o débito já existe
            if not Debt.objects.filter(debt_id=debt_id).exists():
                serializer = self.get_serializer(data=row)
                if serializer.is_valid():
                    serializer.save()
                    # Enfileirar tarefa para processamento do débito
                    process_debt.delay(debt_id)
            else:
                # Log para evitar duplicação
                logging.warning(f"Debt with ID {debt_id} already exists, skipping.")

        return Response({"message": "Debts processed."}, status=status.HTTP_201_CREATED)
