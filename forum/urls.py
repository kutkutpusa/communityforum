from django.urls import path
from .views import PostDetailView
from . import views

urlpatterns = [
    path('home/', views.home, name='forum-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('about/', views.about, name='forum-about'),
    path('', views.index, name='forum-index'),
]