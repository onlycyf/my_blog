# from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.urls import reverse

from datetime import datetime, timedelta

import random

from backweb.models import AType, Article, User, Permission, Role


def login(request):
    if request.method == 'GET':
        return render(request, 'backweb/login.html')
    if request.method == 'POST':
        # 先获取前端输入的数据
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 验证用户名和密码是否一致
        user = auth.authenticate(request,
                                 username=username,
                                 password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('backweb:index'))
        else:
            return HttpResponseRedirect(reverse('backweb:login'))


def index(request):
    if request.method == 'GET':
        types = AType.objects.all()
        # 第一种 使用切片实现分页
        # page_num= int(request.GET.get('page', 1))   #m如果没有，默认为1
        # start_art = 1 * (int(page_num)-1)
        # end_art = 1 * int(page_num)
        # articles = Article.objects.all()[start_art:end_art]

        # 第二种方式
        page_num = int(request.GET.get('page', 1))
        articles = Article.objects.all()
        paginator = Paginator(articles, 5)
        page = paginator.page(page_num)

        return render(request, 'backweb/index.html', {'page': page, 'types':types})
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('backweb:index'))


def delete_art(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        del_art = Article.objects.filter(id=id).first()
        del_art.is_delete = True
        del_art.save()
        return HttpResponseRedirect(reverse('backweb:index'))


def edit(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        types = AType.objects.all()
        edit_arts = Article.objects.filter(id=id).first()
        return render(request, 'backweb/edit.html',{'edit_arts': edit_arts, 'types':types})
    if request.method == 'POST':
        id = request.GET.get('id')
        art = Article.objects.filter(id=id).first()
        art.title = request.POST.get('title')
        art.desc = request.POST.get('desc')
        art.a_type = request.POST.get('a_type')
        art.is_recommend = request.POST.get('is_recommend')
        art.is_show = request.POST.get('is_show')
        art.image_url = request.FILES.get('img')
        art.content = request.POST.get('content')
        art.save()

        return HttpResponseRedirect(reverse('backweb:index'))


def artAdd(request):
    if request.method == 'GET':
        types = AType.objects.all()
        return render(request, 'backweb/article_detail.html', {'types': types})
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        is_recommend = request.POST.get('is_recommend')
        is_show= request.POST.get('is_show')
        a_type = request.POST.get('a_type')
        content = request.POST.get('content')
        img = request.FILES.get('img')

        Article.objects.create(title=title, desc=desc,
                               is_recommend=is_recommend,
                               is_show=is_show,atype_id=a_type,
                               content=content, image_url=img)

        return HttpResponseRedirect(reverse('backweb:index'))


def my_register(request):
    if request.method == 'GET':
        return render(request, 'backweb/my_register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 先验证注册是否通过
        user = User.objects.filter(username=username).exists()
        if user:
            error = '用户名已经注册，请直接登录'
            return render(request, 'backweb/my_register.html', {'error':error})
        else:
            # 两次密码一致
            if password2 == password1:
                User.objects.create(username=username, password=password1)
                return HttpResponseRedirect(reverse('backweb:my_login'))
            else:
                error= '两次密码不一样'
                return render(request, 'backweb/my_register.html', {'error':error})


def my_login(request):
    if request.method == 'GET':
        return render(request, 'backweb/my_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username, password=password).first()
        if user:
            # 账号密码正确
            # 第一步，cookie中设值
            res = HttpResponseRedirect(reverse('backweb:index'))
            s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
            session_id = ''
            for i in range(20):
                session_id += random.choice(s)
            out_time = datetime.now() + timedelta(days=1)
            res.set_cookie('session_id', session_id, expires=out_time)
            # 第二步，服务端存cookie的值
            user.session_id = session_id
            user.out_time = out_time
            user.save()
            return res

        else:
            error = '用户名或密码错误'
            return render(request, 'backweb/my_login.html', {'error': error})


def my_logout(request):
    if request.method == 'GET':
        # 服务端删除session_id
        user = request.user
        user.session_id = ''
        user.save()
        # 删除cookie中的session_id值
        res = HttpResponseRedirect(reverse('backweb:my_login'))
        res.delete_cookie('session_id')
        return res


# 添加用户
def add_user(request):
    if request.method == "GET":
        return render(request, 'backweb/add_user.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # 先判断用户是否存在
        user = User.objects.filter(username=username)
        if user:
            error = '该员工账号已经添加'
            return render(request, 'backweb/add_user.html', {'error': error})
        else:
            # 如果两次密码相同，则创建用户
            if password1 == password2:
                User.objects.create(username=username,password=password1)
                return HttpResponseRedirect(reverse('backweb:userlist'))
            else:
                error = '两次密码不相同'
                return render(request, 'backweb/add_user.html', {'error': error})


# 用户列表
def userlist(request):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'backweb/userlist.html', {'users':users})


# 添加角色
def add_role(request):
    if request.method == 'GET':
        permissions = Permission.objects.all()
        return render(request, 'backweb/add_role.html', {'permissions': permissions})
    if request.method == 'POST':

        role_name = request.POST.get('role_name')
        pers = request.POST.getlist('pers')

        role = Role.objects.create(r_name=role_name)
        for per in pers:
            p = Permission.objects.filter(p_name=per).first()
            role.r_p.add(p)
        return HttpResponseRedirect(reverse('backweb:userlist'))


# 用户角色管理
def user_role(request):
    if request.method == 'GET':
        users = User.objects.all()
        roles = Role.objects.all()

        return render(request, 'backweb/user_role.html', {'users': users, 'roles': roles})
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        user = User.objects.get(id=user_id)
        user.u_r_id = role_id
        user.save()
        return HttpResponseRedirect(reverse('backweb:userlist'))