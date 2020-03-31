from django.http import Http404, HttpResponseRedirect, HttpResponse
import datetime
import os.path
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.template.defaultfilters import slugify

from webapp.forms import CommentForm, DiscoverForm, SearchForm
from webapp.models import Entry, Content, Language, Category, Settings, Comment, TranslatedText, TranslatedSmalltext
from users.models import CustomUser


# Create your views here.

def http404(request, exception):
    page_context = {'general': get_default_context(request),
                    'page_title': 'HTTP Error 404',
                    'text': exception}
    return render(request, 'blank_page.html', context=page_context, status=404)


@require_http_methods(['GET'])
def show_robots_txt(request):
    return HttpResponse(content="User-agent: *\n" +
                                "Disallow: /imprint\n" +
                                "Disallow: /privacy_policy\n" +
                                "Disallow: /*/imprint\n" +
                                "Disallow: /*/privacy_policy", content_type="text/plain; charset=utf-8")


@require_http_methods(['GET'])
def show_favicon_ico(request):
    if Settings.objects.get(id=1).favicon_ico:
        path = Settings.objects.get(id=1).favicon_ico.path
        if os.path.isfile(path):
            fsock = open(path, "rb")
            return HttpResponse(content=fsock, content_type="image/x-icon")
    raise Http404()


@require_http_methods(['GET'])
def show_favicon_png(request):
    if Settings.objects.get(id=1).favicon_png:
        path = Settings.objects.get(id=1).favicon_png.path
        if os.path.isfile(path):
            fsock = open(path, "rb")
            return HttpResponse(content=fsock, content_type="image/png")
    raise Http404()


@require_http_methods(['GET'])
def show_article_readable(request, token, title):
    contents = Content.objects.filter(entry__token=token)
    for content in contents:
        if title == slugify(content.title):
            return show_article(request, token)
    return http404(request, "<h1>Article not found</h2>")


@require_http_methods(['GET'])
def show_index(request):
    latest_entry_tokens = list(Entry.objects.all().reverse().values_list('token', flat=True))[:5]

    page_context = {'general': get_default_context(request),
                    'latest_posts': Content.objects.filter(entry__token__in=latest_entry_tokens,
                                                           language__name_short__exact=get_language_short_name(
                                                               request), is_public=True),
                    }
    return render(request, 'index.html', context=page_context)


@require_http_methods(['GET'])
def show_login(request):
    return render(request, 'login.html')


@require_http_methods(['GET'])
def show_article(request, token):
    if len(Entry.objects.filter(token=token)) == 0:
        return http404(request, "<h1>Article not found</h2>")

    author = Entry.objects.get(token=token).author
    latest_entry_tokens = list(Entry.objects.all().reverse().values_list('token', flat=True))[:5]
    if len(Content.objects.filter(entry__token=token,
                                  language__name_short__exact=get_language_short_name(request))) == 0:
        content = Content.objects.filter(entry__token=token, language__default_language=True)
        if len(content) == 0:
            content = Content.objects.filter(entry__token=token)

        content = content[0]

        default_context = get_default_context(request)

        langs = Language.objects.filter(contents__entry__token=token)
        urls = []
        for url in default_context['language_urls']:
            for lang in langs:
                if '/' + lang.name_short + '/' in url:
                    urls.append(url)
                    break

        page_context = {'general': default_context,
                        'content': content,
                        'author': author,
                        'tags': map(lambda s: s.strip(), list(content.tags.split(','))),
                        'latest_posts': Content.objects.filter(entry__token__in=latest_entry_tokens,
                                                               language__name_short__exact=get_language_short_name(
                                                                   request), is_public=True),
                        'comments_allowed': Settings.objects.get(id=1).comments_allowed,
                        'comment_manual_valuated': Settings.objects.get(id=1).comments_manual_valuation,
                        'comments_same_lang': Comment.objects.
                            filter(passed=True, content__entry__token__exact=token,
                                   content__language_id__exact=Language.objects.filter(
                                       name_short__exact=get_language_short_name(
                                           request)).first().id),
                        'comments_different_lang': Comment.objects.filter(passed=True,
                                                                          content__entry__token__exact=token).exclude(
                            content__language_id__exact=Language.objects.filter(
                                name_short__exact=get_language_short_name(request)).first().id),
                        'author_desc': TranslatedText.objects.get(
                            translatable_textgroup_id__exact=author.description_short.id,
                            language__name_short__exact=get_language_short_name(request)),
                        'avail_langs': langs,
                        'avail_urls': urls

                        }

        return render(request, 'wrong_lang_article.html', context=page_context)

    content = Content.objects.filter(entry__token__exact=token,
                                     language__name_short__exact=get_language_short_name(
                                         request)).first()
    page_context = {'general': get_default_context(request),
                    'content': content,
                    'author': author,
                    'tags': map(lambda s: s.strip(), list(content.tags.split(','))),
                    'latest_posts': Content.objects.filter(entry__token__in=latest_entry_tokens,
                                                           language__name_short__exact=get_language_short_name(
                                                               request), is_public=True),
                    'comments_allowed': Settings.objects.get(id=1).comments_allowed,
                    'comment_manual_valuated': Settings.objects.get(id=1).comments_manual_valuation,
                    'comments_same_lang': Comment.objects.
                        filter(passed=True, content__entry__token__exact=token,
                               content__language_id__exact=Language.objects.filter(
                                   name_short__exact=get_language_short_name(
                                       request)).first().id),
                    'comments_different_lang': Comment.objects.filter(passed=True,
                                                                      content__entry__token__exact=token).exclude(
                        content__language_id__exact=Language.objects.filter(
                            name_short__exact=get_language_short_name(request)).first().id),
                    'author_desc': TranslatedText.objects.get(
                        translatable_textgroup_id__exact=author.description_short.id,
                        language__name_short__exact=get_language_short_name(request)),
                    'share_url': request.build_absolute_uri().replace('/' + get_language_short_name(request) + '/', '/')
                    }

    return render(request, 'article.html', context=page_context)


