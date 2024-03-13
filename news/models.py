from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum

from accounts.models import Author

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    news = 'news'
    article = 'article'
    ITEMS = [
        (news, 'новость'),
        (article, 'статья')
    ]

    title = models.CharField(max_length=264)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    time_created = models.DateTimeField(auto_now_add=True)
    item = models.CharField(max_length=7,
                            choices=ITEMS)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return self.title.title()

    def preview(self):
        return self.text[0:124] + "..."  # ?

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
