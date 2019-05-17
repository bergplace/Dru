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
    path('get_degree_by_block/<int:start_height>/<int:end_height>/<str:address>/<str:mode>', views.get_degree_by_block),
    path('get_degree_max/<int:start_height>/<int:end_height>/<str:mode>', views.get_degree_max),
    path('get_betweenness/<int:start_height>/<int:end_height>/<str:directed>', views.get_betweenness),
    path('get_betweenness_max/<int:start_height>/<int:end_height>/<str:directed>', views.get_betweenness_max),
    path('get_closeness/<int:start_height>/<int:end_height>/<str:directed>', views.get_closeness),
    path('get_closeness_max/<int:start_height>/<int:end_height>/<str:directed>', views.get_closeness_max),
    path('get_transitivity/<int:start_height>/<int:end_height>', views.get_transitivity),
    path('get_transitivity_global/<int:start_height>/<int:end_height>', views.get_transitivity_global),
    path('get_diameter/<int:start_height>/<int:end_height>/<str:directed>', views.get_diameter),
    path('get_density/<int:start_height>/<int:end_height>/<str:directed>/<str:loops>', views.get_density),
    path('are_connected/<int:start_height>/<int:end_height>/<str:address1>/<str:address2>/<str:directed>',
         views.are_connected),
    path('get_transactions_value/<int:start_height>/<int:end_height>/<str:address1>/<str:address2>',
         views.get_transactions_value),
    path('wait_n_seconds/<int:seconds>', views.wait_n_seconds)
]
