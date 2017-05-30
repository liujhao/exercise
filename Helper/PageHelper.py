#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe

class PageHelper():
    def __init__(self,url,allcount,curpage=1,pagesize=10,edgesize = 5):
        self.Url = url
        self.AllCount = allcount
        try:
            curpage = int(curpage)
        except(Exception):
            curpage = 1
        if curpage<=0 :
            curpage = 1
        self.CurPage = curpage
        self.PageSize = pagesize
        self.EdgeSize = edgesize
        self.MaxSize = self.EdgeSize * 2 + 1
        self.all_page_count = 0

    @property
    def start(self):
        self.Start = (self.CurPage-1)*self.PageSize
        return self.Start

    @property
    def end(self):
        self.End = self.CurPage * self.PageSize
        return self.End

    @property
    def allPageCount(self):
        if self.all_page_count == 0:
            temp = divmod(self.AllCount, self.PageSize)
            if temp[1] == 0:
                self.all_page_count = temp[0]
            else:
                self.all_page_count = temp[0]+1
            if self.all_page_count<=0 :
                self.all_page_count = 1
        return self.all_page_count

    def pageHtml(self):
        self.allPageCount
        if self.all_page_count < self.MaxSize:
            begin = 0
            end = self.all_page_count
        else:
            if self.CurPage<self.EdgeSize+1:
                begin = 0
                end = self.MaxSize+1
            else:
                if self.CurPage+self.EdgeSize>self.all_page_count:
                    end = self.all_page_count
                    begin = end - self.MaxSize
                else:
                    begin = self.CurPage-self.EdgeSize-1
                    end = self.CurPage+self.EdgeSize
        page_html = []
        if self.allPageCount>1:
            # end_html = "<li><a href='%s%d'>首页</a></li>" % (self.Url, 1)
            # page_html.append(end_html)
            if self.CurPage == 1:
                next_html = ""#"<li><span class='ct_pagepw'>上一页</span></li>"
            else:
                next_html = "<li><a href='%s%d' class='ct_page_edge'>上一页</a></li>" % (self.Url, self.CurPage-1)
            page_html.append(next_html)
            for i in range(begin, end):
                if self.CurPage == i+1:
                    a_html = "<li><span class='ct_pagepw'>%d</span></li>" %(i+1)
                else:
                    a_html = "<li><a href='%s%d' class='ct_pagepa'>%d</a></li>" %(self.Url,i+1,i+1)
                page_html.append(a_html)
            if self.CurPage+1>self.all_page_count:
                next_html = ""#"<li><span class='ct_pagepw'>下一页</span></li>"
            else:
                next_html = "<li><a href='%s%d' class='ct_page_edge'>下一页</a></li>" %(self.Url,self.CurPage+1)
            page_html.append(next_html)
            # end_html = "<li><a href='%s%d'>尾页</a></li>" %(self.Url,self.all_page_count)
            # page_html.append(end_html)
        return mark_safe(''.join(page_html))
