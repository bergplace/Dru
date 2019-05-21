from django.urls import path

from api.views import as_view
from tasks import tasks
from . import views

urlpatterns = [
    path('result/<str:task_id>', views.result),
    path('register-email', views.register_email),
    path('current_block_height', views.current_block_height),
    path('get_blocks/<int:start_height>/<int:end_height>', as_view(tasks.get_blocks)),
    path('get_blocks_reduced/<int:start_height>/<int:end_height>', as_view(tasks.get_blocks_reduced)),
    path('get_edges/<int:start_height>/<int:end_height>', as_view(tasks.get_edges)),
    path('get_degree/<int:start_height>/<int:end_height>/<str:mode>', as_view(tasks.get_degree)),
    path('get_degree_by_block/<int:start_height>/<int:end_height>/<str:address>/<str:mode>',
         as_view(tasks.get_degree_by_block)),
    path('get_degree_max/<int:start_height>/<int:end_height>/<str:mode>', as_view(tasks.get_degree_max)),
    path('get_betweenness/<int:start_height>/<int:end_height>/<str:directed>', as_view(tasks.get_betweenness)),
    path('get_betweenness_max/<int:start_height>/<int:end_height>/<str:directed>', as_view(tasks.get_betweenness_max)),
    path('get_closeness/<int:start_height>/<int:end_height>/<str:directed>', as_view(tasks.get_closeness)),
    path('get_closeness_max/<int:start_height>/<int:end_height>/<str:directed>', as_view(tasks.get_closeness_max)),
    path('get_transitivity/<int:start_height>/<int:end_height>', as_view(tasks.get_transitivity)),
    path('get_transitivity_global/<int:start_height>/<int:end_height>', as_view(tasks.get_transitivity_global)),
    path('get_diameter/<int:start_height>/<int:end_height>/<str:directed>', as_view(tasks.get_diameter)),
    path('get_density/<int:start_height>/<int:end_height>/<str:directed>/<str:loops>', as_view(tasks.get_density)),
    path('are_connected/<int:start_height>/<int:end_height>/<str:address1>/<str:address2>/<str:directed>',
         as_view(tasks.are_connected)),
    path('get_transactions_value/<int:start_height>/<int:end_height>/<str:address1>/<str:address2>',
         as_view(tasks.get_transactions_value)),
]
