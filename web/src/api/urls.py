from django.urls import path
from . import views

urlpatterns = [
    path('result/<str:task_id>', views.result),
    path('register-email', views.register_email),
    path('block_by_height/<int:height>', views.get_block_by_height),
    path('wait_n_seconds/<int:seconds>', views.wait_n_seconds)
]
