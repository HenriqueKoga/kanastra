import logging
import os

from django.core.files.uploadedfile import TemporaryUploadedFile
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from billing_system.settings import SHARED_FOLDER
from billing_system.tasks.debts_tasks import process_csv


class UploadCSVView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        csv_file: TemporaryUploadedFile = request.FILES['file']

        try:
            file_path = os.path.join(SHARED_FOLDER, csv_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            process_csv.delay(file_path)

            return Response({"message": "Started processing debts"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(f"Error processing debts: {e}")
            return Response({"error": "Error processing debts"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
