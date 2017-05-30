from django.contrib import admin
from index.models import News, NewsType, Admin, UserType, SnatchUrls
from django import forms

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'summary', 'url', 'small_pic', 'news_type', 'isShow', 'isHot', 'user')
        widgets = {
            'summary': forms.Textarea(attrs={'cols':'30','rows':'2'})
        }

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','news_type','hit_count','favor_count','reply_count','isShow','url')
    search_fields = ('title', 'summary','news_type__display')
    list_per_page = 20
    form = NewsForm
    radio_fields = {
        'news_type': admin.HORIZONTAL,
        'isShow':admin.HORIZONTAL,
        'isHot':admin.HORIZONTAL,
        'user':admin.HORIZONTAL
    }

class AdminAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'user_type')

class SnatchAdmin(admin.ModelAdmin):
    fields = ('title','url','reg','num1','num2','used','isdesc','news_type')
    list_display = ('title','url','news_type','used','last_date')

admin.site.register(News, NewsAdmin)
admin.site.register(NewsType)
admin.site.register(Admin, AdminAdmin)
admin.site.register(UserType)
admin.site.register(SnatchUrls, SnatchAdmin)