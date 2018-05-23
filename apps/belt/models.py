from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['name'].isalpha() == False:
            errors["name"] = "Name should be all characters"
            if len(postData['name']) < 3:
                errors["name"] = "Name should be at least 3 characters"

        if len(postData['username']) < 3:
            errors["username"] = "Username should be at least 3 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        user = User.objects.filter(username=postData['username'])
        if(user):
            errors['username'] = 'Username is already in use'
        if postData['confirm_pw'] != postData['password']:
            errors['password'] = "Password not matching"

        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    regdate = models.DateTimeField(null=True)
    objects = UserManager()


class Wish(models.Model):
    itemname = models.CharField(max_length=255)
    adddate = models.DateTimeField(null=True)
    #一对多关系 可join多个trip，一个trip有多个参与者
    all_wishmaker = models.ManyToManyField(User, related_name='attending_wish')
    wish_creater = models.ForeignKey(User, related_name = "user_wish")
