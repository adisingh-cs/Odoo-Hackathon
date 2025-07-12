from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    location = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='profiles/', blank=True)
    is_private = models.BooleanField(default=False)
    availability = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.username
    

class Skill(models.Model):
    OFFERED = 'OFF'
    WANTED = 'WAN'
    TYPE_CHOICES = [
        (OFFERED, 'Offered'),
        (WANTED, 'Wanted'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.get_skill_type_display()}: {self.name}"
    
class Swap(models.Model):
    PENDING = 'PEN'
    ACCEPTED = 'ACC'
    REJECTED = 'REJ'
    COMPLETED = 'COM'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
    ]
    requester = models.ForeignKey(User, related_name='sent_swaps', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_swaps', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.requester} -> {self.recipient} ({self.skill})"
    
class Feedback(models.Model):
    swap = models.OneToOneField(Swap, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewee = models.ForeignKey(User, related_name='feedbacks', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.rating} stars for {self.reviewee}"
    
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title