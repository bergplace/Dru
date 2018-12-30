from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tasks.utils import register_task, task_id_from_request, task_result_response, get_task_result
from tasks.models import Tasks
import tasks.tasks as tasks


@api_view(['GET'])
def result(request, task_id):
    if Tasks.objects.filter(id=task_id).exists():
        task = Tasks.objects.get(id=task_id)
        if task.status != Tasks.READY:
            return Response({'ready': False, 'status': task.status})
        else:
            return Response({
                'ready': True,
                'status': task.status,
                'data': get_task_result(task_id)
            })
    raise Http404()


@api_view(['GET'])
def get_block_by_height(request, height):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_block_by_height, height)
    return task_result_response(task_id)


