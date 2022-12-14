from django import template
from women.models import *

register = template.Library()


@register.simple_tag(name="getcats")
# getcats just name to use in template instead og get_categories
def get_categories():
    return Category.objects.all()
