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
                return redirect('/depart/list/')
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

