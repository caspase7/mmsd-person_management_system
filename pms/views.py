from django.shortcuts import render, redirect
from django.http import HttpResponse
from pms import models
# Create your views here.


def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        password = request.POST.get('password')

        try:
            user = models.UserInfo.objects.get(id=user_id, password=password)

            if user.limit == 0:
                request.session['user_name'] = user.name
                return redirect('/user/list/')
            elif user.limit == 1:
                request.session['user_name'] = user.name
                return redirect('/depart/add/')
            else:

                return HttpResponse('Invalid user limit')

        except models.UserInfo.DoesNotExist:
            # 如果用户不存在或密码不匹配，返回错误消息
            return HttpResponse('Invalid ID or password')

    return render(request, 'login.html')


def logout(request):
    # 清除会话中的 user_name
    request.session.pop('user_name', None)
    return redirect('login')


def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户POST传过来的数据(暂时不考虑为空的情况)
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回到部门列表
    return redirect("/depart/list/")


def depart_delete(request):

    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()

    # 重定向回到部门列表
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """编辑部门"""
    if request.method == "GET":
        # 根据nid，获取他的数据
        row_object = models.Department.objects.filter(id=nid).first()

        return render(request, "depart_edit.html", {"row_object": row_object})

    # 获取用户提交的标题并修改
    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)

    # 重定向回到部门列表
    return redirect("/depart/list/")


# 用户管理
def user_list(request):
    """用户管理"""

    # 获取所有的用户信息 [obj, obj ……]
    # queryset = models.UserInfo.objects.all()
    queryset = models.UserInfo.objects.filter(condition=0)
    """
    # 使用python的语法来获取
    for obj in queryset:

        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"))
        # get_字段名_display()
        print(obj.get_sex_display())
        obj.depart_id  # 获取数据库中存储的那个字段值
        obj.depart.title     # 根据id自动去关联表中id那一行的depart对象"""

    return render(request, 'user_list.html', {'queryset': queryset})


def user_add(request):
    """添加部门"""
    queryset = models.Department.objects.all()
    if request.method == "GET":
        return render(request, 'user_add.html', {'queryset': queryset})
    # 获取用户POST传过来的数据(暂时不考虑为空的情况)
    id = request.POST.get("id")
    name = request.POST.get("name")
    sex = request.POST.get("sex")
    password = request.POST.get("password")
    age = request.POST.get("age")
    salary = request.POST.get("salary")
    degree = request.POST.get("degree")
    marriage = request.POST.get("marriage")
    create_time = request.POST.get("create_time")
    jobtitle = request.POST.get("jobtitle")
    depart = request.POST.get("depart")
    post = request.POST.get("post")
    condition = request.POST.get("condition")
    limit = request.POST.get("limit")

    # 保存到数据库
    models.UserInfo.objects.create(id=id, name=name, sex=sex, password=password, age=age, salary=salary,
                                    degree=degree, marriage=marriage, create_time=create_time, jobtitle=jobtitle,
                                    depart_id=depart, post=post, condition=condition, limit=limit)
    # 重定向回到部门列表
    return redirect("/user/list/")


def user_edit(request, nid):
    """编辑用户"""
    if request.method == "GET":
        # 根据nid，获取他的数据
        queryset = models.Department.objects.all()
        row_object = models.UserInfo.objects.get(id=nid)
        ctime = row_object.create_time.strftime("%Y-%m-%d")
        return render(request, "user_edit.html", locals())

    name = request.POST.get("name")
    sex = request.POST.get("sex")
    password = request.POST.get("password")
    age = request.POST.get("age")
    salary = request.POST.get("salary")
    degree = request.POST.get("degree")
    marriage = request.POST.get("marriage")
    create_time = request.POST.get("create_time")
    jobtitle = request.POST.get("jobtitle")
    depart = request.POST.get("depart")
    post = request.POST.get("post")
    condition = request.POST.get("condition")
    limit = request.POST.get("limit")
    # 获取用户提交的标题并修改
    models.UserInfo.objects.filter(id=nid).update(name=name, sex=sex, password=password, age=age, salary=salary,
                                    degree=degree, marriage=marriage, create_time=create_time, jobtitle=jobtitle,
                                    depart_id=depart, post=post, condition=condition, limit=limit)

    # 重定向回到部门列表
    return redirect("/user/list/")


def user_list_all(request):
    """用户管理"""

    # 获取所有的用户信息 [obj, obj ……]
    # queryset = models.UserInfo.objects.all()
    queryset = models.UserInfo.objects.all()
    """
    # 使用python的语法来获取
    for obj in queryset:

        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"))
        # get_字段名_display()
        print(obj.get_sex_display())
        obj.depart_id  # 获取数据库中存储的那个字段值
        obj.depart.title     # 根据id自动去关联表中id那一行的depart对象"""

    return render(request, 'user_list_all.html', {'queryset': queryset})

