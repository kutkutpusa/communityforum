from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string


@login_required
def home(request):
    p = Post.objects.all().order_by('-date_posted')
    query = request.GET.get('q')
    if query:
        p = Post.objects.filter(
            Q(title__contains=query) | Q(author__username__contains=query) | Q(content__contains=query)).order_by(
            '-date_posted')
    this_page = request.GET.get("page", 1)
    pages = Paginator(p, 5)
    try:
        posts = pages.page(this_page)
    except PageNotAnInteger:
        posts = pages.page(1)
    except EmptyPage:
        posts = pages.page(pages.num_pages)

    context = {
        'posts': posts
    }
    return render(request, 'forum/home.html', context)


class UserPostListView(ListView):
    model = Post
    template_name = 'forum/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    is_liked = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        if post.like.filter(id=self.request.user.id).exists():
            context['is_liked'] = True
        context['total_like'] = post.total_likes()
        print(context)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Prevent other users from editing someone else's post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# def post_detail(request, pk):
#     post = get_object_or_404(Post, id=pk)
#     is_liked = False
#     if post.like.filter(id=request.user.id).exists():
#         is_liked = True
#     context = {
#         'post': post,
#         'is_liked': is_liked,
#         'total_like': post.total_like(),
#     }
#     return render(request, 'forum/post_detail.html', context)


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        is_liked = False
    else:
        post.like.add(request.user)
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_like': post.total_likes(),
    }

    if request.is_ajax():
        html = render_to_string('forum/like_section.html', context, request=request)
        return JsonResponse({'form': html})


def about(request):
    return render(request, 'forum/about.html', {'title': 'About IMVU'})


def index(request):
    return render(request, 'forum/index.html')
