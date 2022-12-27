from django.urls import path, re_path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path("", index, name='home'),
    # add cache for 60 seconds
    # path('', cache_page(60)(WomenHome.as_view()), name='home'),
    path('', WomenHome.as_view(), name='home'),
    path("about/", about, name="about"),
    path("addpage/", AddPage.as_view(), name="add_page"),
    path("contact/", contact, name="contact"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", WomenCategory.as_view(), name="category"),
    # next function use regular expression for year
    re_path(r'^archive/(?P<year>[0-9]{4})/', archive),
]
