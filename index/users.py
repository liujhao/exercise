#/usr/bin/env python
# -*- coding:utf-8 -*-

from index.models import Admin
from index.models import Chat
from Helper import fun

class Users():
    #添加新用户
    def AddByForm(self, frmdata):
        newUser ={}
        if Admin.objects.filter(username=frmdata['username']).count() == 0:
            adminUser = Admin.objects.create(username=frmdata['username'],
                                             password=fun.md5(frmdata['password']),
                                             nickname=frmdata['nickname'],
                                             email=frmdata['email'], user_type_id=1)
            newUser = {'status':1,'id': adminUser.id, 'name': adminUser.username, 'nickname': adminUser.nickname}
        else:
            newUser['status'] = 2
        return newUser

    #用户登录
    def CheckLogin(self, frmdata):
        curUser = {}
        if Admin.objects.filter(username=frmdata['username'],password=fun.md5(frmdata['password'])).count() == 1:
            adminUser = Admin.objects.get(username=frmdata['username'],password=fun.md5(frmdata['password']))
            curUser = {'status':1, 'id': adminUser.id, 'name': adminUser.username, 'nickname': adminUser.nickname}
        else:
            curUser['status'] = 0
        return curUser


    #根据user.id获取用户信息
    def getByid(self, id):
        curUser = {'status':0,'id':0,'name':'','nickname':''}
        try:
            adminUser = Admin.objects.get(id=id)
            curUser['status'] = 1
            curUser['id'] = id
            curUser['name'] = adminUser.username
            curUser['nickname'] = adminUser.nickname
        except Exception as e :
            pass
        return curUser

    # 添加聊天记录信息
    def addChat(self, curUser, content):
        ret = {'status':-1, 'data':None, 'message':''}
        userid = curUser['id']
        if Admin.objects.filter(id=userid).count()==0:
            ret['message'] = '用户不存在！'
        else:
            newChart = Chat.objects.create(content=content, user_id=userid)
            ret['status'] = 1
            ret['data'] = {'id':newChart.id, 'content':content,
                           'user__nickname':curUser['nickname'],
                           'create_date': fun.dateFormat(newChart.create_date)}
        return ret

    # 获取最新的前20条聊天记录信息
    def getTopChatmsg(self, lastid):
        chatList = Chat.objects.filter(id__gt=lastid).values('id','content',
                                       'user__id', 'user__nickname',
                                       'create_date').order_by('-id')[0:20]
        return chatList

    # 密码重置
    def resetPassword(self,frmdata):
        ret = {'status':0, 'message':''}
        username = frmdata['username']
        email = frmdata['email']
        try:
            adminUser = Admin.objects.get(username=username,email=email)
            newpwd = fun.rand_str()
            adminUser.password = fun.md5(newpwd)
            adminUser.save()
            ret['status'] = 1
            ret['data'] = newpwd
        except Exception as e:
            ret['message'] = '用户名或邮箱不正确！'
        return ret
