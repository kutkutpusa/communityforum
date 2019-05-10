from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin
from django.urls import reverse


class Post(models.Model):
    general = 1
    article = 2
    guidelines = 3
    STATUS_CHOICES = (
        (general, 'General'),
        (article, 'Article'),
        (guidelines, 'Guidelines')
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
<<<<<<< HEAD
    status = models.IntegerField(choices=STATUS_CHOICES, default=general)
=======
    like = models.ManyToManyField(User, related_name='likes', blank=True)
>>>>>>> dc6bbab9a515ff76931495c359aff710c061cf33

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.like.count()

