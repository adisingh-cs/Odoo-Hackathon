from django import forms
from .models import Message, PlatformMessage


class MessageForm(forms.ModelForm):
    """Form for sending messages."""
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Type your message...',
                'class': 'form-control'
            }),
        }


class PlatformMessageForm(forms.ModelForm):
    """Form for creating platform messages (admin only)."""
    class Meta:
        model = PlatformMessage
        fields = ['title', 'content', 'message_type', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Message title...'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Message content...'}),
        } 