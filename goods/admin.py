from django.contrib import admin
from .models import *
# Register your models here.

class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id','gtitle','gprice','gunit','gclick','gkucun','gtype']
    list_filter = ('gtype',)    #添加筛选
    search_fields = ('gtitle',) #添加搜索字段

admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)