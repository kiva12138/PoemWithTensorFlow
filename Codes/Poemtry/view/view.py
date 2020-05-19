from django.http import HttpResponse
from django.shortcuts import render
from ..work.Write  import *


def poem(request):
    return render(request, 'index.html')


def write(request):
    try:
        params = dict(request.GET)
        result = ''
        if params['type'][0] == 'random':
            result = writeRandom()
        elif params['type'][0] == 'head' and params['content'][0] != "":
            result = writeHead(params['content'][0])
        elif params['type'][0] == 'start' and params['content'][0] != "":
            result = writeStart(params['content'][0])
        else:
            result = '数据格式有误，您可以刷新尝试'
        return HttpResponse(result)
    except:
        return HttpResponse("内部数据出错")
