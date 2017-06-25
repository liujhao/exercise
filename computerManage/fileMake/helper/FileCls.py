#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import chardet
import re
import json

class FileCls:
    rootPath = ''   # 文件根目录
    toDir = ''      # 生成新文件根目录
    savedList = []  # 已生成文件列表
    def __init__(self, filePath):
        self.filePath = filePath
        self.charset = 'gb2312'
        self.lines = []
        self.fileDirs = filePath.split('\\')

    def getCharset(self):
        charsetDic = {'ascii':'gb2312'}
        f1 = open(self.filePath, 'rb')
        fline = f1.readline()
        enc = chardet.detect(fline)
        encoding = enc['encoding']
        self.charset = charsetDic.get(encoding,'gb2312')

    # 获取知道物理路径对应的文件内容
    def fileContent(self):
        con = []
        # print(filePath)
        if self.filePath != '':
            if os.path.exists(self.filePath):
                self.getCharset()
                file = open(self.filePath, 'r', encoding=self.charset)
                con = file.readlines()
        return con

    # 获取包含文件的绝对路径
    def getAbsFilePath(self, includeFile):
        parentCount = includeFile.count('../')
        absPath = os.path.join('\\'.join(self.fileDirs[0:-1*(parentCount+1)]), includeFile.replace('../','').replace('/','\\'))
        return absPath

    # 保存到文件
    def saveToFile(self, toFilePath, fileCon, charset='gb2312'):
        newFilePath = toFilePath.replace(FileCls.rootPath, FileCls.toDir)
        newDirs = newFilePath.split('\\')
        dirPath = '\\'.join(newDirs[0:-1])
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        with open(newFilePath,'w', encoding=charset) as newFile:
            # print(fileCon)
            newFile.write(fileCon)
            self.savedList.append(newFilePath)
        log = FileLog()
        log.setSourceDir(FileCls.rootPath)
        log.setToDir(FileCls.toDir)
        log.saveLog()


    # 文件合并功能
    def makeFile(self):
        lines = self.fileContent()
        for line in lines:
            # print(line)
            if re.search(r'<!--#\s*include\s+file=\"', line):
                includeFiles = re.findall(r'<!--#\s*include\s+file=\"(.*)\"\s*-->', line)
                for includeFile in includeFiles:
                    absIncludeFilePath = self.getAbsFilePath(includeFile)
                    if os.path.exists(absIncludeFilePath):
                        file2 = FileCls(absIncludeFilePath)
                        newContent = file2.makeFile()
                        newLine = re.sub(r'<!--#\s*include\s+file=\".*\"\s*-->', newContent, line)
                        self.lines.append(newLine)
            else:
                self.lines.append(line.replace('\\','\\\\'))
        return ''.join(self.lines)

# 记录源文件夹和目标文件夹变化记录
class FileLog:
    jsonFile = 'fileLog.json'
    changed = False
    def loadLog(self):
        data = {}
        with open(os.path.join(os.path.dirname(__file__),FileLog.jsonFile), 'r') as logFile:
            data = json.load(logFile)
        return data

    def saveLog(self):
        if FileLog.changed :
            with open(os.path.join(os.path.dirname(__file__),FileLog.jsonFile), 'w') as logFile:
                logFile.write(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    def __init__(self):
        dict = self.loadLog()
        self.sourceDirs = dict.get('sourceDirs',[])
        self.toDirs = dict.get('toDirs',[])

    def setSourceDir(self, newDir):
        if newDir not in self.sourceDirs:
            self.sourceDirs.append(newDir)
            FileLog.changed = True

    def setToDir(self, newDir):
        if newDir not in self.toDirs:
            self.toDirs.append(newDir)
            FileLog.changed = True
