from django.db import models
from Users.models import User


class Video(models.Model):
    title = models.CharField(default='', max_length=64)
    video = models.FileField(upload_to='traffic')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(default='', max_length=32)

    def __str__(self):
        return self.video.name

    class Meta(object):
        # 定义在管理后台显示的名称
        verbose_name = '视频'
        # 定义复数时的名称（去除复数的s）
        verbose_name_plural = verbose_name


class VideoDetail(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    detail = models.JSONField(default=dict)
    handle_video = models.FileField(upload_to='handleVideo', default='')

    class Meta(object):
        # 定义在管理后台显示的名称
        verbose_name = '视频详情'
        # 定义复数时的名称（去除复数的s）
        verbose_name_plural = verbose_name
# Create your models here.
