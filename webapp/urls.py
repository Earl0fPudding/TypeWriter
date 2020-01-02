"""TypeWriter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import i18n, url
from .views import home
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls)
]

urlpatterns += i18n.i18n_patterns(
    url(r'^$', home.show_index, name='home'),
    url('login', home.show_login, name='show_login'),
    path('article/<int:id>', home.show_article, name='show_article'),
    path('comments/new', home.post_comment, name='post_comment'),
    path('comments/delete', home.comment_delete, name='comment_delete')
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
