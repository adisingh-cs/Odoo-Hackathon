from django.contrib import admin
from .models import Category, SkillListing, SkillReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(SkillListing)
class SkillListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'skill_type', 'difficulty_level', 'is_active', 'status', 'created_at']
    list_filter = ['skill_type', 'difficulty_level', 'is_active', 'status', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__email', 'user__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SkillReview)
class SkillReviewAdmin(admin.ModelAdmin):
    list_display = ['skill_listing', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['skill_listing__title', 'reviewer__email', 'comment']
    ordering = ['-created_at']
    readonly_fields = ['created_at'] 