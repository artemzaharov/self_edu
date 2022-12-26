from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout , login
# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator 
# from django.contrib.auth.forms import UserCreationForm


from .utils import *
from .models import *
from . forms import *

# Create your views here.

# menu = [{'title': "About site ", 'url_name': 'about'},
#             {'title': "Add article ", 'url_name': 'add_page'},
#             {'title': "Add article ", 'url_name': 'add_page'},
#             {'title': "Contact Us ", 'url_name': 'contact'},
#             {'title': "Enter ", 'url_name': 'login'},
#             ]


class WomenHome(DataMixin, ListView):
    # next line try to take all records from db and view them as list
    # by default use this template app_name/model_list.html -> women/women_list.html
    # also when we used def index we loop through posts in templates now we will loop via object_list
    # or use context_object_name
    paginate_by = 1
    model = Women
    template_name = "women/index.html"
    context_object_name = 'posts'
    # we can't use extra content with list(we need to check it!!!), its okay for title but if we need list -> use get_context_data.
    # extra_context = {'title': "Home Page"}

    def get_context_data(self, *, object_list=None, **kwargs):
        # this is case if we have menu like list of dicts in views , but we make it temlate tag
        context = super().get_context_data(**kwargs)
        # context['menu'] = menu
        c_def = self.get_user_context(title="Main Page")
        # this are ways to summ 2 dicts
        # context = dict(list(context.items()) + list(c_def.items()))
        # context =  {**context, ** c_def}
        return context | c_def

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


# def index(request):
#     # we can take GET/POST parameters from url adress with request.GET , request.POST is {}
#     if request.GET:
#         print(request.GET)
#     posts = Women.objects.filter(is_published=True)
#     context = {'posts': posts,
#                'title': "Main Page",
#                'cat_selected': 0}
#     return render(request, 'women/index.html', context=context)

def index(request):
    # we can take GET/POST parameters from url adress with request.GET , request.POST is {}
    if request.GET:
        print(request.GET)
    posts = Women.objects.filter(is_published=True)
    context = {'posts': posts,
               'title': "Main Page",
               'cat_selected': 0}
    return render(request, 'women/index.html', context=context)


# @login_required
def about(request):
    # make post pagination with FBV
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_object': page_obj, 'title': "About Page"})


# def addpage(request):
#     # first time request.method = None so we go to else:
#     # second time after submit it will returns form with our data
#     if request.method == "POST":
#         # request files i used for downloading foto
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, "Mistake in Post add")
#             # we use try/exept when form is not connented to model if it is connected - just:
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'title': "Add Page"})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    # LoginRequiredMixin to look this page we must have authorizetion in admin-panel
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    # if we have get_absolute_url in models after adding post we will redirect on post page, but if we want oher page:
    success_url = reverse_lazy('home')
    # login url will rederict to login page, in our case index.html
    login_url = reverse_lazy('home')
    # redirect_field_name = 'redirect_to'
    # if we are not authorized return 403 Page
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add Page")
        return context | c_def


def contact(request):
    return HttpResponse("Contact Page")


# def login(request):
#     return HttpResponse("Login Page")


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)

#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id,  # type: ignore
#     }

#     return render(request, 'women/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    # if we don't have slug_url_kwarg then in urls.py by default we need to use slug instead post_slug
    slug_url_kwarg = 'post_slug'
    # to use post in template
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def




def pageNotFound(request, *args, **kwargs):
    return HttpResponseNotFound("<h1>Page Not Found From woman/views </h1>")


# def show_category(request, cat_slug):
#     cat = Category.objects.get(slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat.id)  # type: ignore

#     if len(posts) == 0:
#         raise Http404()

#     context = {'posts': posts,
#                'title': "Categories view",
#                'cat_selected': cat.id}  # type: ignore
#     return render(request, 'women/index.html', context=context)

class WomenCategory(DataMixin, ListView):
    # we can add paginate in DataMixin because we have it here and in WomenHome
    paginate_by = 1
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # if we don't have posts in category it will be a mistake 'list index out of range
    # we can fix it with allow_empty
    allow_empty = False

    def get_queryset(self):
        # cat__slug is django orm method to another table , self.kwargs['cat_slug'] takes slug from url
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Category -' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return context | c_def


def archive(request, year):
    if int(year) <= 1991:
        raise Http404()
    elif int(year) >= 2023:
        raise Http404()
    elif int(year) == 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Archive for yesrs</h1><p>{year}</p>")


class RegisterUser(DataMixin, CreateView):
    # form_class = UserCreationForm - is standart django form , we write our own in forms.py
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registartion')                         
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


# class LogoutUser(DataMixin, LogoutView):
#     template_name = 'women/logout.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Logout')
#         return context | c_def


def logout_user(request):
    logout(request)
    return redirect('login')