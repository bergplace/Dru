from django.urls import path
from . import views

urlpatterns = [
    path('result/<str:task_id>', views.result),
    path('block_by_height/<int:height>', views.get_block_by_height),
]