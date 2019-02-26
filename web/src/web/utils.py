from django.core.mail import EmailMessage


def send_mail(recipient, subject, msg):
    EmailMessage(
        subject,
        msg,
        'dru@bergplace.org',
        [recipient],
        [],
        reply_to=['dru-support@bergplace.org'],
    ).send()
