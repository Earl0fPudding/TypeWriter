from django.http import Http404, HttpResponseRedirect, HttpResponse
import datetime
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.conf import settings

from webapp.forms import CommentForm, DiscoverForm, SearchForm
from webapp.models import Entry, Content, Language, Category, Settings, Comment, TranslatedText, TranslatedSmalltext
from users.models import CustomUser


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
    author = Entry.objects.get(id=id).author
    latest_entry_ids = list(Entry.objects.all().reverse().values_list('id', flat=True))[:5]
    content = Content.objects.filter(entry_id__exact=id,
                                     language__name_short__exact=get_language_short_name(
                                         request)).first()
    page_context = {'general': get_default_context(request),
                    'content': content,
                    'author': author,
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
                            name_short__exact=get_language_short_name(request)).first().id),
                    'author_desc': TranslatedText.objects.get(
                        translatable_textgroup_id__exact=author.description_short.id,
                        language__name_short__exact=get_language_short_name(request))
                    }

    return render(request, 'article.html', context=page_context)


def get_language_short_name(request):
    return request.build_absolute_uri().split('/')[3]


def get_default_context(request):
    db_settings = Settings.objects.get(id=1)
    cur_url = request.build_absolute_uri()
    urls = []
    for language in Language.objects.all():
        urls.append(cur_url.replace('/' + get_language_short_name(request) + '/', '/' + language.name_short + '/'))
    urls.reverse()
    context = {'blog_title': TranslatedSmalltext.objects.get(
        translatable_smalltext_id=db_settings.blog_title_id,
        language__name_short__exact=get_language_short_name(request)),
        'languages': Language.objects.all(),
        'language_urls': urls,
        'cur_lang_short_name':get_language_short_name(request),
        'categories_lang': TranslatedSmalltext.objects.filter(
            translatable_smalltext_id__in=Category.objects.all().values_list('name_id'),
            language__name_short__exact=get_language_short_name(request)),
        'categories': Category.objects.all(),
        'settings': db_settings,
        'blog_subtitle': TranslatedText.objects.get(
            translatable_textgroup_id__exact=db_settings.blog_subtitle.id,
            language__name_short__exact=get_language_short_name(request)),
        'blog_description': TranslatedText.objects.get(
            translatable_textgroup_id__exact=db_settings.blog_description.id,
            language__name_short__exact=get_language_short_name(request)),
        'uploads_path': settings.MEDIA_URL,
        'static_path': settings.STATIC_URL}
    return context


def show_user_page(request, username):
    user = CustomUser.objects.get(username__exact=username)
    page_context = {'general': get_default_context(request),
                    'user': user,
                    'desc': TranslatedText.objects.get(
                        translatable_textgroup_id__exact=user.description.id,
                        language__name_short__exact=get_language_short_name(request)),
                    'author_content': Content.objects.filter(entry__author=user,
                                                             language__name_short__exact=get_language_short_name(
                                                                 request))
                    }
    return render(request, 'user_page.html', context=page_context)


def show_imprint(request):
    page_context = {'general': get_default_context(request),
                    'page_title': 'Imprint',
                    'text': TranslatedText.objects.get(
                        translatable_textgroup_id__exact=Settings.objects.get(id=1).imprint_text.id,
                        language__name_short__exact=get_language_short_name(request))}
    return render(request, 'blank_page.html', context=page_context)


def show_privacy_policy(request):
    page_context = {'general': get_default_context(request),
                    'page_title': 'Privacy Policy',
                    'text': TranslatedText.objects.get(
                        translatable_textgroup_id__exact=Settings.objects.get(id=1).privacy_policy_text.id,
                        language__name_short__exact=get_language_short_name(request))}
    return render(request, 'blank_page.html', context=page_context)


def show_discover(request):
    contents = None
    form = DiscoverForm(request.GET)
    if form.is_valid():
        if 'languages' in form.data:
            selected_langs = Language.objects.filter(pk__in=request.GET.getlist('languages'))
        else:
            selected_langs = []
        if form.data['all_cat'] == 'all':
            selected_cats = Category.objects.all()
        elif 'categories' in form.data:
            selected_cats = Category.objects.filter(pk__in=request.GET.getlist('categories'))
        else:
            selected_cats = []
        start_date = datetime.datetime(int(form.data['start_year']), int(form.data['start_month']),
                                       int(form.data['start_day']), 0, 0,
                                       0)
        end_date = datetime.datetime(int(form.data['end_year']), int(form.data['end_month']), int(form.data['end_day']),
                                     23, 59, 59)
        contents = Content.objects.filter(language__in=selected_langs,
                                          entry__categories__in=selected_cats,
                                          creation_date__range=[start_date, end_date]).distinct()

        if 'keywords' in form.data and form.data['keywords'] != '':
            keyword_filtered_contents = []
            for content in contents:
                if form.data['title_or_text'] == 'title':
                    if form.data['keywords'].lower() in content.title.lower():
                        keyword_filtered_contents.append(content)
                else:
                    if form.data['keywords'].lower() in content.title.lower() \
                            or form.data['keywords'] in content.summary.lower() \
                            or form.data['keywords'] in content.text.lower():
                        keyword_filtered_contents.append(content)
            contents = keyword_filtered_contents

    else:
        form = SearchForm(request.GET)
        if form.is_valid():
            contents = Content.objects.filter(title__icontains=form.data['keywords'],
                                              language__name_short__exact=get_language_short_name(request))
    page_context = {
        'general': get_default_context(request),
        'current_language': Language.objects.get(name_short__exact=get_language_short_name(request)),
        'results': contents,
        'form': form,
        'selected_langs': request.GET.getlist('languages'),
        'selected_cats': request.GET.getlist('categories')
    }
    return render(request, 'discover.html', context=page_context)
