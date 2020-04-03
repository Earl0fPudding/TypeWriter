from django import template
from webapp.models import Category, TranslatedSmalltext, Content

register = template.Library()


@register.filter
def get_category_name(category_id, lang_short):
    return TranslatedSmalltext.objects.get(
        translatable_smalltext_id=Category.objects.get(id=category_id).name_id,
        language__name_short__exact=lang_short
    ).text


@register.filter
def count_contents_by_categories(category_id, lang_short):
    return len(Content.objects.filter(
        entry__categories=Category.objects.get(id=category_id),
        language__name_short__exact=lang_short,
        is_public=True))
