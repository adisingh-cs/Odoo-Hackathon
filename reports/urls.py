from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_create, name='report_create'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('my-reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('admin/', views.admin_reports, name='admin_reports'),
    path('admin/<int:report_id>/', views.admin_report_detail, name='admin_report_detail'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('activity/', views.user_activity_log, name='user_activity_log'),
    path('analytics/summary/', views.analytics_summary, name='analytics_summary'),
] 