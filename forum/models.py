from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from django.urls import reverse
from django.forms import TextInput, Textarea



class Post(models.Model):
    STATUS_CHOICES = (
        (1, 'General'),
        (2, 'Article'),
        (3, 'Guidelines')
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    like = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.like.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    reply = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.reply
