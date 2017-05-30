#/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import datetime
import random, string
from urllib import request
from django.utils.safestring import mark_safe
from django.core.mail import EmailMultiAlternatives
from Helper.classes import CJsonEncoder
from chouti import settings

def md5(pwd):
    '''
    对进行md5加密
    :param pwd:要加密的文本
    :return:加密后的文本
    '''
    hash = hashlib.md5(bytes('xx7', encoding='utf-8'))
    hash.update(bytes(pwd, encoding='utf-8'))
    return hash.hexdigest()

def jsonEncoder(djlist):
    '''
    把DjangoSet列表类型转换为json格式数据
    :param djlist:DjangoSet列表
    :return:json列表
    '''
    return json.dumps(list(djlist), cls=CJsonEncoder)

def dateFormat(obj):
    '''
    日期时间类型格式转换
    :param obj:
    :return:
    '''
    ret = obj
    if isinstance(obj, datetime.datetime):
        ret = obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    return ret

def getHtml(url):
    page = request.urlopen(url)
    html = page.read()
    return html.decode("utf8")

def htmlStr(str):
    return mark_safe(str)

def rand_str(length=6):
    chars = string.ascii_letters + string.digits
    s = [random.choice(chars) for i in range(length)]
    ret = '{0}'.format(''.join(s))
    return ret

def sendEmail(title='',content='',toEmail='',subtype='html'):
    from_email = settings.DEFAULT_FROM_EMAIL
    # subject 主题 content 内容 to_addr 是一个列表，发送给哪些人
    msg = EmailMultiAlternatives(title, content, from_email, [toEmail])
    msg.content_subtype = subtype
    msg.send()  # 发送

def formatUrl(hosturl, pageurl):
    '''
    域名和页面地址拼接
    :param hosturl: 从带域名的网址中获取域名和前缀信息
    :param pageurl: 页面url
    :return:完整的页面url地址
    '''
    returl = ''
    if 'http://' in pageurl or 'https://' in pageurl:
        returl = pageurl
    else:
        arr_url = hosturl.split('/')
        url_prefix = arr_url[0]
        url_domain = arr_url[2]
        if pageurl[0] == '/':
            returl = url_prefix + '//' + url_domain + '/' + ('/' + pageurl).replace('//', '')
        elif pageurl[0, 3] == '../':
            upnum = pageurl.count('../')
            arr_url2 = arr_url[0,len(arr_url)-upnum]
            returl += '/'.join(arr_url2) +'/'+ pageurl.replace('../','')
    return returl
