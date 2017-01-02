#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms

class Computer(forms.Form):
    name = forms.CharField(max_length=20)
    code = forms.CharField(max_length=30)
    ip = forms.GenericIPAddressField()