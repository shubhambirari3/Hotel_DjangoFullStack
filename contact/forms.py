from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Message', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            # For authenticated users, set name and email as read-only with profile values
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['name'].initial = self.user.get_full_name()
            self.fields['email'].initial = self.user.email
        else:
            # For non-authenticated users, make all fields editable and required
            self.fields['name'].required = True
            self.fields['email'].required = True