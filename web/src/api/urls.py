from django.urls import path
from . import views

urlpatterns = [
    path('result/<str:task_id>', views.result),
    path('register-email', views.register_email),
    path('block_by_height/<int:height>', views.get_block_by_height),
    path('current_block_height', views.current_block_height),
    path('get_blocks/<int:start_height>/<int:end_height>', views.get_blocks),
    path('get_blocks_reduced/<int:start_height>/<int:end_height>', views.get_blocks_reduced),
    path('get_edges/<int:start_height>/<int:end_height>', views.get_edges),
    path('get_degree/<int:start_height>/<int:end_height>/<str:mode>', views.get_degree),
    path('get_degree_max/<int:start_height>/<int:end_height>/<str:mode>', views.get_degree_max),
    path('get_betweenness/<int:start_height>/<int:end_height>/<str:directed>', views.get_betweenness),
    path('get_betweenness_max/<int:start_height>/<int:end_height>/<str:directed>', views.get_betweenness_max),
    path('get_closeness/<int:start_height>/<int:end_height>/<str:directed>', views.get_closeness),
    path('get_closeness_max/<int:start_height>/<int:end_height>/<str:directed>', views.get_closeness_max),
    path('get_transitivity/<int:start_height>/<int:end_height>', views.get_transitivity),
    path('wait_n_seconds/<int:seconds>', views.wait_n_seconds)
]
