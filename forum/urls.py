from django.urls import path
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views

urlpatterns = [
    path('home/', views.home, name='forum-home'),
    path('home/articles/', views.article, name='forum-article'),
    path('home/guidelines/', views.guidelines, name='forum-guideline'),
    path('home/discussions/', views.discussions, name='forum-discussion'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('about/', views.about, name='forum-about'),
    path('', views.index, name='forum-index'),
]
