from django.urls import path
from . import views

urlpatterns = [
    path('result/<str:task_id>', views.result),
    path('register-email', views.register_email),
    path('block_by_height/<int:height>', views.get_block_by_height),
    path('get_blocks_range/<int:start_height>/<int:end_height>', views.get_blocks_range),
    path('get_blocks_number/<int:start_height>/<int:num_of_blocks>', views.get_blocks_number),
    path('get_edges_range/<int:start_height>/<int:end_height>', views.get_edges_range),
    path('wait_n_seconds/<int:seconds>', views.wait_n_seconds)
]
