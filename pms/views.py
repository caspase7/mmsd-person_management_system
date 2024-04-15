from django.shortcuts import render,redirect
from pms import models
# Create your views here.


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

