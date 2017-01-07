from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from web.Forms.Computer import ComputerForm as pcForm
from web.Forms.Users import UserTypeForm
from web.models import *

def pcAdd(request):
    pcform = pcForm()
    if request.method == 'POST':
        form = pcForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if Computer.objects.filter(code=data['code']).count()==0:
                Computer.objects.create(name=data['name'], code=data['code'], ip=data['ip'])
                if request.POST['act'] == 'save':
                    # return render_to_response('computerAdd.html', {'form': pcform,'success':'保存成功！'})
                    return HttpResponseRedirect('/web/pclist/')
                else:
                    return HttpResponseRedirect('/web/pcadd/')
            else:
                return render_to_response('computerAdd.html', {'form': pcform, 'err': '编号为【'+data['code']+'】的电脑已存在！'})
        else:
            return render_to_response('computerAdd.html', {'form': pcform,'err':'保存失败！'})
    else:
        return render_to_response('computerAdd.html',{'form': pcform})

def pcEdit(request, id):
    pcform = pcForm()
    if request.method == 'POST':
        form = pcForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if Computer.objects.filter(id=id).count()>0:
                pc = Computer.objects.get(id=id)
                pc.name = data['name']
                pc.code = data['code']
                pc.ip = data['ip']
                pc.save()
                return HttpResponse('<script>if(window.opener){window.opener.location.reload();window.close();}</script>')
        else:
            return render_to_response('computerAdd.html', {'form': pcform,'err':'保存失败！'})
    else:
        # print(id)
        pc = Computer.objects.get(id=id)
        pcform = pcForm(initial={'name':pc.name,'code':pc.code,'ip':pc.ip})
        return render_to_response('computerAdd.html',{'form': pcform,'id':id})

def pcList(request):
    list = Computer.objects.order_by('-id')
    return render_to_response('computerList.html', {'list': list})

def transIntOrds(list):
    ret = ''
    for ord in list:
        ret += ('' if ret=='' else ',') + ord
    return ret

def getPcListByIds(ords):
    pcords = list(eval('('+ ords +',)'))
    pclist = Computer.objects.filter(id__in=pcords)
    return pclist

def groupList(request):
    gplist = []
    groups = UserGroup.objects.order_by('-id')
    for group in groups:        
        pclist = getPcListByIds(group.managePcs)
        pcnames = ""
        for pc in pclist:
            pcnames += pc.name + " "
        gplist.append({"group":group, "managePcs":pcnames})
    return render_to_response('userGroupList.html',{'gplist':gplist})

def groupAdd(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        if name.strip() == '':
            pclist = Computer.objects.order_by('-id').values('id','name')
            return render_to_response('userGroupAdd.html',{'pclist':pclist, 'err':'请输入组名称！'})
        pc = request.POST.getlist('pc') 
        pcords = transIntOrds(pc)        
         
        if UserGroup.objects.filter(name=name).count()==0:
            UserGroup.objects.create(name=name, managePcs=pcords)
            if request.POST['act'] == 'save':
                return HttpResponseRedirect('/web/grouplist/')
            else:
                return HttpResponseRedirect('/web/groupadd')
        else:
            pclist = Computer.objects.order_by('-id').values('id','name')
            return render_to_response('userGroupAdd.html',{'pclist':pclist, 'err':'这个用户组已存在！'})
    else:
        pclist = Computer.objects.order_by('-id').values('id','name')
        return render_to_response('userGroupAdd.html',{'pclist':pclist})

def groupManagePcs(request):
    ord = request.POST.get('ord',None)
    if ord==None:
        ord = 0
    group = UserGroup.objects.get(id=ord)
    pclist = getPcListByIds(group.managePcs)
    pcnames = ''
    for pc in pclist:
        pcnames += ('' if pcnames=='' else '\2') + pc.name 
    return HttpResponse(group.managePcs +'\1'+pcnames)

def userTypeList(request):
    utlist = UserType.objects.order_by('-id')
    return render_to_response('userTypeList.html',{'list':utlist})


def userTypeAdd(request):
    utypeForm = UserTypeForm()
    if request.method == 'POST':
        form = UserTypeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            UserType.objects.create(name=data['name'])
            if request.POST['act'] == 'save':
                return HttpResponseRedirect('/web/utypelist/')
            else:
                return HttpResponseRedirect('/web/utypeadd/')
        else:
            return render_to_response('userTypeAdd.html',{'err':'保存失败！'})        
    else:        
        return render_to_response('userTypeAdd.html',{'form':utypeForm})


def userList(request):
    userList = Users.objects.order_by('-createDate')
    return render_to_response('userList.html',{'list':userList})

def userAdd(request):    
    contaions = {}
    if request.method == 'POST':
        noErr = True
        errTip = ''
        name = request.POST.get('name',None)
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        typeId = request.POST.get('typeId',None)
        gplist = request.POST.getlist('groupId')
        pcordlist = request.POST.getlist('pcord')
        age = request.POST.get('age',None)
        gender = request.POST.get('gender',None)
        phone = request.POST.get('phone',None)
        email = request.POST.get('email',None)
        memo = request.POST.get('memo',None)
        act = request.POST.get('act','')
        if noErr and name == None:
            errTip = '请输入用户名称！'
            noErr = False
        if noErr and username == None:
            errTip = '请输入用户账号！'
            noErr = False
        if noErr and password == None:
            errTip = '请输入用户密码！'
            noErr = False
        if noErr and typeId == None:
            errTip = '请选择用户类型！'
            noErr = False
        if noErr and age!=None and age.isdigit()==False:
            errTip = '请正确的年龄！'
            noErr = False
        if noErr==False:
            contaions['err'] = errTip
            grouplist = UserGroup.objects.order_by('-id')
            contaions['grouplist'] = grouplist
            utlist = UserType.objects.order_by('-id')
            contaions['utlist'] = utlist
            return render_to_response('userAdd.html', contaions)
        else:
            user = Users.objects.create(name=name,
                username=username,password=password,
                typeId=UserType.objects.get(id=typeId),
                managePcs=transIntOrds(pcordlist),
                age=age,gender=gender,phone=phone,
                email=email,memo=memo)
            user.save()
            glist = UserGroup.objects.filter(id__in=gplist)
            user.groupId.add(*glist)
            # for gord in gplist:
            #     group = UserGroup.objects.get(id=gord)
            #     user.groupId.add(group)

            if act == 'save':
                return HttpResponseRedirect('/web/userlist/')
            else:
                return HttpResponseRedirect('/web/useradd/')
    else:
        grouplist = UserGroup.objects.order_by('-id')
        contaions['grouplist'] = grouplist
        utlist = UserType.objects.order_by('-id')
        contaions['utlist'] = utlist
        return render_to_response('userAdd.html', contaions)
