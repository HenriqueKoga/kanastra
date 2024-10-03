from unittest.mock import MagicMock

import pytest

from billing_system.tasks.debts_tasks import process_debt


@pytest.fixture
def debt_serializer_mock(mocker):
    return mocker.patch('billing_system.tasks.debts_tasks.DebtSerializer')


@pytest.fixture
def debt_mock(mocker):
    return mocker.patch('billing_system.tasks.debts_tasks.Debt')


@pytest.fixture
def invoice_mock(mocker):
    return mocker.patch('billing_system.tasks.debts_tasks.Invoice')


@pytest.fixture
def bill_pdf_generator_mock(mocker):
    return mocker.patch('billing_system.tasks.debts_tasks.BillPDFGenerator')


@pytest.fixture
def email_sender_mock(mocker):
    return mocker.patch('billing_system.tasks.debts_tasks.EmailSenderSMTP')


def test_process_debt_creation(
    debt_serializer_mock: MagicMock,
    debt_mock: MagicMock,
    invoice_mock: MagicMock,
    bill_pdf_generator_mock: MagicMock,
    email_sender_mock: MagicMock
):
    debt_serializer_mock.return_value.is_valid.return_value = True
    debt_mock.objects.filter.return_value.first.return_value = None
    invoice_mock.objects.filter.return_value.first.return_value = None
    bill_pdf_generator_mock.generate_bill.return_value = True

    debt_data = {
        'name': 'Test User',
        'government_id': '123456789',
        'email': 'test@test.com',
        'debt_amount': 100.0,
        'debt_due_date': '2022-12-31',
        'debt_id': '123456'
    }
    process_debt(debt_data)

    debt_serializer_mock.assert_called_once_with(data=debt_data)
    debt_serializer_mock.return_value.is_valid.assert_called_once()
    debt_serializer_mock.return_value.save.assert_called_once()
    invoice_mock.objects.filter.assert_called_once_with(
        debt=debt_serializer_mock.return_value.save.return_value
    )
    bill_pdf_generator_mock.generate_bill.assert_called_once_with(
        debt_serializer_mock.return_value.save.return_value.debt_id
    )
    email_sender_mock.send_email.assert_called_once_with(
        debt_serializer_mock.return_value.save.return_value.email,
        "Billing",
        f'Hello {debt_serializer_mock.return_value.save.return_value.name}, your debt is {debt_serializer_mock.return_value.save.return_value.debt_amount}'
    )
