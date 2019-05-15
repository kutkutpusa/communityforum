from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('analytics/', views.analytics, name='analytics-home'),
]

