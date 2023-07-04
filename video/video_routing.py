from django.urls import re_path
from video.video_handlers import VideoHandler
# 建议url前缀使用 ws/xxx 用于区分ws请求和http请求
websocket_urlpatterns = [
    re_path(r'ws/video_handler/(?P<room_name>\w+)$', VideoHandler.as_asgi()),
    # path('ws/asqosws/<tradeNo>', AsyncOrderStatusConsumers.as_asgi()),
]