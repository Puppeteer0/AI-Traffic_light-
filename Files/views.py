import json

from django.http import FileResponse
from django.shortcuts import HttpResponse
from Files import models


def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        account = request.POST.get('account')
        for file in files:
            print(request.POST)
            f = models.Files(file=file, user_id=account, title=request.POST)
            f.save()
        return HttpResponse(json.dumps({'status': 'ok'}))


def show_files(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        files = models.Files.objects.filter(user__account=account).all()
        file_list = []
        for i in files:
            file_list.append({'file': i.file.url, 'account': i.user.account, 'file_name': i.file.name.split('/')[1],
                              'id': i.id})
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
        models.Files.objects.filter(id=identify).delete()
        return HttpResponse(json.dumps({'status': 'success'}))
# Create your views here.
