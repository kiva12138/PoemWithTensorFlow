from django.http import HttpResponse


def bad_request(request, exception):
    # return render(request, '400.html')
    return HttpResponse("400 Bad Request!")


def permission_denied(request, exception):
    # return render(request, '403.html')
    return HttpResponse("403 Permission Denied!")


def page_not_found(request, exception):
    # return render(request, '404.html')
    return HttpResponse("404 Not Found!")


def error(request):
    # return render(request, '500.html')
    return HttpResponse("500 Error!")
