from django import forms
from .models import SwapRequest, SwapReview, SwapTransaction


class SwapRequestForm(forms.ModelForm):
    """Form for creating swap requests."""
    class Meta:
        model = SwapRequest
        fields = ['requested_skill', 'message', 'proposed_duration']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Explain why you want to swap and any specific details...'}),
            'proposed_duration': forms.NumberInput(attrs={'min': 1, 'max': 24, 'placeholder': 'Duration in hours'}),
        }
    
    def __init__(self, *args, **kwargs):
        requesting_skill = kwargs.pop('requesting_skill', None)
        super().__init__(*args, **kwargs)
        
        if requesting_skill:
            # Filter requested_skill choices to exclude the user's own skills
            self.fields['requested_skill'].queryset = requesting_skill.user.skill_listings.filter(
                is_active=True, 
                skill_type='offer'
            ).exclude(id=requesting_skill.id)


class SwapReviewForm(forms.ModelForm):
    """Form for creating swap reviews."""
    class Meta:
        model = SwapReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your experience with this swap...'}),
        }


class SwapTransactionForm(forms.ModelForm):
    """Form for creating swap transactions."""
    class Meta:
        model = SwapTransaction
        fields = ['start_date', 'end_date', 'actual_duration', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'actual_duration': forms.NumberInput(attrs={'min': 1, 'max': 24}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any notes about the swap session...'}),
        } 