from django.db import models

# Create your models here.
class UserType(models.Model):
    display = models.CharField(max_length=5)
    def __str__(self):
        return self.display

class Admin(models.Model):
    username = models.CharField(max_length=50, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    nickname = models.CharField(max_length=20, null=True, verbose_name='昵称')
    email = models.EmailField(verbose_name='Email')
    user_type = models.ForeignKey('UserType', verbose_name='用户类型')
    def __str__(self):
        return self.username

class NewsType(models.Model):
    display = models.CharField(max_length=50)
    def __str__(self):
        return self.display

class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    summary = models.CharField(max_length=256,blank=True,null=True,verbose_name='简介')
    url = models.URLField(verbose_name='网址')
    small_pic = models.CharField(max_length=300,blank=True,null=True,verbose_name='缩略图')
    favor_count = models.IntegerField(default=0,verbose_name='推荐数')
    reply_count = models.IntegerField(default=0,verbose_name='评论数')
    hit_count = models.IntegerField(default=0,verbose_name='点击数')
    isShow = models.BooleanField(default=1, choices=((1,'是'),(0,'否')), verbose_name='显示')
    isHot = models.BooleanField(default=0, choices=((0,'否'),(1,'是')), verbose_name='推荐')
    news_type = models.ForeignKey('NewsType',verbose_name='类型')
    user = models.ForeignKey('Admin',verbose_name='添加人')
    snatch = models.ForeignKey('SnatchUrls',null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '新闻'
    def __str__(self):
        return self.title

class Reply(models.Model):
    content = models.TextField()
    user = models.ForeignKey('Admin')
    new = models.ForeignKey('News')
    create_date = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    content = models.TextField()
    user = models.ForeignKey('Admin')
    create_date = models.DateTimeField(auto_now_add=True)

class SnatchUrls(models.Model):
    title = models.CharField(max_length=30, verbose_name='标题')
    url = models.CharField(max_length=255, verbose_name='网址')
    reg = models.CharField(max_length=100, verbose_name='匹配正则')
    num1 = models.IntegerField(default=1, verbose_name='一次抓取条数')
    num2 = models.IntegerField(default=1, verbose_name='每天最多抓取数')
    used = models.BooleanField(default=1, choices=((1,'是'),(0,'否')), verbose_name='启用')
    isdesc = models.BooleanField(default=1, choices=((1, '降序'), (0, '升序')), verbose_name='抓取顺序')
    news_type = models.ForeignKey('NewsType', verbose_name='类型')
    create_date = models.DateTimeField(auto_now_add=True)
    last_date = models.DateTimeField(verbose_name='最后抓取时间',null=True)