def get_language_short_name(request):
    return request.build_absolute_uri().split('/')[3]


def get_default_context(request):
    db_settings = Settings.objects.get(id=1)
    cur_url = request.build_absolute_uri()
    urls = []
    for language in Language.objects.all():
        url = cur_url.replace('/' + get_language_short_name(request) + '/', '/' + language.name_short + '/')
        url = url[url.find('/') + 2:]
        url = url[url.find('/'):]
        urls.append(url)
    urls.reverse()
    context = {'blog_title': TranslatedSmalltext.objects.get(
        translatable_smalltext_id=db_settings.blog_title_id,
        language__name_short__exact=get_language_short_name(request)),
        'languages': Language.objects.all(),
        'language_urls': urls,
        'cur_lang_short_name': get_language_short_name(request),
        'cur_lang': Language.objects.get(name_short__exact=get_language_short_name(request)),
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
        'default_meta_description': TranslatedSmalltext.objects.get(
            translatable_smalltext_id__exact=db_settings.default_meta_description.id,
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
                                                                 request), is_public=True)
                    }
    return render(request, 'user_page.html', context=page_context)


def show_imprint(request):
    if len(TranslatedText.objects.filter(
            translatable_textgroup_id__exact=Settings.objects.get(id=1).imprint_text.id,
            language__name_short__exact=get_language_short_name(request))) == 0:
        langs = ''
        for text in TranslatedText.objects.filter(
                translatable_textgroup_id__exact=Settings.objects.get(id=1).imprint_text.id):
            langs += text.language.name + ' '
        return http404(request,
                       "<h1>Page not available in your language</h1>\n<h3>Available languages are " + langs + "</h3>")

    page_context = {'general': get_default_context(request),
                    'page_title': 'Imprint',
                    'text': TranslatedText.objects.get(
                        translatable_textgroup_id__exact=Settings.objects.get(id=1).imprint_text.id,
                        language__name_short__exact=get_language_short_name(request)).text}
    return render(request, 'blank_page.html', context=page_context)


def show_privacy_policy(request):
    if len(TranslatedText.objects.filter(
            translatable_textgroup_id__exact=Settings.objects.get(id=1).privacy_policy_text.id,
            language__name_short__exact=get_language_short_name(request))) == 0:
        langs = ''
        for text in TranslatedText.objects.filter(
                translatable_textgroup_id__exact=Settings.objects.get(id=1).privacy_policy_text.id):
            langs += text.language.name + ' '
        return http404(request,
                       "<h1>Page not available in your language</h1>\n<h3>Available languages are " + langs + "</h3>")

    page_context = {'general': get_default_context(request),
                    'page_title': 'Privacy Policy',
                    'text': TranslatedText.objects.get(
                        translatable_textgroup_id__exact=Settings.objects.get(id=1).privacy_policy_text.id,
                        language__name_short__exact=get_language_short_name(request)).text}
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
                                          creation_date__range=[start_date, end_date], is_public=True).distinct()

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
                                              language__name_short__exact=get_language_short_name(request),
                                              is_public=True)
    page_context = {
        'general': get_default_context(request),
        'current_language': Language.objects.get(name_short__exact=get_language_short_name(request)),
        'results': contents,
        'form': form,
        'selected_langs': request.GET.getlist('languages'),
        'selected_cats': request.GET.getlist('categories')
    }
    return render(request, 'discover.html', context=page_context)
