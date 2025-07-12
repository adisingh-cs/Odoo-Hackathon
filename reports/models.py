from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Report(models.Model):
    """User reports for various issues."""
    REPORT_TYPES = [
        ('user', 'User Report'),
        ('skill', 'Skill Listing Report'),
        ('swap', 'Swap Report'),
        ('message', 'Message Report'),
        ('platform', 'Platform Issue'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('investigating', 'Under Investigation'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_filed')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_resolved')
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Related object fields (optional)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reports_received')
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reporter.email} - {self.title} ({self.status})"


class Analytics(models.Model):
    """Daily analytics data."""
    date = models.DateField(unique=True)
    total_users = models.PositiveIntegerField(default=0)
    active_users = models.PositiveIntegerField(default=0)
    new_users = models.PositiveIntegerField(default=0)
    total_skills = models.PositiveIntegerField(default=0)
    new_skills = models.PositiveIntegerField(default=0)
    total_swaps = models.PositiveIntegerField(default=0)
    completed_swaps = models.PositiveIntegerField(default=0)
    total_messages = models.PositiveIntegerField(default=0)
    total_reports = models.PositiveIntegerField(default=0)
    pending_reports = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Analytics'
    
    def __str__(self):
        return f"Analytics for {self.date}"


class UserActivity(models.Model):
    """User activity logs."""
    ACTIVITY_TYPES = [
        ('login', 'User Login'),
        ('register', 'User Registration'),
        ('skill_create', 'Skill Created'),
        ('skill_edit', 'Skill Edited'),
        ('skill_delete', 'Skill Deleted'),
        ('swap_request', 'Swap Request Created'),
        ('swap_accept', 'Swap Request Accepted'),
        ('swap_reject', 'Swap Request Rejected'),
        ('swap_complete', 'Swap Completed'),
        ('message_sent', 'Message Sent'),
        ('review_posted', 'Review Posted'),
        ('report_filed', 'Report Filed'),
        ('profile_update', 'Profile Updated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.email} - {self.activity_type} - {self.created_at}" 