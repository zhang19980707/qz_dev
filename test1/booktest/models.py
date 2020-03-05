from django.db import models

# Create your models here.


class BookInfo(models.Model):
    """定义图书类"""
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()


class HeroInfo(models.Model):
    """定义英雄类"""
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField()
    hcomment = models.CharField(max_length=100)
    hbook = models.ForeignKey('BookInfo')
