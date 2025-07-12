from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<int:conversation_id>/read/', views.mark_conversation_read, name='mark_conversation_read'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('platform/', views.platform_messages, name='platform_messages'),
    path('platform/<int:message_id>/', views.platform_message_detail, name='platform_message_detail'),
    path('platform/create/', views.create_platform_message, name='create_platform_message'),
    path('unread-count/', views.get_unread_count, name='get_unread_count'),
] 