from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import markdown

from webapp.forms import CommentForm
from webapp.models import Entry, Content, Language, Category, Settings, Comment


@csrf_exempt
def comment_delete(request, id):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            comment = get_object_or_404(Comment, pk=id)
            if comment.content.entry.author == request.user:
                comment.delete()
                return HttpResponse(status=204)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=405)
    return HttpResponse(status=500)
