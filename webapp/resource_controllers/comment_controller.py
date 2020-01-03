from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import markdown

from webapp.forms import CommentForm
from webapp.models import Entry, Content, Language, Category, Settings, Comment

@require_http_methods(['POST'])
def comment_delete(request):
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=request.POST['id'])
        if comment.content.entry.author == request.user:
            comment.delete()
            return HttpResponse(status=200)
