from django.contrib import admin
from .models import Video, VideoDetail

# Register your models here.

class VideoAdmin(admin.ModelAdmin):

    """设置列表可显示的字段"""
    list_display = ('title', 'video',  'user', 'state', 'date', 'location')

    '''设置过滤选项'''
    list_filter = ('title', 'user', 'state', 'location')

    '''每页显示条目数'''
    list_per_page = 10

    '''按日期月份筛选'''
    date_hierarchy = 'date'

    '''按发布日期排序'''
    ordering = ('date',)


admin.site.register(Video, VideoAdmin)


class VideoDetailAdmin(admin.ModelAdmin):

    """设置列表可显示的字段"""
    list_display = ('video', 'detail', 'handle_video')

    '''设置过滤选项'''
    list_filter = ('video', 'detail', 'handle_video')

    '''每页显示条目数'''
    list_per_page = 10


admin.site.register(VideoDetail, VideoDetailAdmin)
# Register your models here.
