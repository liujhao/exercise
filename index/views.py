import json, os, io
from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import HttpRequest
from Helper import fun, Checkcode
from index.models import *
from index.djforms import *
from index.users import Users
from index.NewsView import NewsView
from chouti.settings import BASE_DIR
def defUser(func):
    '''
    应用装饰器读取记住用户名的用户信息并存到session中
    '''
    def _defUser(*args, **kwargs):
        if len(args)>0:
            if isinstance(args[0], HttpRequest):
                getUserByCookie(args[0])
        ret = func(*args, **kwargs)
        return ret
    return _defUser

def getUserByCookie(request):
    '''
    从cookie中读取用户信息并存入session中
    :param request:
    '''
    if request.session.get('curUser',None) is None:
        if request.COOKIES.get('userid','')!='':
            userid = request.COOKIES.get('userid','0')
            user1 = Users()
            curUser = user1.getByid(userid)
            if curUser['status'] == '1':
                request.session['curUser'] = curUser

@defUser
def Index(request,page):
    data = {}
    news = NewsView()
    ntypeDic = news.getTopNType()
    newsDic = news.getNews(urltmp='/index/',page=page)
    data['title'] = '首页'
    data['curUser'] = request.session.get('curUser',None)
    data['navlist'] = ntypeDic['ntlist']
    data['newsList'] = newsDic['newslist']
    data['pageHtml'] = newsDic['pageHtml']
    data['recommNews'] = news.recommNews(1,0)
    data['recommNews2'] = news.recommNews(2,0)
    return render_to_response('index.html',data)

@defUser
def List(request, type, page):
    data = {}
    news = NewsView()
    ntypeDic = news.getTopNType(type=type)
    newsDic = news.getNews(type=type, urltmp='/news/'+type+'/', page=page)
    data['title'] = ntypeDic['title']
    data['curUser'] = request.session.get('curUser', None)
    data['ntype'] = int(type)
    data['navlist'] = ntypeDic['ntlist']
    data['newsList'] = newsDic['newslist']
    data['pageHtml'] = newsDic['pageHtml']
    data['recommNews'] = news.recommNews(1, type)
    data['recommNews2'] = news.recommNews(2, type)
    return render_to_response('index.html',data)

def ViewNews(request, id):
    news = NewsView()
    ret = news.viewNews(id)
    if ret['status'] == 1:
        return HttpResponseRedirect(ret['data'])
    else:
        return HttpResponse('<script>alert("'+ret['message']+'");window.close();</script>')

def Regist(request):
    data = {}
    ntlist = NewsType.objects.all()
    data['navlist'] = ntlist
    adminForm = AdminForm()
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            frmdata = form.cleaned_data
            user1 = Users()
            curUser = user1.AddByForm(frmdata)
            if curUser['status'] == 1:
                request.session['curUser'] = curUser
                return HttpResponseRedirect('/index/')
            else:
                data['form'] = form
                data['err'] = '用户名已存在！'
                return render_to_response('regist.html',data)
        else:
            data['form'] = form
            data['err'] = '提交信息不完整！'
            return render_to_response('regist.html', data)
    else:
        data['form'] = adminForm
        return render_to_response('regist.html', data)

def RndCodePic(request):
    validate_code = Checkcode.create_validate_code()
    img = validate_code[0]
    img.save(os.path.join(BASE_DIR, 'static/randCode.gif'), "GIF")
    request.session["CheckCode"] = validate_code[1]
    return HttpResponseRedirect('/static/randCode.gif')
    '''
    validate_code = Checkcode.create_validate_code()
    img = validate_code[0]
    buff = io.BytesIO(img.tobytes())
    # buff2 = io.StringIO(str(img.tobytes()))
    return HttpResponse(str(buff.getvalue()), 'image/jpeg')
    '''

def Login(request):
    data = {}
    ntlist = NewsType.objects.all()
    data['navlist'] = ntlist
    if request.method == 'POST':
        frmdata = {'username':request.POST.get('username',''),
                   'password':request.POST.get('password',''),
                   'rndcode':request.POST.get('rndcode','')}
        if frmdata['username']=='':
            data['form'] = frmdata
            data['err'] = '请输入用户名！'
            return render_to_response('login.html', data)
        elif frmdata['password']=='':
            data['form'] = frmdata
            data['err'] = '请输入密码！'
            return render_to_response('login.html', data)
        elif frmdata['rndcode']=='':
            data['form'] = frmdata
            data['err'] = '请输入验证码！'
            return render_to_response('login.html', data)
        else:
            rndcode = frmdata['rndcode']
            if rndcode.lower()!=request.session.get('CheckCode','').lower():
                data['form'] = frmdata
                data['err'] = '验证码不正确！'
                return render_to_response('login.html', data)
            else:
                user1 = Users()
                curUser = user1.CheckLogin(frmdata)
                if curUser['status'] == 1:
                    request.session['curUser'] = curUser
                    response = HttpResponseRedirect('/index/')
                    if request.POST.get('keeplogin', '0') == '1':
                        response.set_cookie('userid', curUser['id'], 60 * 60 * 24 * 30)
                    return response
                else:
                    data['form'] = frmdata
                    data['err'] = '用户名或密码不正确！'
                    return render_to_response('login.html', data)

    else:
        return render_to_response('login.html', data)

