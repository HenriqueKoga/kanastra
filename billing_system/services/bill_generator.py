import logging
from abc import ABC, abstractmethod


class BillGenerator(ABC):
    @classmethod
    @abstractmethod
    def generate_bill(cls, debt_id: str) -> bool:
        pass


class BillPDFGenerator(BillGenerator):

    @classmethod
    def generate_bill(cls, debt_id: str) -> bool:
        logging.info(f'Generating PDF bill for debt_id: {debt_id}')
        return True
