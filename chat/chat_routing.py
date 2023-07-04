from django.urls import path, re_path
from chat.chat_consumers import ChatConsumer
# 建议url前缀使用 ws/xxx 用于区分ws请求和http请求
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/(?P<chat_name>\w+)/(?P<chat_no>\w+)$', ChatConsumer.as_asgi()),
    # path('ws/asqosws/<tradeNo>', AsyncOrderStatusConsumers.as_asgi()),
]
