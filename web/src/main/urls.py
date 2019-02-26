from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('verify-email/<slug:verification_str>', views.verify_email),
]