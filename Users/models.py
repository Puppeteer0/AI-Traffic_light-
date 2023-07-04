from django.db import models


class User(models.Model):
    account = models.EmailField(max_length=32)
    password = models.CharField(max_length=32, default='')
    nickname = models.CharField(max_length=16, default='')
    avatar = models.FileField(upload_to='avatar', default='avatar/default.webp')

    def __str__(self):
        return self.account

    class Meta(object):
        # 定义在管理后台显示的名称
        verbose_name = '用户'
        # 定义复数时的名称（去除复数的s）
        verbose_name_plural = verbose_name
# Create your models here.
