from django.shortcuts import render

from api.models import Email


def index(request):
    return render(request, 'main/index.html')


def verify_email(request, verification_str):
    updated = Email.objects.filter(verification_string=verification_str).update(verified=True)
    return render(request, 'main/email-verified.html')
