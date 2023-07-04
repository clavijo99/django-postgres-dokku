from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'project_name': settings.WSGI_APPLICATION.split(".")[0]})
