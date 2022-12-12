from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *

# Create your views here.
menu = [{'title': "About site ", 'url_name': 'about'},
        {'title': "Add article ", 'url_name': 'add_page'},
        {'title': "Contact Us ", 'url_name': 'contact'},
        {'title': "Enter ", 'url_name': 'login'},
        ]


def index(request):
    posts = Women.objects.all()
    cats = Category.objects.all()
    context = {'posts': posts,
               'menu': menu,
               'cats': cats,
               'title': "Main Page",
               'cat_selected': 0}
    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': "About Page"})


def addpage(request):
    return HttpResponse("Add new Page")


def contact(request):
    return HttpResponse("Contact Page")


def login(request):
    return HttpResponse("Login Page")


def show_post(request, post_id):
    return HttpResponse(f"Show post with id = {post_id}")


def pageNotFound(request, *args, **kwargs):
    return HttpResponseNotFound("<h1>Page Not Found From woman/views </h1>")


def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    if len(posts) == 0:
        raise Http404()

    context = {'posts': posts,
               'menu': menu,
               'cats': cats,
               'title': "Categiries view",
               'cat_selected': cat_id}
    return render(request, 'women/index.html', context=context)
