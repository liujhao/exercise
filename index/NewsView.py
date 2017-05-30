#/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import datetime
from index.models import News, NewsType
from index.models import Reply
from index.models import Admin
from index.models import SnatchUrls
from Helper import PageHelper
from Helper import fun

class NewsView():
    def __init__(self):
        self.baseNewsFields = ('id','title','summary','url','news_type__id','news_type__display','favor_count','reply_count','create_date','small_pic','snatch__title','snatch__url')

    # 顶部导航项
    def getTopNType(self, type=0):
        ret = {'ntlist':None, 'title':''}
        if type == None:
            type = 0
        else:
            type = int(type)
        ntlist = NewsType.objects.all()
        if type > 0:
            curntlist = NewsType.objects.filter(id=type)
            if curntlist:
                curNType = curntlist[0]
                curNTypeTitle = curNType.display
                ret['title'] = curNTypeTitle
        ret['ntlist'] = ntlist
        return ret

    # 新闻列表的显示
    def getNews(self, type=0, urltmp='',page=1):
        ret = {'count':0, 'newslist':None, 'pageHtml':''}
        if type == 0:
            count = News.objects.all().count()
            pager = PageHelper.PageHelper(urltmp, count, page, edgesize=4)
            newsList = News.objects.order_by('-create_date').values(*self.baseNewsFields)[pager.start:pager.end]
        else:
            count = News.objects.filter(news_type__id=type).count()
            pager = PageHelper.PageHelper(urltmp, count, page, edgesize=4)
            newsList = News.objects.filter(news_type__id=type).order_by('-create_date').values(*self.baseNewsFields)[pager.start:pager.end]
        ret['count'] = count
        ret['newslist'] = newsList
        ret['pageHtml'] = pager.pageHtml()
        return ret

    # 新闻搜索列表的显示
    def getSecNews(self, words='', urltmp='',page=1):
        ret = {'count':0, 'newslist':None, 'pageHtml':''}
        if words == '':
            count = News.objects.all().count()
            pager = PageHelper.PageHelper(urltmp, count, page, edgesize=4)
            newsList = News.objects.order_by('-create_date').values(*self.baseNewsFields)[pager.start:pager.end]
        else:
            count = News.objects.filter(title__icontains=words).count()
            pager = PageHelper.PageHelper(urltmp, count, page, edgesize=4)
            newsList = News.objects.filter(title__icontains=words).order_by('-create_date').values(*self.baseNewsFields)[pager.start:pager.end]
        ret['count'] = count
        ret['newslist'] = newsList
        ret['pageHtml'] = pager.pageHtml()
        return ret

    # 查看新闻
    def viewNews(self, id=0):
        ret = {'status':0,'data':None,'message':''}
        try:
            news = News.objects.get(id=id)
            news.hit_count = news.hit_count + 1
            news_url = news.url
            if 'http://' in news_url or 'https://' in news_url:
                pass
            else:
                snatch_url = news.snatch.url
                news_url = fun.formatUrl(snatch_url,news_url)
            ret['status'] = 1
            ret['data'] = news_url
            news.save()
        except Exception as e:
            ret['message'] = str(e)
        return ret

    # 新闻点赞
    def addFavor(self, id):
        ret = {'status':0, 'data':None, 'message':''}
        try:
            newsObj = News.objects.get(id=id)
            favorCount = newsObj.favor_count
            newsObj.favor_count = favorCount + 1
            newsObj.save()
            ret['status'] = 1
            ret['data'] = favorCount+1
        except Exception as e:
            ret['message'] = e.message
        return ret

    # 新闻添加评论
    def addReply(self,id, curUser, content):
        ret = {'status':-1, 'data':None, 'message':''}
        if News.objects.filter(id=id).count() == 0:
            ret['status'] = -1
            ret['message'] = '此新闻已不存在！'
        else:
            Reply.objects.create(new_id=id, user_id=curUser['id'], content=content)
            replyCount = Reply.objects.filter(new__id=id).count()
            curNews = News.objects.get(id=id)   #更新新闻表的评论数
            curNews.reply_count = replyCount
            curNews.save()
            ret['status'] = 1
            ret['data'] = replyCount
        return ret

    # 新闻评论树
    def getNewsReplyTree(self, id):
        replyList = Reply.objects.filter(new__id=id).values('content','new__id','user__nickname','create_date').order_by('create_date')
        return replyList

    # 保存新闻记录到数据库
    def saveNews(self, frmdata):
        ret = {'status':0, 'data':None, 'message':''}
        title = frmdata['title']
        if News.objects.filter(title=title).count()>0:
            ret['status'] = 2
            ret['message'] = '已有同样的新闻记录！'
        else:
            news1 = News.objects.create(title=title, url=frmdata['url'],
                                        summary=frmdata.get('summary',''),
                                        small_pic=frmdata.get('small_pic',''),
                                        news_type_id=frmdata.get('type',None),
                                        user_id=frmdata.get('userid',None),
                                        snatch_id=frmdata.get('snatch',None))
            ret['status'] = 1
            ret['data'] = {'id':news1.id, 'title':news1.title,
                           'url':news1.url, 'summary':news1.summary,'type':news1.news_type.id}
        return ret

    # 爬虫抓取新闻记录保存到数据库中
    def spiderNews(self):
        ret = {'status': 0, 'data':None, 'message': ''}
        snatchList = SnatchUrls.objects.filter(used=1).values('id','url','reg','num1','num2','isdesc','last_date','news_type__id')
        userid = None
        allCount = 0
        if snatchList.count()>0:
            try:
                user = Admin.objects.get(username='spider')
                userid = user.id
            except Exception as e:
                pass
        date1 = datetime.date.today()
        date2 = date1 + datetime.timedelta(days=1)
        for snatch in snatchList:
            snatchid = snatch["id"]
            num1 = snatch["num1"]
            num2 = snatch["num2"]
            isdesc = snatch["isdesc"]
            last_date = snatch["last_date"]
            type = snatch["news_type__id"]
            url = snatch["url"]

            yzqCount = News.objects.filter(snatch__id=snatchid,create_date__range=(date1,date2)).count()
            if yzqCount>= num2: #当天抓取记录数如果超过了最大抓取数量，则跳过
                continue
            html = fun.getHtml(url)
            newsre = re.compile(r''+snatch["reg"])
            newslist = newsre.findall(html)
            if isdesc == 1:
                newslist.reverse()
            count = 0
            for news in newslist:
                news_url = fun.formatUrl(url,news[0])
                news_title = news[1]
                news_summary = ''
                if len(news)>2:
                    news_summary = news[2]
                newsData = {'url':news_url, 'title':news_title, 'summary':news_summary,
                            'type':type, 'userid':userid, 'snatch':snatchid}
                saveret = self.saveNews(newsData)
                if saveret['status'] == 1:
                    count += 1
                    allCount += 1
                    if count>=num1: #如果超过一次抓取的条数就跳出本层循环
                        break
                    if count>=num2: #当天抓取记录数如果超过了最大抓取数量跳出本层循环
                        break
            if count>0:
                SnatchUrls.objects.filter(id=snatchid).update(last_date=datetime.datetime.now())
        ret['status'] = 1
        ret['data'] = allCount
        return ret

    def spiderTest(self, id=0):
        newslist = None
        try:
            snatch = SnatchUrls.objects.get(id=id)
        except Exception as e:
            pass
        if snatch:
            html = fun.getHtml(snatch.url)
            newsre = re.compile(r'' + snatch.reg)
            newslist = newsre.findall(html)
        return newslist

    def recommNews(self, type=1, newsType=0):
        if type == 1:   #热门文章
            if newsType == 0:
                newsList = News.objects.filter(isShow=1,isHot=0).order_by('-hit_count','-reply_count')[0:10]
            else:
                newsList = News.objects.filter(isShow=1,isHot=0,news_type__id=newsType).order_by('-hit_count','-reply_count')[0:10]
        elif type==2:   #推荐文章
            if newsType == 0:
                newsList = News.objects.filter(isShow=1,isHot=1).order_by('-hit_count','-reply_count')[0:10]
            else:
                newsList = News.objects.filter(isShow=1,news_type__id=newsType,isHot=1).order_by('-hit_count','-reply_count')[0:10]
        return newsList