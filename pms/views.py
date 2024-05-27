from django.shortcuts import render, redirect
from django.http import HttpResponse
from pms import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.db.models import Sum, Q, Func , Value
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractYear, Concat


def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        password = request.POST.get('password')

        try:
            user = models.UserInfo.objects.get(id=user_id, password=password)

            if user.limit == 0:
                request.session['user_name'] = user.name
                request.session['user_id'] = user.id
                return redirect('/user/list/')
            elif user.limit == 1:
                request.session['user_name'] = user.name
                request.session['user_id'] = user.id
                return redirect('/user/info/')
            else:

                return HttpResponse('Invalid user limit')

        except models.UserInfo.DoesNotExist:
            # 如果用户不存在或密码不匹配，返回错误消息
            return HttpResponse('Invalid ID or password')

    return render(request, 'login.html')


def logout(request):
    # 清除会话中的 user_name
    request.session.pop('user_name', None)
    request.session.pop('user_id', None)
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
    nnid = request.GET.get('nid')
    if nnid == '1':
        queryset = models.UserInfo.objects.all()
        nnid = '0'
    else:
        queryset = models.UserInfo.objects.filter(condition=0)
        nnid = '1'

    return render(request, 'user_list.html', locals())


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
    age = request.POST.get("age")
    salary = request.POST.get("salary")
    degree = request.POST.get("degree")
    marriage = request.POST.get("marriage")
    create_time = request.POST.get("create_time")
    jobtitle = request.POST.get("jobtitle")
    depart = request.POST.get("depart")
    post = request.POST.get("post")
    condition = request.POST.get("condition")
    # 获取用户提交的标题并修改
    models.UserInfo.objects.filter(id=nid).update(name=name, sex=sex, age=age, salary=salary,
                                    degree=degree, marriage=marriage, create_time=create_time, jobtitle=jobtitle,
                                    depart_id=depart, post=post, condition=condition)

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



def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = models.UserInfo.objects.get(id=request.session['user_id'])
            if user.password == current_password:
                if new_password == confirm_password:
                    # 更新用户的新密码

                    user.password = new_password
                    user.save()  # 保存更改

                    return redirect('/user/list/')
                else:
                    return HttpResponse('新密码与确认密码不匹配！')
            else:
                return HttpResponse('原密码输入错误！')
        except models.UserInfo.DoesNotExist:
            return HttpResponse('用户不存在！')

    return render(request, 'change_password.html')


def user_change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = models.UserInfo.objects.get(id=request.session['user_id'])
            if user.password == current_password:
                if new_password == confirm_password:
                    # 更新用户的新密码

                    user.password = new_password
                    user.save()  # 保存更改

                    return redirect('/user/list/')
                else:
                    return HttpResponse('新密码与确认密码不匹配！')
            else:
                return HttpResponse('原密码输入错误！')
        except models.UserInfo.DoesNotExist:
            return HttpResponse('用户不存在！')

    return render(request, 'user_change_password.html')

def user_info(request):
    """个人信息"""

    queryset = models.UserInfo.objects.filter(id=request.session['user_id'])


    return render(request, 'user_info.html', {'queryset': queryset})


def user_info_edit(request):
    """编辑个人信息"""
    if request.method == "GET":
        # 根据nid，获取他的数据
        queryset = models.Department.objects.all()
        row_object = models.UserInfo.objects.get(id=request.session['user_id'])
        ctime = row_object.create_time.strftime("%Y-%m-%d")
        return render(request, "user_info_edit.html", locals())

    name = request.POST.get("name")
    sex = request.POST.get("sex")
    age = request.POST.get("age")
    degree = request.POST.get("degree")
    marriage = request.POST.get("marriage")

    # 获取用户提交的标题并修改
    models.UserInfo.objects.filter(id=request.session['user_id']).update(name=name, sex=sex, age=age,degree=degree, marriage=marriage)

    return redirect("/user/info/")


def user_check_salary(request):
    # 获取用户信息
    user = models.UserInfo.objects.get(id=request.session['user_id'])
    base_salary = user.salary

    # 获取奖励和惩罚记录
    rewards_and_punishments = models.RewardsAndPunishments.objects.filter(uid=request.session['user_id'])

    # 按月汇总
    salary_summary = rewards_and_punishments.annotate(
        year=ExtractYear('time'),
        month=ExtractMonth('time')
    ).values('year', 'month').annotate(
        total_rewards=Sum('amount', filter=Q(isrewards=True)),
        total_penalties=Sum('amount', filter=Q(isrewards=False))
    ).order_by('year', 'month')

    # 计算每个月的总工资
    monthly_salaries = []
    for entry in salary_summary:
        year = entry['year']
        month = entry['month']
        total_rewards = entry['total_rewards'] or 0
        total_penalties = entry['total_penalties'] or 0
        total_salary = base_salary + total_rewards - total_penalties

        monthly_salaries.append({
            'year': year,
            'month': month,
            'base_salary': base_salary,
            'total_rewards': total_rewards,
            'total_penalties': total_penalties,
            'total_salary': total_salary
        })

    return render(request, 'user_salary.html', {'monthly_salaries': monthly_salaries})


def month_details(request, year, month):
    user = request.session.get('user_id')
    # 获取指定月份的奖励和惩罚记录
    details = models.RewardsAndPunishments.objects.filter(
        uid=user,
        time__year=year,
        time__month=month
    )

    return render(request, 'month_details.html', {'details': details, 'year': year, 'month': month})

def rewards_list(request):
    """用户管理"""

    # 获取所有的用户信息 [obj, obj ……]
    # queryset = models.UserInfo.objects.all()
    queryset = models.RewardsAndPunishments.objects.select_related('uid').order_by('time')

    return render(request, 'rewards_list.html', {'queryset': queryset})


def rewards_add(request):
    """添加部门"""
    now = datetime.now()
    ctime = now.strftime("%Y-%m-%dT%H:%M")
    queryset = models.RewardsAndPunishments.objects.all()
    if request.method == "GET":
        return render(request, 'rewards_add.html', locals())
    # 获取用户POST传过来的数据(暂时不考虑为空的情况)
    id = request.POST.get("id")
    isr = request.POST.get("isrewards")
    amount = request.POST.get("amount")
    text = request.POST.get("text")

    time = request.POST.get("time")

    # 保存到数据库
    models.RewardsAndPunishments.objects.create(uid_id=id, isrewards=isr, amount=amount, text=text, time=time)
    # 重定向回到部门列表
    return redirect("/rewards/list/")