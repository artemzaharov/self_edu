from django import template
from women.models import *

register = template.Library()

# just an example , we dont use it
# get_categories is just an example , we dont use it


@register.simple_tag(name="getcats")
# getcats just name to use in template instead of get_categories
def get_categories():
    return Category.objects.all()


@register.inclusion_tag("women/list_categories.html")
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    # this parametr 'cats' will automaticly work in list_categories
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag("women/menu.html")
def show_menu():
    menu = [{'title': "About site ", 'url_name': 'about'},
            {'title': "Add article ", 'url_name': 'add_page'},
            {'title': "Add article ", 'url_name': 'add_page'},
            {'title': "Contact Us ", 'url_name': 'contact'},
            {'title': "Enter ", 'url_name': 'login'},
            ]
    # this parametr 'cats' will automaticly work in list_categories
    return {"menu": menu, }