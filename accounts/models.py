from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum

from news.models import Post, Comment
#
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        s = 0
        for r in Post.objects.filter(author=self).values('rating'):  # суммарный рейтинг каждой статьи автора
            s += int(r['rating'])*3
        for r in Comment.objects.filter(user=self.authorUser).values('rating'):  # суммарный рейтинг всех комментариев автора
            s += int(r['rating'])
        # for c in Post.objects.filter(author=self).values('id'):  # суммарный рейтинг всех комментариев к статьям автора
        #     for r in Comment.objects.filter(id=c.values()).values('rating'):
        #         s += int(r['rating'])
        self.rating = s
        self.save()
        #
        # postRat = self.post_set.aggregate(rating=Sum('rating'))
        # pRat = 0
        # pRat += postRat.get('rating')  #  ?  ('postRating')
        #
        # commentRat = self.authorUser.comment_set.aggregate(rating=Sum('rating'))
        # cRat = 0
        # cRat += commentRat.get('rating')  #  ('commentRating')
        #
        # self.rating = pRat * 3 + cRat
        # self.save()
        return None



