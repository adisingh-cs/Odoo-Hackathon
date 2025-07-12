from django.contrib import admin
from .models import SwapRequest, SwapTransaction, SwapReview


@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ['requesting_user', 'requested_user', 'requesting_skill', 'requested_skill', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['requesting_user__email', 'requested_user__email', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'accepted_at', 'completed_at']


@admin.register(SwapTransaction)
class SwapTransactionAdmin(admin.ModelAdmin):
    list_display = ['swap_request', 'start_date', 'end_date', 'actual_duration', 'created_at']
    list_filter = ['start_date', 'end_date', 'created_at']
    search_fields = ['swap_request__requesting_user__email', 'swap_request__requested_user__email', 'notes']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(SwapReview)
class SwapReviewAdmin(admin.ModelAdmin):
    list_display = ['swap_request', 'reviewer', 'reviewed_user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['swap_request__requesting_user__email', 'swap_request__requested_user__email', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['created_at'] 