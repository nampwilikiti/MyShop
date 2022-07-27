from datetime import datetime
import os
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import modelform_factory

# Create your models here.


class User(AbstractUser):
    kazi = models.TextField(max_length=50, null=True)
    simu = models.IntegerField(unique=True, null=True)
    sehemu = models.TextField(max_length=100, null=True)


class product(models.Model):
    name = models.TextField(max_length=100, null=False)
    cartegory = models.TextField(max_length=100, null=True)
    price = models.IntegerField(null=False)
    discription = models.TextField(max_length=500, null=True)
    image = models.ImageField(upload_to='uploads', null=False, unique=True)
    time = models.DateTimeField(default=datetime.now(), null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class product_location(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    nation = models.TextField(max_length=100)
    region = models.TextField(max_length=100)
    name = models.TextField(max_length=100)
    latitude = models.DecimalField(max_digits=15, decimal_places=8)
    longtude = models.DecimalField(max_digits=15, decimal_places=8)


class user_location(models.Model):
    ip = models.GenericIPAddressField(null=False)
    nation = models.TextField(max_length=100)
    region = models.TextField(max_length=100)
    latitude = models.DecimalField(max_digits=15, decimal_places=8)
    longtude = models.DecimalField(max_digits=15, decimal_places=8)


class history(models.Model):
    customer = models.ForeignKey(user_location, on_delete=models.CASCADE)
    product_viewed = models.ForeignKey(product_location, on_delete=models.CASCADE)
    date = models.DateTimeField()
