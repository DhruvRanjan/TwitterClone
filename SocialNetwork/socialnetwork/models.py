from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser
from PIL import Image

class myUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0, blank=True)
    username = models.CharField(max_length=40, unique=True)
    bio = models.CharField(max_length=430, blank=True)
    profile_picture = models.ImageField(upload_to="pictures", default = "pictures/defaultPicture.jpg")
    following = models.ForeignKey('self', null = True, on_delete=models.CASCADE) 

    def __unicode__(self):
        return self.username

class Post(models.Model):

    user = models.ForeignKey(User)
    post_text = models.CharField(max_length=160)
    post_date = models.DateTimeField("date made")

    def __unicode__(self):
        return self.post_text

class Comment(models.Model):

    post = models.ForeignKey(Post)
    comment_text = models.CharField(max_length=160)
    post_date = models.DateTimeField("date made")
    post_author = models.CharField(max_length=40)

