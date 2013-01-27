from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    activation_key = models.CharField(max_length=64, blank=True)
    key_expires = models.DateTimeField()

    # Extra fields
    rank = models.CharField(max_length=64, blank=True)
    group = models.CharField(max_length=64, blank=True)

    karma = models.IntegerField(default=0)
    gekinPoints = models.IntegerField(default=0)
    achievements = models.ManyToManyField('Achievement', blank=True)

    # Settings
    show_email = models.BooleanField(default=False)
    show_signatures = models.BooleanField(default=True)

    
    signature = models.CharField(max_length=256, blank=True)

    def __unicode__(self):
        return self.user.username

    def get_num_posts(self):
        return self.post_set.count()

    def get_signature(self):
        return self.signature

class Achievement(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    gekinPoints = models.IntegerField(default=0)
   
    def __unicode__(self):
        return self.title 
    
