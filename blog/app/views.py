from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse

from backweb.models import Article, AType


def index(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        types = AType.objects.all()
        return render(request, 'web/index.html', {'articles': articles, 'types': types})


def gbook(request):
    if request.method == 'GET':
        return render(request, 'web/gbook.html')


def share(request):
    if request.method == 'GET':
        return render(request, 'web/share.html')


def about(request):
    if request.method == 'GET':
        return render(request, 'web/about.html')


def info(request):
    if request.method == 'GET':
        return render(request, 'web/info.html')


def infopic(request):
    if request.method == 'GET':
        return render(request, 'web/infopic.html')


def list(requset):
    if requset.method == 'GET':
        return render(requset, 'web/list.html')