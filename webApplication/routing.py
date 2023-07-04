from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import chat.chat_routing
import video.video_routing


django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.chat_routing.websocket_urlpatterns + video.video_routing.websocket_urlpatterns
        )
    ),
})
