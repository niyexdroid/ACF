
### legacy code.

from django import forms
from .models import *

class PrimaryUserForm(forms.ModelForm):
    class Meta:
        model = PrimaryUser
        fields = '__all__'

    def clean_full_name(self, *args, **kwargs):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 6:
            raise forms.ValidationError('Please enter your full name')
        return full_name

    def clean_phone(self, *args, **kwargs):
        phone = self.cleaned_data.get('phone')
        if len(phone) > 12 :
            raise forms.ValidationError('Please enter a valid phone number')
        return phone


class SecondaryUserForm(forms.ModelForm):
    class Meta:
        model = SecondaryUser
        fields = '__all__'
    
