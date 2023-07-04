from django.contrib import admin
from .models import Chat

# Register your models here.
admin.site.site_title = "人来车往"
admin.site.site_header = "人来车往"
admin.site.index_title = "人来车往"


class ChatAdmin(admin.ModelAdmin):

    """设置列表可显示的字段"""
    list_display = ('user', 'text',  'date')

    '''设置过滤选项'''
    list_filter = ('user', 'text')

    '''每页显示条目数'''
    list_per_page = 10

    '''按日期月份筛选'''
    date_hierarchy = 'date'

    '''按发布日期排序'''
    ordering = ('date',)


admin.site.register(Chat, ChatAdmin)

# Register your models here.
