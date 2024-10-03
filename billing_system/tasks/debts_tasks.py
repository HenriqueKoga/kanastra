import logging
import os
from concurrent.futures import ThreadPoolExecutor, wait

import pandas as pd

from billing_system.infrastructure.celery import app as celery_app
from billing_system.models.debt import Debt
from billing_system.models.invoice import Invoice, InvoiceStatus
from billing_system.models.serializers.debt_serializer import DebtSerializer
from billing_system.services.bill_generator import BillPDFGenerator
from billing_system.services.email_sender import EmailSenderSMTP


@celery_app.task
def process_debt(debt_data: dict):
    try:
        debt_id = debt_data['debt_id']

        serializer = DebtSerializer(data=debt_data)
        debt = Debt.objects.filter(debt_id=debt_id).first()

        if not debt:
            if serializer.is_valid():
                debt = serializer.save()
            else:
                logging.error(f"Error processing debt {debt_id}: {serializer.errors}")
                return

        invoice = Invoice.objects.filter(debt=debt).first()
        if invoice and invoice.status == InvoiceStatus.SENT:
            logging.info(f"Invoice for debt {debt_id} already exists")
            return

        if BillPDFGenerator.generate_bill(debt.debt_id):
            EmailSenderSMTP.send_email(debt.email, "Billing", f'Hello {debt.name}, your debt is {debt.debt_amount}')
            Invoice.objects.create(debt=debt, status=InvoiceStatus.SENT)
    except Exception as e:
        logging.error(f"Error processing debt {debt_id}: {e}")


@celery_app.task
def process_csv(file_path: str):
    if os.path.exists(file_path):
        rows = pd.read_csv(file_path, sep=',').to_dict('records')
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [
                executor.submit(process_debt.delay, {
                    'name': row['name'],
                    'government_id': row['governmentId'],
                    'email': row['email'],
                    'debt_amount': row['debtAmount'],
                    'debt_due_date': row['debtDueDate'],
                    'debt_id': row['debtId']
                })
                for row in rows
            ]

            logging.info('Waiting for tasks to complete...')
            wait(futures)
            logging.info('Tasks completed')
            os.remove(file_path)
    else:
        logging.error(f"File {file_path} not found")
        return
