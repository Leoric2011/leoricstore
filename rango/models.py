'''
!/usr/bin/python3.6
-*- coding: utf-8 -*-
File: models.py
Project: Tango with Django 2.0
File Created: Thursday, 3rd May 2018 12:41:48 pm
Author: Dennis, Wangyi (denniswangyi@gmail.com)
-----
Last Modified: Saturday, 12th May 2018 6:33:17 pm
Modified By: Dennis, Wangyi (denniswangyi@gmail.com>)
-----
Copyright 2018 - 2018 Dennis, Wangyi
'''
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class Category(models.Model):
    """目录主体数据模型"""
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Page(models.Model):
    '''页面链接主体数据模型'''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.user.username
