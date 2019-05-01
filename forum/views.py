from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def home(request):
    p = Post.objects.all().order_by('-date_posted')
    query = request.GET.get('q')
    if query:
        p = Post.objects.filter(Q(title__contains=query) | Q(author__username__contains=query) | Q(content__contains=query)).order_by('-date_posted')
    context = {
        'posts' : p
    }
    return render(request, 'forum/home.html', context)

class PostDetailView(DetailView):
    model = Post
    

def about(request):
    return render(request, 'forum/about.html', {'title': 'About IMVU'})

def index(request):
    return render(request, 'forum/index.html')
