from django.db import models
from Users.models import User


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, default='')
    date = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        # 定义在管理后台显示的名称
        verbose_name = '聊天室'
        # 定义复数时的名称（去除复数的s）
        verbose_name_plural = verbose_name
# Create your models here.
