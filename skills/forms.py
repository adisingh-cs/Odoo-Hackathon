from django import forms
from .models import SkillListing, SkillReview, Category


class SkillListingForm(forms.ModelForm):
    """Form for creating and editing skill listings."""
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        required=False,
        help_text='Enter tags separated by commas (e.g., python, web development, django)'
    )
    
    class Meta:
        model = SkillListing
        fields = ['category', 'title', 'description', 'skill_type', 'difficulty_level', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_tags(self):
        """Convert comma-separated tags to list."""
        tags = self.cleaned_data.get('tags', '')
        if tags:
            # Split by comma, strip whitespace, and filter out empty strings
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            return tag_list
        return []


class SkillReviewForm(forms.ModelForm):
    """Form for creating skill reviews."""
    class Meta:
        model = SkillReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your experience with this skill...'}),
        }


class SkillSearchForm(forms.Form):
    """Form for searching skill listings."""
    query = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Search skills...'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    skill_type = forms.ChoiceField(
        choices=[('', 'All Types'), ('offer', 'Offering'), ('request', 'Requesting')],
        required=False
    )
    difficulty_level = forms.ChoiceField(
        choices=[('', 'All Levels'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')],
        required=False
    )
    min_rating = forms.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        required=False, 
        min_value=0, 
        max_value=5,
        widget=forms.NumberInput(attrs={'placeholder': 'Min rating'})
    ) 