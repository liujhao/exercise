#/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms

class AdminForm(forms.Form):
    username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':'用户名','class':'userid'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class':'pwd','placeholder':'密码'}))
    nickname = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder':'昵称'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))


