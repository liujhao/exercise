#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms

class ComputerForm(forms.Form):
    name = forms.CharField(max_length=20)
    code = forms.CharField(max_length=30)
    # code = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ip = forms.GenericIPAddressField()
    def __init__(self,*args,**kwargs):
        super(ComputerForm,self).__init__(*args,**kwargs)
        self.fields['name'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['code'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
        self.fields['ip'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
