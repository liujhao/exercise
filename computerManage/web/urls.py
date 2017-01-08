from django.conf.urls import url
from web.views import *
urlpatterns = [
    url(r'^pcadd/',pcAdd),
    url(r'^pcedit/(?P<id>\d+)',pcEdit),
    url(r'^pclist/(\d*)',pcList),
    url(r'^grouplist/',groupList),
    url(r'^groupadd/',groupAdd),
    url(r'^groupManagePcs/',groupManagePcs),
    url(r'^utypelist/',userTypeList),
    url(r'^utypeadd/',userTypeAdd),
    url(r'^userlist/',userList),
    url(r'^useradd/',userAdd),
]
