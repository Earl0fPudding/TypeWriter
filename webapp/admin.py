from django.contrib import admin
from .models import CustomUser, Language, Category, Entry, Comment, Content


# Register your models here.
@admin.register(CustomUser, Language, Category, Entry, Comment, Content)
class MyAdminSite(admin.ModelAdmin):
    site_header = 'TypeWriter admin site'

