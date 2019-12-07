from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


# Create your views here.

@require_http_methods(['GET'])
def show_index(request):
    return render(request, 'index.html')

@require_http_methods(['GET'])
def show_login(request):
    return render(request, 'login.html')
