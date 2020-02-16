from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core import serializers

from webapp.forms import CommentForm
from webapp.models import Entry, Content, Language, Category, Settings, Comment


@require_http_methods(['POST'])
# @csrf_exempt
def post_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        if form.cleaned_data['answer_to']:
            answer_to = form.cleaned_data['answer_to']
            content_id = None
        else:
            answer_to = None
            content_id = form.cleaned_data['content_id']

        if request.user.is_authenticated:
            new_comment = Comment(author_user=request.user, text=form.cleaned_data['text'], answer_to_id=answer_to,
                                  content_id=content_id)
        else:
            new_comment = Comment(author_name=form.cleaned_data['author_name'], text=form.cleaned_data['text'],
                                  answer_to_id=answer_to,
                                  content_id=content_id)
        if Settings.objects.get(id=1).comments_manual_valuation == 0:
            new_comment.passed = 1
        new_comment.save()

        return HttpResponse(content=serializers.serialize('json', [Comment.objects.get(id=new_comment.id)],
                                                          use_natural_foreign_keys=True, use_natural_primary_keys=True),
                            status=201, content_type='application/json')
    else:
        return HttpResponse(status=400)


@csrf_exempt
def comment_delete(request, id):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            comment = get_object_or_404(Comment, pk=id)
            if request.user.is_superuser or (
                    comment.content is not None and comment.content.entry.author == request.user) or (
                    comment.author_user_id is not None and comment.author_user_id == request.user.id):
                comment.delete()
                return HttpResponse(status=204)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=405)
    return HttpResponse(status=500)
