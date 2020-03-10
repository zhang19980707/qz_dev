from django.db import models

# Create your models here.


class BookInfo(models.Model):
    """图书模型类"""
    btitle = models.CharField(max_length=20)     # 图书名
    bpub_date = models.DateField()       # 出版日期
    bread = models.IntegerField(default=0)      # 阅读量
    bcomment = models.IntegerField(default=0)       # 评论量
    isDelete = models.BooleanField(default=False)       # 删除标记（逻辑删除）


class HeroInfo(models.Model):
    """英雄类"""
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)  # 逻辑删除
    hcomment = models.CharField(max_length=200)
    hbook = models.ForeignKey('BookInfo')    # 关系属性
