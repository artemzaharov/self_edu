from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *

# Create your views here.


def index(request):
    # we can take GET/POST parameters from url adress with request.GET , request.POST is {}
    if request.GET:
        print(request.GET)
    posts = Women.objects.filter(is_published=True)
    context = {'posts': posts,
               'title': "Main Page",
               'cat_selected': 0}
    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': "About Page"})


def addpage(request):
    return HttpResponse("Add new Page")


def contact(request):
    return HttpResponse("Contact Page")


def login(request):
    return HttpResponse("Login Page")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    context = {
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,  # type: ignore
    }

    return render(request, 'women/post.html', context=context)


def pageNotFound(request, *args, **kwargs):
    return HttpResponseNotFound("<h1>Page Not Found From woman/views </h1>")


def show_category(request, cat_slug):
    print('!')
    print(request.GET)
    print('!')
    cat = Category.objects.get(slug=cat_slug)
    posts = Women.objects.filter(cat_id=cat.id)  # type: ignore

    if len(posts) == 0:
        raise Http404()

    context = {'posts': posts,
               'title': "Categories view",
               'cat_selected': cat.id}  # type: ignore
    return render(request, 'women/index.html', context=context)

def archive(request, year):
    if int(year) <= 1991:
        raise Http404()
    elif int(year) >= 2023:
        raise Http404()
    elif int(year) == 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Archive for yesrs</h1><p>{year}</p>")
