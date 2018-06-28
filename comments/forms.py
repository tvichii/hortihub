from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Comment
        fields = ['content_type', 'object_id', 'content']  # list of fields you want from model
        widgets = {'content_type': forms.HiddenInput(), 'object_id': forms.HiddenInput(),
       }
