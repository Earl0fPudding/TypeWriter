from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from webapp.forms import CommentForm
from webapp.models import Entry, Content, Language, Category, Settings, Comment


# Create your views here.

@require_http_methods(['GET'])
def show_index(request):
    return render(request, 'index.html')


@require_http_methods(['GET'])
def show_login(request):
    return render(request, 'login.html')


@require_http_methods(['POST'])
def post_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        if form.cleaned_data['answer_to'] != '-1':
            answer_to = None
            content_id = form.cleaned_data['content_id']
        else:
            answer_to = form.cleaned_data['answer_to']
            content_id = None
        if request.user.is_authenticated:
            new_comment = Comment(author_user=request.user, text=form.cleaned_data['text'], answer_to=answer_to, content_id=content_id)
        else:
            new_comment = Comment(author_name=form.cleaned_data['author_name'], text=form.cleaned_data['text'], answer_to=answer_to,
                                  content_id=content_id)
        if Settings.objects.get(id=1).comments_manual_valuation == 0:
            new_comment.passed = 1
        new_comment.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
   # return redirect(show_article, id=Content.objects.get(id=form.content_id).entry_id)


@require_http_methods(['GET'])
def show_article(request, id):
    latest_entry_ids = list(Entry.objects.all().reverse().values_list('id', flat=True))[:5]
    page_context = {'general': get_default_context(request),
                    'content': Content.objects.filter(entry_id__exact=id,
                                                      language__name_short__exact=get_language_short_name(
                                                          request)).first(),
                    'author': Entry.objects.get(id=id).author,
                    'latest_posts': Content.objects.filter(entry_id__in=latest_entry_ids,
                                                           language__name_short__exact=get_language_short_name(
                                                               request)),
                    'comments_allowed': Settings.objects.get(id=1).comments_allowed,
                    'comment_manual_valuated': Settings.objects.get(id=1).comments_manual_valuation,
                    'comments_same_lang': Comment.objects.
                        filter(content__entry_id__exact=id, content__language_id__exact=Language.objects.filter(
                        name_short__exact=get_language_short_name(
                            request)).first().id),
                    'comments_different_lang': Comment.objects.filter(content__entry_id__exact=id).exclude(
                        content__language_id__exact=Language.objects.filter(
                            name_short__exact=get_language_short_name(request)).first().id)}

    return render(request, 'article.html', context=page_context)


def get_language_short_name(request):
    return request.build_absolute_uri().split('/')[3]


def get_default_context(request):
    cur_url = request.build_absolute_uri()
    urls = []
    for language in Language.objects.all():
        urls.append(cur_url.replace('/' + get_language_short_name(request) + '/', '/' + language.name_short + '/'))
    urls.reverse()
    context = {'languages': Language.objects.all(), 'language_urls': urls, 'categories': Category.objects.all()}
    Language.objects.all().count()
    return context
