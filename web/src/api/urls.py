from django.urls import path
from . import views

urlpatterns = [
    path('result/<str:task_id>', views.result),
    path('register-email', views.register_email),
    path('block_by_height/<int:height>', views.get_block_by_height),
    path('get_blocks/<int:start_height>/<int:end_height>', views.get_blocks),
    path('get_blocks_reduced/<int:start_height>/<int:end_height>', views.get_blocks_reduced),
    path('get_edges/<int:start_height>/<int:end_height>', views.get_edges),
    path('get_max_degree/<int:start_height>/<int:end_height>', views.get_max_degree),
    path('wait_n_seconds/<int:seconds>', views.wait_n_seconds)
]
