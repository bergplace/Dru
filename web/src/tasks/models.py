from django.conf import settings
from django.db import models

from web.utils import send_mail


class Tasks(models.Model):
    QUEUED = 'queued'
    PROCESSING = 'processing'
    READY = 'ready'
    ERROR = 'error'

    id = models.TextField(primary_key=True)
    status = models.CharField(
        choices=(
            (QUEUED, 'queued'),
            (PROCESSING, 'processing'),
            (READY, 'ready'),
            (ERROR, 'error'),
        ),
        default=QUEUED,
        max_length=14
    )
    email = models.EmailField(null=True)
    received_t = models.DateTimeField(auto_now_add=True)
    processing_start_t = models.DateTimeField(null=True)
    end_t = models.DateTimeField(null=True)

    def set_status(self, status):
        self.status = status
        self.save()
        self.send_email()

    def set_email(self, email):
        self.email = email
        self.save()
        self.send_email()

    def send_email(self):
        if self.email:
            if self.status is not Tasks.READY:
                send_mail(
                    self.email,
                    f'DRU Task changed state to {self.status}',
                    f'DRU Task with id {self.id} changed state to {self.status}'
                )
            else:
                send_mail(
                    self.email,
                    f'DRU Task finnished!',
                    f'DRU Task with id {self.id} changed state to READY, link to result: {Tasks.url(self.id)}'
                )

    @staticmethod
    def url(task_id):
        return f"{settings.BASE_URL}/api/result/{task_id}"
