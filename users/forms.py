from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    location = forms.CharField(max_length=100, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'location', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    class Meta:
        model = UserProfile
        fields = ['phone', 'website', 'social_media', 'preferences', 'date_of_birth']
        widgets = {
            'social_media': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter as JSON: {"twitter": "handle", "linkedin": "profile"}'}),
            'preferences': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter as JSON: {"notifications": true, "privacy": "public"}'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class UserUpdateForm(forms.ModelForm):
    """Form for updating user basic information."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'location', 'profile_picture']


class UserSearchForm(forms.Form):
    """Form for searching users."""
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search by name, email, or location...'}))
    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Filter by location...'}))
    min_rating = forms.DecimalField(max_digits=3, decimal_places=2, required=False, min_value=0, max_value=5)
    verified_only = forms.BooleanField(required=False, initial=False) 