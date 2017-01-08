#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.http.response import HttpResponse

class myMiddleWare(object):
    def process_request(self,request):
        print('1. process_request')

    def process_view(self,request, callback, callback_args,callback_kwargs):
        print('1.process_view')

    def process_exception(self,request,exception):
        print('1.process_exception')

    def process_response(self,request,response):
        print('1.process_response')
        return response