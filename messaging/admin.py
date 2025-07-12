from django.contrib import admin
from .models import Conversation, Message, PlatformMessage, UserMessageRead


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'participants_display', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['participants__email', 'participants__username']
    ordering = ['-updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def participants_display(self, obj):
        return ', '.join([user.email for user in obj.participants.all()])
    participants_display.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'content_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__email', 'content', 'conversation__participants__email']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(PlatformMessage)
class PlatformMessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'message_type', 'is_active', 'created_by', 'created_at']
    list_filter = ['message_type', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'created_by__email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserMessageRead)
class UserMessageReadAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform_message', 'read_at']
    list_filter = ['read_at']
    search_fields = ['user__email', 'platform_message__title']
    ordering = ['-read_at']
    readonly_fields = ['read_at'] 