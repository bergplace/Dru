from django.urls import path
from . import views

urlpatterns = [
    path('last_block', views.last_block),
]