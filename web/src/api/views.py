from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.models import Email
from tasks.netutils import get_max_height
from tasks.utils import register_task, task_id_from_request, task_result_response, get_task_result
from tasks.models import Tasks
import tasks.tasks as tasks
from web.settings import BASE_URL
from web.utils import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


@api_view(['GET', 'POST'])
def result(request, task_id):
    if Tasks.objects.filter(id=task_id).exists():
        task = Tasks.objects.get(id=task_id)

        if request.method == 'GET':
            if task.status != Tasks.READY:
                return Response({'ready': False, 'status': task.status})
            else:
                return Response({
                    'ready': True,
                    'status': task.status,
                    'data': get_task_result(task_id)
                })
        if request.method == 'POST':
            if 'email' in request.data:
                email = request.data['email']
                if not Email.is_registered(email):
                    return Response({
                        'error': True,
                        'error-msg': 'email not registered'
                    })
                try:
                    validate_email(email)
                    task.set_email(email)
                    return Response({'status': 'ok'})
                except ValidationError:
                    return Response({
                        'error': True,
                        'error-msg': 'email is not valid'
                    })
            else:
                return Response({
                    'error': True,
                    'error-msg': 'email not specified'
                })
    raise Http404()


@api_view(['POST'])
def register_email(request):
    if 'email' in request.data:
        obj, created = Email.objects.get_or_create(hash=Email.email_hash(request.data['email']))
        if obj.verification_emails_sent > 10:
            return Response({
                'state': 'error',
                'msg': "we've sent verification email 10 times already and we'll sent no more!"
            })
        if (obj.verification_emails_sent
                and timezone.now() < obj.last_verification_email_sent_time + timedelta(seconds=10)):
            return Response({
                'state': 'error',
                'msg': "we've sent verification email less than 10 seconds ago already"
            })
        send_mail(
            request.data['email'],
            'Email Verification',
            f'{BASE_URL}/verify-email/{obj.verification_string}'
        )
        obj.verification_emails_sent += 1
        obj.save()
        if created:
            return Response({'state': 'ok', 'msg': 'verification email sent'})
        return Response({'state': 'ok', 'msg': 'verification email resent'})
    else:
        return Response({'state': 'error', 'msg': 'no variable email in post request'})

@api_view(['GET'])
def current_block_height(request):
    return Response({'height': get_max_height()})

@api_view(['GET'])
def get_block_by_height(request, height):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_block_by_height, height)
    return task_result_response(task_id)

@api_view(['GET'])
def get_blocks(request, start_height, end_height):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_blocks, start_height, end_height)
    return task_result_response(task_id)

@api_view(['GET'])
def get_blocks_reduced(request, start_height, end_height):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_blocks_reduced, start_height, end_height)
    return task_result_response(task_id)

@api_view(['GET'])
def get_edges(request, start_height, end_height):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_edges, start_height, end_height)
    return task_result_response(task_id)

@api_view(['GET'])
def get_degree(request, start_height, end_height, mode):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_degree, start_height, end_height, mode)
    return task_result_response(task_id)

@api_view(['GET'])
def get_degree_by_block(request, start_height, end_height, address, mode):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_degree_by_block, start_height, end_height, address, mode)
    return task_result_response(task_id)

@api_view(['GET'])
def get_degree_max(request, start_height, end_height, mode):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_degree_max, start_height, end_height, mode)
    return task_result_response(task_id)

@api_view(['GET'])
def get_betweenness(request, start_height, end_height, directed):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_betweenness, start_height, end_height, directed)
    return task_result_response(task_id)

@api_view(['GET'])
def get_betweenness_max(request, start_height, end_height, directed):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_betweenness_max, start_height, end_height, directed)
    return task_result_response(task_id)

@api_view(['GET'])
def get_closeness(request, start_height, end_height, directed):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_closeness, start_height, end_height, directed)
    return task_result_response(task_id)

@api_view(['GET'])
def get_closeness_max(request, start_height, end_height, directed):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_closeness_max, start_height, end_height, directed)
    return task_result_response(task_id)

@api_view(['GET'])
def get_transitivity(request, start_height, end_height):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_transitivity, start_height, end_height)
    return task_result_response(task_id)

@api_view(['GET'])
def get_transitivity_global(request, start_height, end_height):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_transitivity_global, start_height, end_height)
    return task_result_response(task_id)

@api_view(['GET'])
def get_diameter(request, start_height, end_height, directed):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_diameter, start_height, end_height, directed)
    return task_result_response(task_id)

@api_view(['GET'])
def get_density(request, start_height, end_height, directed, loops):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_density, start_height, end_height, directed, loops)
    return task_result_response(task_id)

@api_view(['GET'])
def are_connected(request, start_height, end_height, address1, address2, directed):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.are_connected, start_height, end_height, address1, address2, directed)
    return task_result_response(task_id)

@api_view(['GET'])
def get_transactions_value(request, start_height, end_height, address1, address2):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_transactions_value, start_height, end_height, address1, address2)
    return task_result_response(task_id)

@api_view(['GET'])
def wait_n_seconds(request, seconds):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.wait_n_seconds, seconds)
    return task_result_response(task_id)
