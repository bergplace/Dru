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

    @classmethod
    def is_registered(cls, email):
        return cls.objects.filter(hash=cls.email_hash(email)).exists()

    @classmethod
    def email_hash(cls, email):
        return hashlib.sha256(email.encode('utf-8')).hexdigest()
