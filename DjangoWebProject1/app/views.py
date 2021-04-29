"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import MyRequestForm
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm


def home(request):
    """Renders the home page."""
    posts = Blog.objects.all().reverse()[:6]
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'posts' : posts,
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Свяжитесь с нами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Здесь вы найдете!',
            'year':datetime.now().year,
        }
    )

def links(request):
 
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )


def pool(request):
    """Renders the request page."""
    assert isinstance(request, HttpRequest)
    data = None

    if request.method == 'POST':
        form = MyRequestForm(request.POST)
        if form.is_valid():
            data = dict()
            data['theme'] = form.cleaned_data['requestTheme']
            data['text'] = form.cleaned_data['requestText']
            data['choice'] = form.cleaned_data['requestChoice']
            data['radio'] = form.cleaned_data['requestRadio']
            data['email'] = form.cleaned_data['requestMail']
            form = None
    else:
        form = MyRequestForm()

    return render(
        request,
        'app/pool.html',
        {
            'form' : form,
            'data' : data,
            'title':'Обратная связь',
            'message' : 'Оставьте сообщение об ошибке.',
            'year':datetime.now().year,
        }
    )

def registration(request):
        if request.method == "POST":
            regform = UserCreationForm(request.POST)
            if regform.is_valid():
                reg_f = regform.save(commit=False)
                reg_f.is_staff = False
                reg_f.is_active = True
                reg_f.is_superuser = False
                reg_f.date_joined = datetime.now()
                reg_f.last_login = datetime.now()
                regform.save()
                return redirect('home')
        else:
           regform =  UserCreationForm()
           
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/registration.html',
            {
                'title': 'Регистрация',
                'regform' : regform,
                'year':datetime.now().year,
                }
            )
def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()
   
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
    )
def blogpost(request, parameter):
    """Renders the blog page."""
    post = Blog.objects.get(id=parameter)
    comments = Comment.objects.filter(post=parameter)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parameter)
            comment_f.save()
            return redirect('blogpost', parameter=post.id)
                
    else:
        form = CommentForm()
        


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            
            'post': post,
            'comments': comments,
            'form': form,
            'year':datetime.now().year,
        }
    )
def newpost(request):

    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.author = request.user
            blog_f.posted = datetime.now()
            blog_f.save()
            return redirect('blog')
                
    else:
        blogform = BlogForm()
        


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
        {
            
            'blogform': blogform,
            'year':datetime.now().year,
        }
    )
                                                          