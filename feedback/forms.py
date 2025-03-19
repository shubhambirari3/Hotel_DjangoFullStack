from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'country', 'rating', 'comment', 'email']  # Added name and country
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name', 'class': 'form-control'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter your country', 'class': 'form-control'}),
            'rating': forms.RadioSelect(choices=[(i, f'⭐ {i}') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your feedback...', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'}),
        }
