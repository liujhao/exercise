#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms

class Computer(forms.Form):
    name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control'}))
    code = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    ip = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class':'form-control'}))
