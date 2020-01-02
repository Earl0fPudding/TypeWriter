from django import forms
from .models import Comment


class CommentForm(forms.Form):
    author_name = forms.CharField(max_length=80, required=False)
    text = forms.CharField(widget=forms.Textarea, required=True)
    content_id = forms.IntegerField(required=True)
    answer_to = forms.IntegerField(required=False)
