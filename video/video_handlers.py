from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from video.models import Video, VideoDetail
import sys

sys.path.append('D:\\github\\traffic_tracking\\traffic_tracking\\yolov8_tracking_master')
count = 0

class VideoHandler(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.video = None
        self.download_group_name = None

    def connect(self):
        self.download_group_name = self.scope['url_route']['kwargs']['room_name']
        self.download_group_name = 'handle_%s' % self.download_group_name
        print(self.download_group_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.download_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.download_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        global count
        text_data_json = json.loads(text_data)
        no = text_data_json['no']
        if not count:
            count += 1
            import track
            video = Video.objects.filter(id=no).all()[0]
            self.send(text_data=json.dumps({
                'state': False,
                'order': 'first'
            }))
            print(video.video.name.split('/')[-1])
            print("_________________________________________________________________________________________________________")
            result = track.run("D:\\github\\traffic_tracking\\traffic_tracking\\dist\\static\\media\\traffic\\"+video.video.name.split('/')[-1])
            # result = track.run(video.video.name.split('/')[-1])
            count = 0
            path = "/".join(result[1].replace('\\', '/').split('/')[-2:])
            # print(path, result[-1])
            new_video = VideoDetail.objects.create(video=video, detail=result[-1], handle_video=path)
            identity = new_video.id
            path = new_video.handle_video.url
            video.state = True
            video.save()
            self.send(text_data=json.dumps({
                'state': True,
                'order': 'first',
                'detail': {
                    'url': path,
                    'id': identity,
                    'name': new_video.handle_video.name.split('/')[-1]
                }
            }))
        # Send message to room group
        else:
            self.send(text_data=json.dumps({
                'state': False,
                'order': 'second'
            }))

    # Receive message from room group
    # def info(self, event):
    #     message = event['status']
    #
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         'status': message,
    #     }))
