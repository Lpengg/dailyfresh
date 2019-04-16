from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserInfo(AbstractUser):
    ushou = models.CharField(max_length=20,default='')
    uaddress = models.CharField(max_length=100,default='')
    uyoubian = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')
