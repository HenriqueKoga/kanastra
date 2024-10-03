from billing_system.services.bill_generator import BillPDFGenerator


def test_generate_bill():
    assert BillPDFGenerator.generate_bill('123')
