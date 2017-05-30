"""chouti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.shortcuts import redirect
from django.contrib import admin
from index import views

def Index(request):
    return redirect('/index/')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',Index),
    url(r'^index/(?P<page>\d*)',views.Index),
    url(r'^news/(?P<type>\d+)/(?P<page>\d*)',views.List),
    url(r'^viewnews/(?P<id>\d+)', views.ViewNews),
    url(r'^regist/',views.Regist),
    url(r'^login/',views.Login),
    url(r'^rndcodepic/',views.RndCodePic),
    url(r'^logout/',views.Logout),
    url(r'^addfavor/',views.AddFavor),
    url(r'^addreply/',views.AddReply),
    url(r'^newsreplytree/',views.NewsReplyTree),
    url(r'^sendchat/',views.SendChat),
    url(r'^topchatmsg/',views.TopChatmsg),
    url(r'^search/(?P<words>\w*)/(?P<page>\d*)',views.DoSearch),
    url(r'^search/',views.DoSearch),
    url(r'^spidernews/',views.SpiderNews),
    url(r'^spidertest/(?P<id>\d+)',views.SpiderTest),
    url(r'^resetpwd/',views.RestPwd),
]
