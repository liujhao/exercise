from django.shortcuts import render, HttpResponse
import os
from helper.FileCls import FileCls, FileLog

# Create your views here.
def home(request):
    logDict = FileLog()
    content = {}
    content['sourceDirs'] = logDict.sourceDirs
    content['toDirs'] = logDict.toDirs
    return render(request,'home.html', content)

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
            return
    else:
        msg = '请输入源文件夹路径！'
        return

    if toDir != '':
        if os.path.exists(toDir):
            pass
        else:
            msg = '目标文件夹不存在！'
            return
    else:
        msg = '请输入目标文件夹路径！'
        return

    if fileListStr !='':
        fileList = fileListStr.split('\n')
        FileCls.rootPath = sourceDir
        FileCls.toDir = toDir
        FileCls.savedList = []
        for item in fileList:
            fpath = os.path.join(sourceDir, item[1:].strip().replace('/','\\'))
            if os.path.exists(fpath):
                file1 = FileCls(fpath)
                charset = file1.charset
                fileCon = file1.makeFile()
                file1.saveToFile(fpath, fileCon, charset)
                if(len(FileCls.savedList)>0):
                    msg = "<h3>成功生成以下文件：</h3>"+'<br>'.join(FileCls.savedList)

    else:
        msg = '请输入文件列表！'
        return
    return HttpResponse(msg)





