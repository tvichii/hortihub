from  django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget= forms.SelectDateWidget())

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
