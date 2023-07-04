import json

import datetime

from video.congestion import data_calculation

from django.http import HttpResponse, FileResponse

from video.models import Video, VideoDetail

beijing = datetime.timezone(datetime.timedelta(hours=8))


def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        account = request.POST.get('account')
        location = request.POST.get('location')
        for file in files:
            print(request.POST)
            f = Video(video=file, user_id=account, title=file.name, state=False, location=location)
            f.save()
        return HttpResponse(json.dumps({'status': 'ok'}))


def show_files(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        files = Video.objects.filter(user_id=account).all()
        file_list = []
        for i in files:
            if i.state:
                operation = '已操作'
            else:
                operation = '未操作'
            details = i.videodetail_set.all()
            detail = {'url': None, 'id': None, 'name': None}
            if len(details):
                detail['url'] = details[0].handle_video.url
                detail['id'] = details[0].id
                detail['name'] = details[0].video.title
            file_list.append({'file': i.video.url,
                              'account': i.user.account,
                              'file_name': i.title,
                              'id': i.id,
                              'state': i.state == 0,
                              'date': i.date.replace(tzinfo=datetime.timezone.utc)
                             .astimezone(beijing).strftime('%Y-%m-%d %H:%M:%S'),
                              'location': i.location,
                              'operation': operation,
                              'detail': detail
                              })
        return HttpResponse(json.dumps({'status': 'ok', 'file_list': file_list}))


def download_files(request):
    if request.method == 'GET':
        url = request.GET.get('url')
        name = request.GET.get('name')
        file = open(url, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % name
        return response


def delete_file(request):
    if request.method == 'GET':
        identify = request.GET.get('id')
        print(identify)
        video = Video.objects.filter(id=identify).all()[0]
        detail = video.videodetail_set.all()
        if len(detail):
            detail[0].handle_video.delete()
        video.video.delete()
        video.delete()
        return HttpResponse(json.dumps({'status': 'success'}))


def get_detail(detail):
    info = []
    start = 1
    end = len(detail)
    count = 0
    text, time = data_calculation(detail)
    info.append(text + str(time))
    time = int(time/6)
    start = time + start
    print("the end of this: ")
    print(end)
    while start < end:
        print('**************************************')
        text, time = data_calculation(detail[start:])
        print("the text of this: ")
        print(text)
        start = time + start
        print("the start of this: ")
        print(start)
        info.append(text + str(time))
        count = count + 1
    print("the count of this: ")
    print(count)
    return info


def get_video_detail(request):
    if request.method == 'POST':
        identity = request.POST.get('no')
        lst = []
        videos = Video.objects.filter(user_id=identity).all()
        for video in videos:
            if video.state:
                lst.append({
                    'id': video.videodetail_set.all()[0].id,
                    'title': video.title,
                    'location': video.location,
                    'date': video.date.replace(tzinfo=datetime.timezone.utc).astimezone(beijing).strftime('%Y-%m-%d '
                                                                                                          '%H:%M:%S'),
                })
        if len(videos):
            detail = videos.last().videodetail_set.all()[0].detail
            info = get_detail(detail)
            return HttpResponse(json.dumps({'detail': detail, 'info': info, 'id': lst[-1]['id'], 'detail_list': lst}))
        else:
            return HttpResponse(json.dumps({'detail': [], 'info': [], 'id': '', 'detail_list': []}))


def select_video_detail(request):
    if request.method == 'POST':
        no = request.POST.get('no')
        detail = VideoDetail.objects.filter(id=no).all()[0].detail
        info = get_detail(detail)
        return HttpResponse(json.dumps({'detail': detail, 'info': info}))
# Create your views here.
