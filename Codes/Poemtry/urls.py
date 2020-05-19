"""Poemtry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .view import view
from .view import errorhandler as error_handler_view

urlpatterns = [
    # path('admin/', admin.site.urls),

    path(r'', view.poem),
    path(r'write', view.write),
]

handler400 = error_handler_view.bad_request
handler403 = error_handler_view.permission_denied
handler404 = error_handler_view.page_not_found
handler500 = error_handler_view.error
