from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    """Form for creating reports."""
    class Meta:
        model = Report
        fields = ['report_type', 'title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Brief description of the issue...'}),
            'description': forms.Textarea(attrs={
                'rows': 5, 
                'placeholder': 'Please provide detailed information about the issue...'
            }),
        }


class ReportAdminForm(forms.ModelForm):
    """Form for admin to update reports."""
    class Meta:
        model = Report
        fields = ['status', 'admin_notes']
        widgets = {
            'admin_notes': forms.Textarea(attrs={'rows': 4}),
        } 