from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from skills.models import SkillListing

User = get_user_model()


class SwapRequest(models.Model):
    """Swap requests between users."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    requesting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swap_requests_sent')
    requested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swap_requests_received')
    requesting_skill = models.ForeignKey(SkillListing, on_delete=models.CASCADE, related_name='swap_requests_as_offered')
    requested_skill = models.ForeignKey(SkillListing, on_delete=models.CASCADE, related_name='swap_requests_as_requested')
    message = models.TextField(blank=True)
    proposed_duration = models.PositiveIntegerField(help_text='Duration in hours')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.requesting_user.email} → {self.requested_user.email} - {self.status}"
    
    def save(self, *args, **kwargs):
        # Update accepted_at when status changes to accepted
        if self.status == 'accepted' and not self.accepted_at:
            from django.utils import timezone
            self.accepted_at = timezone.now()
        super().save(*args, **kwargs)


class SwapTransaction(models.Model):
    """Completed swap transactions."""
    swap_request = models.OneToOneField(SwapRequest, on_delete=models.CASCADE, related_name='transaction')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    actual_duration = models.PositiveIntegerField(help_text='Actual duration in hours')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction for {self.swap_request}"


class SwapReview(models.Model):
    """Reviews for completed swaps."""
    swap_request = models.ForeignKey(SwapRequest, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swap_reviews_given')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swap_reviews_received')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['swap_request', 'reviewer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reviewer.email} → {self.reviewed_user.email} - {self.rating} stars" 