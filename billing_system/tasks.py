import logging

from celery import shared_task

from .models import Debt, Invoice
from .services.bill_generator import BillGenerator
from .services.email_sender import EmailSender


@shared_task
def process_debt(debt_id):
    try:
        debt = Debt.objects.get(debt_id=debt_id)
        bill_generator = BillGenerator()
        email_sender = EmailSender()

        if bill_generator.generate_bill(debt_id):
            email_sender.send_email(debt.email, "Seu Boleto", f"Aqui está seu boleto no valor de {debt.debt_amount}.")
            Invoice.objects.create(debt=debt, status='sent')
    except Exception as e:
        logging.error(f"Error processing debt {debt_id}: {e}")
