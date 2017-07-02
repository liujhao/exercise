import os
import logging
from django.shortcuts import render, HttpResponse
from helper.FileCls import FileCls, FileLog

logger = logging.getLogger('tools.views')

def home(request):
    logDict = FileLog()
    content = {}
    content['sourceDirs'] = logDict.sourceDirs
    content['toDirs'] = logDict.toDirs
    return render(request,'home.html', content)

def doMakeFiles(request):
    sourceDir = request.POST.get('sourceDir','').strip()
    toDir = request.POST.get('toDir','').strip()
    fileListStr = request.POST.get('fileList','').strip()
    msg = ''
    if sourceDir != '':
        if os.path.exists(sourceDir):
            pass
        else:
            msg = '源文件夹不存在！'
    else:
        msg = '请输入源文件夹路径！'

    if toDir != '':
        if os.path.exists(toDir):
            pass
        else:
            msg = '目标文件夹不存在！'
    else:
        msg = '请输入目标文件夹路径！'

    if fileListStr !='':
        fileList = fileListStr.split('\n')
        FileCls.rootPath = sourceDir
        FileCls.toDir = toDir
        # FileCls.showCharset = False
        FileCls.savedList = []
        for i, item in enumerate(fileList):
            fpath = os.path.join(sourceDir, item[1:].strip().replace('/','\\'))
            if os.path.exists(fpath):
                try:
                    file1 = FileCls(fpath)
                    charset = file1.charset
                    fileCon = file1.makeFile()
                    file1.saveToFile(fpath, fileCon, charset)
                except Exception as e:
                    logger.error(e)
                if(len(FileCls.savedList)>0):
                    msg = "<h3>成功生成以下文件：</h3>"+'<br>'.join(FileCls.savedList)
            else:
                if i==0:
                    msg = "<font color=red>源文件不存在，请确认源文件路径是否正确！</font>"

    else:
        msg = '请输入文件列表！'
    return HttpResponse(msg)





