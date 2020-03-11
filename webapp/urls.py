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
from .resource_controllers import comment_controller
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^robots.txt$', home.show_robots_txt),
    url(r'^favicon.ico$', home.show_favicon_ico),
    url(r'^favicon.png$', home.show_favicon_png),
    url(r'^mstile-144x144.png$', home.show_favicon_png),
    url(r'^apple-touch-icon.png$', home.show_favicon_png)
]

urlpatterns += i18n.i18n_patterns(
    url(r'^$', home.show_index, name='home'),
    url('login', home.show_login, name='show_login'),
    path('article/<int:id>', home.show_article, name='show_article'),
    path('article/<int:id>/<slug:title>', home.show_article_readable, name='show_article_readable'),
    path('comments/new', comment_controller.post_comment, name='post_comment'),
    path('comments/<int:id>', comment_controller.comment_delete, name='comment_delete'),
    path('imprint', home.show_imprint, name='show_imprint'),
    path('privacy_policy', home.show_privacy_policy, name='show_privacy_policy'),
    path('discover', home.show_discover, name='show_discover'),
    path('@<slug:username>', home.show_user_page, name='show_user_page')
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
