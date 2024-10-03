from billing_system.services.email_sender import EmailSenderSMTP


def test_send_email():
    assert EmailSenderSMTP.send_email('email_mock', 'subject_mock', 'message_mock')
