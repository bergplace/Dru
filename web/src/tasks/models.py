from django.db import models


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
