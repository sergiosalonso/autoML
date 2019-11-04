from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from ml_core import models

class ProcessForm(forms.ModelForm):
    class Meta:
        fields = ('title','description')
        model = models.Process
#Customization
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['slug'].label = "Email Address"
        self.fields['description'].label = "Description"
