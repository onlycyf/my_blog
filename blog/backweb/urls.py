from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from backweb import views

urlpatterns = [
    # django自带的登录注销
    # url(r'^login/', views.login, name='login'),
    url(r'index/',views.index, name='index'),
    url(r'artAdd/', views.artAdd, name='artAdd'),

    # 自己实现登录和注册
    url(r'^my_register/', views.my_register, name='my_register'),
    url(r'my_login/', views.my_login, name='my_login'),
    url(r'my_logout/', views.my_logout, name='my_logout'),

    # 添加用户
    url(r'add_user/', views.add_user, name='add_user'),
    url(r'userlist/', views.userlist, name='userlist'),

    # 角色和权限
    url(r'add_role/', views.add_role, name='add_role'),
    url(r'user_role/', views.user_role, name='user_role'),

    # 删除
    url(r'delete_art/', views.delete_art, name='delete_art'),
    # 编辑
    url(r'edit/', views.edit,name='edit'),


]