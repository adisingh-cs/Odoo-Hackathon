from django.urls import path
from . import views

app_name = 'swaps'

urlpatterns = [
    path('', views.swap_list, name='swap_list'),
    path('create/<int:skill_id>/', views.swap_request_create, name='swap_request_create'),
    path('<int:swap_id>/', views.swap_detail, name='swap_detail'),
    path('<int:swap_id>/accept/', views.swap_accept, name='swap_accept'),
    path('<int:swap_id>/reject/', views.swap_reject, name='swap_reject'),
    path('<int:swap_id>/complete/', views.swap_complete, name='swap_complete'),
    path('<int:swap_id>/cancel/', views.swap_cancel, name='swap_cancel'),
    path('sent/', views.sent_requests, name='sent_requests'),
    path('received/', views.received_requests, name='received_requests'),
] 