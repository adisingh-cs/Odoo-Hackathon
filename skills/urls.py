from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('create/', views.skill_create, name='skill_create'),
    path('<int:skill_id>/', views.skill_detail, name='skill_detail'),
    path('<int:skill_id>/edit/', views.skill_edit, name='skill_edit'),
    path('<int:skill_id>/delete/', views.skill_delete, name='skill_delete'),
    path('<int:skill_id>/toggle/', views.skill_toggle_status, name='skill_toggle_status'),
    path('<int:skill_id>/reviews/', views.skill_reviews, name='skill_reviews'),
    path('my-skills/', views.my_skills, name='my_skills'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
] 