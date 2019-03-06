import hashlib

from django.db import models

from api.utils import randhex256


class Email(models.Model):
    hash = models.CharField(primary_key=True, max_length=64)
    verified = models.BooleanField(default=False)
    verification_string = models.CharField(
        max_length=256,
        default=randhex256,
        db_index=True,
    )
    verification_emails_sent = models.IntegerField(default=0)
    last_verification_email_sent_time = models.DateTimeField(auto_now=True)

    @classmethod
    def is_registered(cls, email):
        return cls.objects.filter(hash=cls.email_hash(email), verified=True).exists()

    @classmethod
    def email_hash(cls, email):
        return hashlib.sha256(email.encode('utf-8')).hexdigest()
