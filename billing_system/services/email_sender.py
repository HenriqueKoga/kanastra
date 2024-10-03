import logging
from abc import ABC, abstractmethod


class EmailSender(ABC):

    @classmethod
    @abstractmethod
    def send_email(cls, email: str, subject: str, message: str) -> bool:
        pass


class EmailSenderSMTP(EmailSender):

    @classmethod
    def send_email(cls, email: str, subject: str, message: str) -> bool:
        logging.info(f"Sending email to {email} - {subject}:{message}")
        return True
