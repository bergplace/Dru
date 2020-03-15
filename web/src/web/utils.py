from django.core.mail import EmailMessage
from django.conf import settings


def send_mail(recipient, subject, msg):
    EmailMessage(
        subject,
        msg,
        settings.EMAIL_ADDRESS,
        [recipient],
        [],
        reply_to=[settings.EMAIL_REPLY_TO_ADDRESS],
    ).send()
