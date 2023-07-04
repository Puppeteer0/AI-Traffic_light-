from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):

    """设置列表可显示的字段"""
    list_display = ('account', 'nickname',  'avatar')

    '''设置过滤选项'''
    list_filter = ('account', 'nickname')

    '''每页显示条目数'''
    list_per_page = 10

    '''设置可编辑字段'''
    list_editable = ('nickname',)


admin.site.register(User, UserAdmin)
# Register your models here.
