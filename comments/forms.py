from django import forms
from .models import Comment
# class CommentForm(forms.Form):
#     content_type = forms.CharField(widget=forms.HiddenInput)
#     object_id = forms.IntegerField(widget=forms.HiddenInput)
#     #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
#     content = forms.CharField(label='', widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='')
    class Meta:
        model = Comment
        fields = ['content_type','object_id', 'content'] # list of fields you want from model
        widgets = {'content_type': forms.HiddenInput(),'object_id': forms.HiddenInput(),
       }