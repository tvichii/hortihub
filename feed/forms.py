from .models import UserPost
from django.forms import ModelForm, Textarea


class UserPostForm(ModelForm):
    # content = CharField(widget=forms.Textarea, label='')

    class Meta:
        model = UserPost
        fields = ['post_body', 'image']
        widgets = {'post_body': Textarea(attrs={'rows': 4, 'cols': 65}),
       }
