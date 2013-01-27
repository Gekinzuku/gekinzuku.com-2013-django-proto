import re
from urllib import quote
from django.db import models
from django.contrib.auth.models import User
from profile.models import UserProfile
from postmarkup import render_bbcode

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=64)
    position = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title

    def get_boards(self):
        return self.board_set.order_by("position")

class Board(models.Model):
    category = models.ForeignKey(Category)

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    position = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title

    def get_topics(self):
        return self.topic_set.order_by("pk")

    def get_topic_count(self):
        return self.topic_set.count()

    def get_most_recent_topic(self):
        return self.topic_set.order_by("-pk")[0]

    def get_total_post_count(self):
        PostCount = 0
        for topic in self.topic_set.order_by("pk"):
            PostCount += topic.get_post_count()
        return PostCount

    def get_URL(self):
        return quote(str(self.pk) + "-" + re.sub(r'[^a-zA-Z0-9:-]', '', self.title.replace(' ', '-')))


class Topic(models.Model):
    board = models.ForeignKey(Board)

    title = models.CharField(max_length=256)

    def __unicode__(self):
        return self.title

    def get_posts(self):
        return self.post_set.order_by("pk")

    def get_post_count(self):
        return self.post_set.count()

    def get_reply_count(self):
        return self.post_set.count()-1

    def get_author(self):
        return self.post_set.order_by("pk")[0].author

    def get_last_reply_author(self):
        return self.post_set.order_by("-pk")[0].author

    def get_date_started(self):
        return self.post_set.order_by("pk")[0].date_posted

    def get_date_last_reply(self):
        return self.post_set.order_by("-pk")[0].date_posted

    def get_URL(self, page=0):
        if page == 0:
            return quote("topic/" + str(self.pk) + "-" + re.sub(r'[^a-zA-Z0-9:-]', '', self.title.replace(' ', '-')))
        else:
            return quote("topic/" + str(self.pk) + "-" + re.sub(r'[^a-zA-Z0-9:-]', '', self.title.replace(' ', '-')) + '/' + page)

    class Meta:
        permissions = (
            ("delete_other_topic", "Can delete other's topics"),
        )
        

class Post(models.Model):
    topic = models.ForeignKey(Topic)
    author = models.ForeignKey(UserProfile)

    body = models.CharField(max_length=16384)

    date_posted = models.DateTimeField(auto_now=False)
    last_edit = models.DateTimeField(auto_now=False)

    def __unicode__(self):
        return self.body

    def get_poster(self):
        return self.author.user.username

    def get_poster_profile(self):
        return self.author

    def get_body(self):
        return render_bbcode(self.body)

    class Meta:
        permissions = (
            ("delete_other_post", "Can delete other's posts"),
            ("change_other_post", "Can edit other's posts"),
        )

