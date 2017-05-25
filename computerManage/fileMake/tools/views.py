from django.shortcuts import render, HttpResponse
import os
import chardet

# Create your views here.
def home(request):
    return render(request,'home.html')

def doMakeFiles(request):
    sourceDir = request.POST.get('sourceDir','')
    toDir = request.POST.get('toDir','')
    fileListStr = request.POST.get('fileList','')
    msg = ''
    if sourceDir != '':
        if os.path.exists(sourceDir):
            pass
        else:
            msg = '源文件夹不存在！'
    else:
        msg = '请输入源文件夹路径！'

    if fileListStr !='':
        fileList = fileListStr.split('\n')
        msg = fileList
    else:
        msg = '请输入文件列表！'
    return HttpResponse(msg)


# 获取知道物理路径对应的文件内容
def fileContent(self, filePath):
    con = []
    # print(filePath)
    if filePath != '':
        if os.path.exists(filePath):
            f1 = open(filePath, 'rb')
            fline = f1.readline()
            enc = chardet.detect(fline)
            # print('encoding:', enc['encoding'])
            file = open(filePath, 'r', encoding=enc['encoding'])
            con = file.readlines()
    return con


