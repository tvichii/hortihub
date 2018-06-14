from  django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.forms.fields import DateField

class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email' ]

class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget = forms.SelectDateWidget())

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']