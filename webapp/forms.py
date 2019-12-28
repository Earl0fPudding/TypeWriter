from django import forms
from .models import Comment


class CommentForm(forms.Form):
    #    class Meta:
    #        model = Comment
    #        fields = '__all__'
    author_name = forms.CharField(max_length=80)
    text = forms.CharField(widget=forms.Textarea)
    content_id = forms.IntegerField()
    answer_to = forms.IntegerField()
