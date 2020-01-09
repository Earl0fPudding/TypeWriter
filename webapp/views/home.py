from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import markdown
from django.conf import settings

from webapp.forms import CommentForm
from webapp.models import Entry, Content, Language, Category, Settings, Comment


# Create your views here.

@require_http_methods(['GET'])
def show_index(request):
    latest_entry_ids = list(Entry.objects.all().reverse().values_list('id', flat=True))[:5]

    page_context = {'general': get_default_context(request),
                    'latest_posts': Content.objects.filter(entry_id__in=latest_entry_ids,
                                                           language__name_short__exact=get_language_short_name(
                                                               request)),
                    }
    return render(request, 'index.html', context=page_context)


@require_http_methods(['GET'])
def show_login(request):
    return render(request, 'login.html')


@require_http_methods(['GET'])
def show_article(request, id):
    latest_entry_ids = list(Entry.objects.all().reverse().values_list('id', flat=True))[:5]
    content = Content.objects.filter(entry_id__exact=id,
                                     language__name_short__exact=get_language_short_name(
                                         request)).first()
    page_context = {'general': get_default_context(request),
#                    'text': markdown.markdown(content.text, output_format='html5'),
                    'content': content,
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
    context = {'languages': Language.objects.all(), 'language_urls': urls, 'categories': Category.objects.all(),
               'settings': Settings.objects.get(id=1), 'uploads_path': settings.MEDIA_URL}
    Language.objects.all().count()
    return context


def show_imprint(request):
    page_context = {'general': get_default_context(request),
                    'imprint_text': markdown.markdown(settings.IMPRINT)}
    return render(request, 'blank_page.html', context=page_context)


def show_privacy_policy(request):
    page_context = {'general': get_default_context(request),
                    'imprint_text': markdown.markdown(settings.PRIVACY_POLICY)}
    return render(request, 'blank_page.html', context=page_context)
