#/usr/bin/python
# -*- coding:utf-8 -*-

from django import forms

# class UserAdd(forms.Form):
# 	name = forms.CharField(max_length=20)
# 	username = forms.CharField(max_length=20)
# 	password = forms.CharField(max_length=20)
# 	email = forms.EmailField(max_length=200, null=True)
# 	phone = forms.CharField(max_length=30, null=True)
# 	gender = forms.BooleanField(default=False)
# 	age = forms.IntegerField(null=True)
# 	memo = forms.TextField(null=True)
	

class UserTypeForm(forms.Form):
	name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
	