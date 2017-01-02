from django.db import models

# 电脑
class Computer(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=30)
    ip = models.CharField(null=True, max_length=30)

# 用户组
class UserGroup(models.Model):
    name = models.CharField(max_length=20)
    managePcs = models.CharField(null=True,max_length=500)

# 用户类型
class UserType(models.Model):
    name = models.CharField(max_length=20)

# 用户
class Users(models.Model):
    name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=200, null=True)
    phone = models.CharField(max_length=30, null=True)
    gender = models.BooleanField(default=False)
    age = models.IntegerField(null=True)
    memo = models.TextField(null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    typeId = models.ForeignKey(UserType)
    groupId = models.ManyToManyField(UserGroup)
    managePcs = models.CharField(null=True,max_length=500)

