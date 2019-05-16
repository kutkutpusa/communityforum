from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from users.forms import CommentForm
from django.shortcuts import redirect


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


def article(request):
    a = Post.objects.filter(status=Post.article).order_by('-date_posted')
    query = request.GET.get('q')
    if query:
        a = Post.objects.filter(status=Post.article).order_by('-date_posted')
    this_page = request.GET.get("page", 1)
    pages = Paginator(a, 5)
    try:
        articles = pages.page(this_page)
    except PageNotAnInteger:
        articles = pages.page(1)
    except EmptyPage:
        articles = pages.page(pages.num_pages)

    context = {
        'articles' : articles
    }
    return render(request, 'forum/article.html', context)

def guidelines(request):
    g = Post.objects.filter(status=Post.guidelines).order_by('-date_posted')
    query = request.GET.get('q')
    if query:
        g = Post.objects.filter(status=Post.guidelines).order_by('-date_posted')
    this_page = request.GET.get("page", 1)
    pages = Paginator(g, 5)
    try:
        guidelines = pages.page(this_page)
    except PageNotAnInteger:
        guidelines = pages.page(1)
    except EmptyPage:
        guidelines = pages.page(pages.num_pages)

    context = {
        'guidelines' : guidelines
    }
    return render(request, 'forum/guideline.html', context)

def discussions(request):
    d = Post.objects.filter(status=Post.general).order_by('-date_posted')
    query = request.GET.get('q')
    if query:
        d = Post.objects.filter(status=Post.general).order_by('-date_posted')
    this_page = request.GET.get("page", 1)
    pages = Paginator(d, 5)
    try:
        discussions = pages.page(this_page)
    except PageNotAnInteger:
        discussions = pages.page(1)
    except EmptyPage:
        discussions = pages.page(pages.num_pages)

    context = {
        'discussions' : discussions
    }
    return render(request, 'forum/discussion.html', context)


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
        context['form'] = CommentForm()
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
    template_name = 'forum/edit_forum_post.html'
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


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        print(request.user)
        if form.is_valid():
            reply = request.POST.get('reply')
            comment = Comment.objects.create(post=post, author=request.user, reply=reply)
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'forum/add_comment_to_post.html', {'form': form})



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
    if request.method == 'POST':
        return render(request, 'forum/main.html')
    