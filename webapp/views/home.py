from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse


# Create your views here.

@require_http_methods(['GET'])
def show_index(request):
    return render(request, 'index.html')


@require_http_methods(['GET'])
def show_login(request):
    return render(request, 'login.html')


@require_http_methods(['GET'])
def test(request):
    page_context = {'message':request.build_absolute_uri().split('/')[3]}
    return render(request, 'test.html', context=page_context)
