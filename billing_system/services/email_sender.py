# billing/services/email_sender.py

import logging


class EmailSender:
    def send_email(self, email, subject, message):
        # Simulação de envio de e-mail
        logging.info(f"Sending email to {email}: {subject}")
        return True  # Retorne True se o envio for bem-sucedido
