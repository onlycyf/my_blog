from django.db import models

# from DjangoUeditor.models import UEditorField


class AType(models.Model):
    name = models.CharField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'atype'


class Article(models.Model):
    title = models.CharField(max_length=15, null=False)
    desc = models.CharField(max_length=50, null=False)
    # 是否展示
    is_show = models.BooleanField(default=False)
    # 是否推荐
    is_recommend = models.BooleanField(default=False)

    # 保存图片upload_to = 'upload' 将图片保存到upload的文件夹中
    image_url= models.ImageField(upload_to='upload', null=True)

    content = models.TextField()
    # 外键wa
    atype = models.ForeignKey(AType)
    create_time = models.DateTimeField(auto_now_add=True)
    oprate_time = models.DateTimeField(auto_now=True)

    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'article'


class Permission(models.Model):
    """
    权限表
    文章列表权限 --- 》LISTARTICLE
    文章添加权限 --- 》ADDARTICLE
    文章编辑权限 --- 》EDITARTICLE
    文章删除权限 --- 》DELETEARTICLE
    """
    p_name= models.CharField(max_length=15)

    class Meta:
        db_table = 'permission'


class Role(models.Model):
    """
    角色表
    """
    r_name = models.CharField(max_length=10)
    r_p = models.ManyToManyField(Permission)

    class Meta:
        db_table = 'role'


class User(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=225)
    is_superuser = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=30, null=True)
    out_time = models.DateTimeField(null=True)
    u_r = models.ForeignKey(Role, null=True)

    class Meta:
        db_table = 'user'








