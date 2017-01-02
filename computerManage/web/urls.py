from django.conf.urls import url
from web.views import *
urlpatterns = [
    url(r'^pcadd/',pcAdd),
    url(r'^pclist/',pcList),
    url(r'^grouplist/',groupList),
    url(r'^groupadd/',groupAdd),
    url(r'^groupManagePcs/',groupManagePcs),
    url(r'^utypelist/',userTypeList),
    url(r'^utypeadd/',userTypeAdd),
    url(r'^userlist/',userList),
    url(r'^useradd/',userAdd),
]
