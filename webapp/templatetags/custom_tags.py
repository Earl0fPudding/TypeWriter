from django import template
from webapp.models import Category, TranslatedSmalltext

register = template.Library()


@register.filter
def get_category_name(category_id, lang_short):
    return TranslatedSmalltext.objects.get(
        translatable_smalltext_id=Category.objects.get(id=category_id).name_id,
        language__name_short__exact=lang_short
    ).text