from django.contrib import admin
from .models import Files

# Register your models here.


class FilesAdmin(admin.ModelAdmin):

    """设置列表可显示的字段"""
    list_display = ('title', 'file',  'user', 'chatroom', 'date')

    '''设置过滤选项'''
    list_filter = ('title', 'user', 'chatroom')

    '''每页显示条目数'''
    list_per_page = 10

    '''按日期月份筛选'''
    date_hierarchy = 'date'

    '''按发布日期排序'''
    ordering = ('date',)


admin.site.register(Files, FilesAdmin)

# Register your models here.
