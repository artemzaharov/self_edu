from .models import *
from django.db.models import *
from django.core.cache import cache

menu = [{'title': "About site ", 'url_name': 'about'},
            {'title': "Add article ", 'url_name': 'add_page'},
            {'title': "Contact Us ", 'url_name': 'contact'},
            ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        # use it for cache
        cats = cache.get('cats')
        if not cats:
            # we take only categories wich have posts
            cats = Category.objects.annotate(Count('get_posts'))
            cache.set('cats', cats, 30)
        
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:# type: ignore
             user_menu.pop(1)
        
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        print("Context: ", context)
        return context

