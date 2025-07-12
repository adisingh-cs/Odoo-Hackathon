from django.contrib import admin
from .models import User, Skill, Swap, Feedback

class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'skill_type')
    list_filter = ('skill_type',)
    search_fields = ('name', 'tags')

class SwapAdmin(admin.ModelAdmin):
    list_display = ('requester', 'recipient', 'skill', 'status')
    list_filter = ('status',)
    actions = ['mark_completed']

    def mark_completed(self, request, queryset):
        queryset.update(status=Swap.COMPLETED)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('reviewee', 'rating', 'reviewer')
    list_filter = ('rating',)

admin.site.register(User)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Swap, SwapAdmin)
admin.site.register(Feedback, FeedbackAdmin)

from .models import Announcement

admin.site.register(Announcement)