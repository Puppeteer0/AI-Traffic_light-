from django.db import models
from Users.models import User
from chat.models import Chat


class Files(models.Model):
    title = models.CharField(max_length=64)
    file = models.FileField(upload_to='files')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(Chat, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        # 定义在管理后台显示的名称
        verbose_name = '文件'
        # 定义复数时的名称（去除复数的s）
        verbose_name_plural = verbose_name


# Create your models here.
