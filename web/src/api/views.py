from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main.models import Email
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
                    Response({
                        'error': True,
                        'error-msg': 'email not registered'
                    })
                try:
                    validate_email(email)
                    task.set_email(email)
                    return Response({'status': 'ok'})
                except ValidationError:
                    Response({
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
def get_block_by_height(request, height):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.get_block_by_height, height)
    return task_result_response(task_id)


@api_view(['GET'])
def wait_n_seconds(request, seconds):
    task_id = task_id_from_request(request)
    register_task(task_id, tasks.wait_n_seconds, seconds)
    return task_result_response(task_id)


