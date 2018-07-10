from django.forms import ModelForm, Textarea, CharField, HiddenInput
from .models import Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
       #  fields = ['content_type', 'object_id', 'content']  # list of fields you want from model
       #  widgets = {'content_type':  HiddenInput(), 'object_id': HiddenInput(),
       #      'content': Textarea(attrs={'rows': 4, 'cols': 65}),
       # }
        fields = ['content']  # list of fields you want from model
        widgets = {
             'content': Textarea(attrs={'rows': 4, 'cols': 65}),
        }
