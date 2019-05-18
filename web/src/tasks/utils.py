from time import time
import json
from hashlib import sha256
import traceback

from rest_framework.response import Response

from tasks.netutils import get_max_height
from .models import Tasks
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def register_task(task_id, task_fn, *args, **kwargs):
    _, created = Tasks.objects.get_or_create(id=task_id)
    if created:
        logger.debug(f"accepted task {task_id} for processing")
        task_fn.delay(task_id, *args, **kwargs)

def task_id_from_request(request):
    return sha256((request.path + request.method + str(time())).encode('utf-8')).hexdigest()


def task_result_response(task_id):
    return Response({'result_url': Tasks.url(task_id)})


def save_task_result(task_id, result):
    with open(task_path(task_id), 'w') as f:
        f.write(json.dumps(result))


def get_task_result(task_id):
    with open(task_path(task_id), 'r') as f:
        return json.loads(f.read())


def task_path(task_id):
    return f"{settings.TASK_RESULTS_DIR}/{task_id}.json"


def auto_save_result(fn):
    def wrapper(task_id, *args, **kwargs):
        task = lambda: Tasks.objects.get(id=task_id)
        logger.debug(f"running task.{fn.__name__}, id: {task_id}")
        task().set_status(Tasks.PROCESSING).set_debug_info(
            task_name=fn.__name__, params=[args, kwargs]
        )
        try:
            result = fn(*args, **kwargs)
            save_task_result(task_id, result)
            task().set_status(Tasks.READY)
        except Exception as e:
            task().set_status(Tasks.ERROR).set_error_info(type(e).__name__, traceback.format_exc())
            raise
    wrapper.__name__ = fn.__name__ + "_asr"
    return wrapper


def heights_are_valid(start_height, end_height):
    return 0 <= start_height <= end_height <= get_max_height()
