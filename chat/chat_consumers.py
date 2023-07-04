import random

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from chat.models import Chat
from Users.models import User
import datetime


# 异步通讯 redis版本需为5.0及以上
# class AsyncOrderStatusConsumers(AsyncWebsocketConsumer):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.tradeNo_group_name = None
#         self.tradeNo = None
#
#     async def connect(self):
#         self.tradeNo = self.scope['url_route']['kwargs']['tradeNo']
#         self.tradeNo_group_name = 'chat_%s' % self.tradeNo
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.tradeNo_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.tradeNo_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         # text_data_json = json.loads(text_data)
#         # message = text_data_json['message']
#
#         text_data_json = json.loads(text_data)
#         trade_no = text_data_json['tradeNo']
#
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.tradeNo_group_name,
#             {
#                 'type': 'chat_message',  # type 用于指定该消息的类型，根据消息类型调用不同的函数去处理消息
#                 'message': trade_no  # message 内为消息主体
#             }
#         )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         trade_no = event['tradeNo']
#         stop = False
#         # while not stop:
#         data = {
#             "mes": 'hello'
#         }
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps(data))
#         if stop:
#             await self.close()

# class OrderStatusConsumers(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#
#     def disconnect(self, message):
#         pass
#
#     def receive(self, text_data=None, bytes_data=None):
#         # 这里是接受数据后的操作，下面的方法按需修改
#         # logger.info("接受订单号，发送数据")
#         text_data_json = json.loads(text_data)
#         # print(json.loads(text_data))
#         print(text_data_json)
#         data = {
#             "status": 'hello'
#         }
#         # 推送信息到前端
#         self.send(text_data=json.dumps(text_data_json))
#         # 我项目ws推送的结束逻辑


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_no = None
        self.room_group_name = None
        self.room_name = None
        self.chat_name = None

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_no = self.scope['url_route']['kwargs']['chat_no']

        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_group_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        all_content = []
        beijing = datetime.timezone(datetime.timedelta(hours=8))
        content = {
            "date": '',
            "text": '',
            "mine": '',
            "name": '',
            "img": ''
        }
        for chat in Chat.objects.all():
            content['date'] = chat.date.replace(tzinfo=datetime.timezone.utc).astimezone(beijing).strftime(
                '%Y-%m-%d %H:%M:%S')
            if chat.text == '照片':
                content['text'] = {
                    # http://localhost:5000
                    "text": f'<img data-src="/static{chat.files_set.all()[0].file.url}">'
                }
            else:
                content['text'] = {"text": chat.text}
            content['mine'] = self.chat_name == chat.user.nickname
            content['name'] = chat.user.nickname
            # http://localhost:5000
            content['img'] = f'/static{chat.user.avatar.url}'
            all_content.append(content.copy())
        self.send(text_data=json.dumps({
            'status': 'first',
            'message': all_content
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        if not bytes_data:
            text_data_json = json.loads(text_data)
            no = text_data_json[0]
            user = User.objects.filter(id=no).all()[0]
            message = text_data_json[1]
            Chat.objects.create(user=user, text=message['text']['text'])
            message['mine'] = False
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        else:
            from django.core.files.uploadedfile import InMemoryUploadedFile
            from io import BytesIO
            f = BytesIO()
            f.write(bytes_data)
            # InMemoryUploadedFile 需要的参数：file, field_name, name, content_type, size, charset, content_type_extra = None
            image = InMemoryUploadedFile(f, None, "{}_{}.png".format('KF45464789', random.randint(100, 999)), None,
                                         len(bytes_data), None, None)
            user = User.objects.filter(id=self.chat_no).all()[0]
            file = Chat.objects.create(user=user, text='照片').files_set.create(user=user, title=image.name, file=image)
            # http://localhost:5000
            # http://localhost:5000
            message = {
                "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "text": {"text": f'<img data-src="/static{file.file.url}">'},
                "mine": True,
                "name": self.chat_name,
                "img": f'/static{user.avatar.url}'
            }
            self.send(json.dumps({
                'status': 'times',
                'message': message,
                'type': 'pic'
            }))
            message['mine'] = False
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_pic',
                    'message': message
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'status': 'times',
            'message': message
        }))

    def chat_pic(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'status': 'times',
            'message': message,
        }))
