from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from . forms import *
from django.views.generic import ListView

# Create your views here.

<<<<<<< HEAD
class WomenHome(ListView):
    # next line try to take all records from db and view them as list
    # by default use this template app_name/model_list.html -> women/women_list.html
    # also when we used def index we loop through posts in templates now we will loop via object_list 
    # or use context_object_name    
    model = Women
    template_name = "women/index.html"
    context_object_name = 'posts'

# def index(request):
#     # we can take GET/POST parameters from url adress with request.GET , request.POST is {}
#     if request.GET:
#         print(request.GET)
#     posts = Women.objects.filter(is_published=True)
#     context = {'posts': posts,
#                'title': "Main Page",
#                'cat_selected': 0}
#     return render(request, 'women/index.html', context=context)
=======

def index(request):
    # we can take GET/POST parameters from url adress with request.GET , request.POST is {}
    if request.GET:
        print(request.GET)
    posts = Women.objects.filter(is_published=True)
    context = {'posts': posts,
               'title': "Main Page",
               'cat_selected': 0}
    return render(request, 'women/index.html', context=context)
>>>>>>> 5d4033edeb0541d19fa2cf22197178e478209eec


def about(request):
    return render(request, 'women/about.html', {'title': "About Page"})


def addpage(request):
    # first time request.method = None so we go to else:
    # second time after submit it will returns form with our data
    if request.method == "POST":
        # request files i used for downloading foto
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            # try:
            #     Women.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, "Mistake in Post add")
            # we use try/exept when form is not connented to model if ti is just:
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'women/addpage.html', {'form': form, 'title': "Add Page"})


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
<<<<<<< HEAD
=======
    print('!')
    print(request.GET)
    print('!')
>>>>>>> 5d4033edeb0541d19fa2cf22197178e478209eec
    cat = Category.objects.get(slug=cat_slug)
    posts = Women.objects.filter(cat_id=cat.id)  # type: ignore

    if len(posts) == 0:
        raise Http404()

    context = {'posts': posts,
               'title': "Categories view",
               'cat_selected': cat.id}  # type: ignore
    return render(request, 'women/index.html', context=context)

<<<<<<< HEAD

=======
>>>>>>> 5d4033edeb0541d19fa2cf22197178e478209eec
def archive(request, year):
    if int(year) <= 1991:
        raise Http404()
    elif int(year) >= 2023:
        raise Http404()
    elif int(year) == 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Archive for yesrs</h1><p>{year}</p>")
