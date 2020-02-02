from django import forms
from .models import Comment


class CommentForm(forms.Form):
    author_name = forms.CharField(max_length=80, required=False)
    text = forms.CharField(widget=forms.Textarea, required=True)
    content_id = forms.IntegerField(required=True)
    answer_to = forms.IntegerField(required=False)


class DiscoverForm(forms.Form):
    keywords = forms.CharField(max_length=200, required=False),
    title_or_text = forms.RadioSelect(choices={"title", "both"}),
    languages = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple()),
    all_cat = forms.RadioSelect(choices={"all", "select"}),
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple()),,
    start_day = forms.IntegerField(required=True, min_value=1, max_value=31),
    start_month = forms.IntegerField(required=True, min_value=1, max_value=12),
    start_year = forms.IntegerField(required=True, min_value=2020, max_value=3000),
    end_day = forms.IntegerField(required=True, min_value=1, max_value=31),
    send_month = forms.IntegerField(required=True, min_value=1, max_value=12),
    end_year = forms.IntegerField(required=True, min_value=2020, max_value=3000)


class SearchForm(forms.Form):
    keywords = forms.CharField(max_length=200, min_length=1, required=True)