def Logout(request):
    if request.session.get('curUser',None):
        del request.session['curUser']
    response = HttpResponseRedirect('/index/')
    if request.COOKIES.get('userid','')!='':
        response.delete_cookie('userid')
    return response

def AddFavor(request):
    news = NewsView()
    id = request.POST.get('id',0)
    return HttpResponse(json.dumps(news.addFavor(id)))

def AddReply(request):
    ret = {'status':0,'data':None,'message':''}
    news = NewsView()
    id = request.POST.get('id', 0)
    content = request.POST.get('content','')
    curUser = request.session.get('curUser',None)
    if curUser is None:
        ret['message'] = '登录后才可以提交评论或回复，请先登录！'
        return HttpResponse(json.dumps(ret))
    else:
        addRet = news.addReply(id, curUser,content)
        return HttpResponse(json.dumps(addRet))

def NewsReplyTree(request):
    news = NewsView()
    id = request.POST.get('id', 0)
    return HttpResponse(fun.jsonEncoder(news.getNewsReplyTree(id)))

def SendChat(request):
    ret = {'status': 0, 'data': None, 'message': ''}
    content = request.POST.get('content')
    curUser = request.session.get('curUser', None)
    if curUser is None:
        ret['message'] = '登录后才可以聊天，请先登录！'
        return HttpResponse(json.dumps(ret))
    else:
        user1 = Users()
        addRet = user1.addChat(curUser,content)
        return HttpResponse(json.dumps(addRet))

def TopChatmsg(request):
    user1 = Users()
    lastid = int(request.POST.get('lastid',0))
    return HttpResponse(fun.jsonEncoder(user1.getTopChatmsg(lastid)))

def DoSearch(request, words='', page=1):
    if request.method == 'POST':
        words = request.POST.get('words','')
        return HttpResponseRedirect('/search/'+words+'/')
    else:
        data = {}
        news = NewsView()
        ntypeDic = news.getTopNType()
        newsDic = news.getSecNews(words=words, urltmp='/search/' + words + '/', page=page)
        data['title'] = '搜索：'+ words
        data['searchkey'] = words
        data['curUser'] = request.session.get('curUser', None)
        data['navlist'] = ntypeDic['ntlist']
        data['newsList'] = newsDic['newslist']
        data['pageHtml'] = newsDic['pageHtml']
        data['recommNews'] = news.recommNews(1, 0)
        data['recommNews2'] = news.recommNews(2, 0)
        return render_to_response('index.html', data)

def SpiderNews(request):
    news = NewsView()
    return HttpResponse(news.spiderNews())

def SpiderTest(request, id):
    '''
    测试抓取项的正则匹配是否成功
    :param request:
    :param id: 抓取相id
    '''
    news = NewsView()
    return HttpResponse(json.dumps(news.spiderTest(id)))

# 密码重置，重置成功后发送到邮箱
def RestPwd(request):
    data = {}
    news = NewsView()
    ntypeDic = news.getTopNType()
    data['title'] = '找回密码'
    data['navlist'] = ntypeDic['ntlist']
    if request.method == 'POST':
        frmdata = {'username': request.POST.get('username', ''),
                   'email': request.POST.get('email', ''),
                   'rndcode': request.POST.get('rndcode', '')}
        if frmdata['username'] == '':
            data['form'] = frmdata
            data['err'] = '请输入用户名！'
            return render_to_response('resetpwd.html', data)
        elif frmdata['email'] == '':
            data['form'] = frmdata
            data['err'] = '请输入Email！'
            return render_to_response('resetpwd.html', data)
        elif frmdata['rndcode'] == '':
            data['form'] = frmdata
            data['err'] = '请输入验证码！'
            return render_to_response('resetpwd.html', data)
        else:
            rndcode = frmdata['rndcode']
            if rndcode.lower() != request.session.get('CheckCode', '').lower():
                data['form'] = frmdata
                data['err'] = '验证码不正确！'
                return render_to_response('resetpwd.html', data)
            else:
                user1 = Users()
                ret = user1.resetPassword(frmdata)
                if ret['status'] == 1:
                    fun.sendEmail('密码重置成功',
                                  '<h3>密码重置成功</h3><br>您的新密码是：<font color=red>'+ret['data']+'</font>',
                                  frmdata['email'])
                    data['message'] = '密码重置成功! 新密码已发送到您的邮箱，请进入邮箱查阅。'
                    return render_to_response('resetpwd.html', data)
                else:
                    data['form'] = frmdata
                    data['err'] = ret['message']
                    return render_to_response('resetpwd.html', data)
    else:
        return render_to_response('resetpwd.html', data)


