import json

from django.shortcuts import HttpResponse
from Users import models
import requests


def register(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        nickname = request.POST.get('nickName')
        user = models.User.objects.filter(account=account).all()
        dic = {'status': '', 'info': ''}
        if len(user) == 0:
            models.User.objects.create(account=account, password=password, nickname=nickname)
            dic['status'] = 'success'
            dic['info'] = '注册成功'
        else:
            dic['status'] = 'error'
            dic['info'] = '账号已存在'
        return HttpResponse(json.dumps(dic))


def check_nickname(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickName')
        if len(models.User.objects.filter(nickname=nickname).all()):
            return HttpResponse(json.dumps({'status': 'error'}))
        else:
            return HttpResponse(json.dumps({'status': 'ok'}))


def login(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        user = models.User.objects.filter(account=account).all()
        dic = {'status': '',
               'info': '',
               'detail': {
                   'nickName': '',
                   'no': '',
                   'avatar': ''
               }
               }
        if len(user):
            user = user.filter(password=password).all()
            if len(user):
                dic['detail']['nickName'] = user[0].nickname
                dic['detail']['no'] = user[0].id
                dic['detail']['avatar'] = user[0].avatar.url
                dic['status'] = 'success'
                dic['info'] = '登陆成功'
            else:
                dic['status'] = 'error'
                dic['info'] = '密码错误'
        else:
            dic['status'] = 'error'
            dic['info'] = '账号不存在'
        return HttpResponse(json.dumps(dic))


def get_personal_info(request):
    if request.method == 'POST':
        no = request.POST.get('no')
        user = models.User.objects.filter(id=no).all()[0]
        return HttpResponse(json.dumps({
            '账号': user.account,
            '昵称': user.nickname,
            '上传视频条数': len(user.video_set.all()),
            '聊天记录条数': len(user.chat_set.all())
        }))


def upload_avatar(request):
    if request.method == 'POST':
        no = request.POST.get('no')
        img = request.FILES.get('img')
        user = models.User.objects.filter(id=no).all().first()
        user.avatar = img
        user.save()
        return HttpResponse(json.dumps({'status': 'ok'}))


def get_address(request):
    detail = json.loads(requests.get('https://api.map.baidu.com/location/ip?ak=TdFnlwfseG2vzNxISSeAaaoMLU27h9sI&coor'
                                     '=bd09ll').content.decode('utf-8'))
    return HttpResponse(json.dumps({
        'city': detail['content']['address_detail']['city'],
        'point': {
            'x': detail['content']['point']['x'],
            'y': detail['content']['point']['y']
        }
    }))


def get_spot_info(request):
    query = request.GET.get('query')
    region = request.GET.get('region')
    info = json.loads(
        requests.get(f'https://api.map.baidu.com/place/v2/suggestion?query={query}&region={region}&output=json&ak'
                     f'=TdFnlwfseG2vzNxISSeAaaoMLU27h9sI&coor=bd09ll').content.decode('utf-8')
    )
    return HttpResponse(json.dumps({
        'result': info['result']
    }))


def get_routes(request):
    point1 = request.GET.get('point1').split(',')
    point2 = request.GET.get('point2').split(',')
    routes = json.loads(
        requests.get(f'https://api.map.baidu.com/directionlite/v1/driving?origin={point1[0]},{point1[1]}&destination='
                     f'{point2[0]},{point2[1]}&ak=TdFnlwfseG2vzNxISSeAaaoMLU27h9sI&coor=bd09ll')
        .content.decode('utf-8')
    )
    return HttpResponse(json.dumps({
        'result': routes['result']['routes'][0]
    }))


def get_avatar(request):
    no = request.GET.get('no')
    user = models.User.objects.filter(id=no)
    state = False
    url = ''
    if len(user):
        url = f'/static{user.first().avatar.url}'
        state = True
    print(url)
    return HttpResponse(json.dumps({
        'state': state,
        'url': url
    }))

# Create your views here.
