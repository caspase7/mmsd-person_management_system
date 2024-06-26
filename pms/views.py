from django.shortcuts import render, redirect
from django.http import HttpResponse
from pms import models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
# Create your views here.
from .forms import EmployeeSearchForm
from .models import UserInfo, Department
from django.db.models import Q
import json
from django.http import HttpResponse
import pandas as pd
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

                    return redirect('/user/info/')
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



def get_month_range(start_date, end_date):
    """生成从入职时间到当前时间的所有月份"""
    current = start_date.replace(day=1)
    while current <= end_date:
        yield current
        next_month = current.month % 12 + 1
        next_year = current.year + current.month // 12
        current = current.replace(year=next_year, month=next_month)

def user_check_salary(request):
    # 获取用户信息
    user = models.UserInfo.objects.get(id=request.session['user_id'])
    base_salary = user.salary

    # 获取用户的入职时间
    hire_date = user.create_time
    current_date = datetime.now().date()

    # 获取奖励和惩罚记录
    rewards_and_punishments = models.RewardsAndPunishments.objects.filter(uid=request.session['user_id'])

    # 按月汇总并按年份和月份倒序排列
    salary_summary = rewards_and_punishments.annotate(
        year=ExtractYear('time'),
        month=ExtractMonth('time')
    ).values('year', 'month').annotate(
        total_rewards=Sum('amount', filter=Q(isrewards=True)),
        total_penalties=Sum('amount', filter=Q(isrewards=False))
    ).order_by('-year', '-month')

    # 生成从入职时间到当前时间的所有月份并倒序
    month_range = list(get_month_range(hire_date, current_date))[::-1]

    # 构建字典以便快速查找
    summary_dict = {(entry['year'], entry['month']): entry for entry in salary_summary}

    # 计算每个月的总工资
    monthly_salaries = []
    for month in month_range:
        year = month.year
        month_num = month.month
        entry = summary_dict.get((year, month_num), {})
        total_rewards = entry.get('total_rewards', 0) or 0
        total_penalties = entry.get('total_penalties', 0) or 0
        total_salary = base_salary + total_rewards - total_penalties

        monthly_salaries.append({
            'year': year,
            'month': month_num,
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

    queryset = models.RewardsAndPunishments.objects.select_related('uid').order_by('time')

    return render(request, 'rewards_list.html', {'queryset': queryset})


def rewards_add(request):
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

    return redirect("/rewards/list/")


def user_search(request):
    # queryset = models.Department.objects.all()
    # if request.method == "GET":
    # return render(request, 'user_search.html', {'queryset': queryset})
    if request.method == 'POST':
        form = EmployeeSearchForm(request.POST)
        employees = UserInfo.objects.all()

        criteria_count = int(request.POST.get('criteria_count', 0))
        query = Q()
        for i in range(criteria_count):
            attribute = request.POST.get(f'attribute_{i}')
            # print(attribute)
            if attribute == 'sex':
                value = request.POST.get(f'sex_{i}')
                query &= Q(sex=value)
            elif attribute == 'marriage':
                value = request.POST.get(f'marriage_{i}')
                query &= Q(marriage=value)
            elif attribute == 'condition':
                value = request.POST.get(f'condition_{i}')
                query &= Q(condition=value)
            elif attribute == 'limit':
                value = request.POST.get(f'limit_{i}')
                query &= Q(limit=value)
            elif attribute == 'depart':
                value = request.POST.get(f'depart_{i}')
                query &= Q(depart=value)
            elif attribute == 'salary':
                operator = request.POST.get(f'salary_operator_{i}')
                value = request.POST.get(f'salary_{i}')
                if operator == 'gt':
                    query &= Q(salary__gt=value)
                elif operator == 'lt':
                    query &= Q(salary__lt=value)
                elif operator == 'eq':
                    query &= Q(salary=value)
            elif attribute == 'age':
                operator = request.POST.get(f'age_operator_{i}')
                value = request.POST.get(f'age_{i}')
                if operator == 'gt':
                    query &= Q(age__gt=value)
                elif operator == 'lt':
                    query &= Q(age__lt=value)
                elif operator == 'eq':
                    query &= Q(age=value)
            elif attribute == 'create_time':
                operator = request.POST.get(f'create_time_operator_{i}')
                value = request.POST.get(f'create_time_{i}')
                if operator == 'gt':
                    query &= Q(create_time__gt=value)
                elif operator == 'lt':
                    query &= Q(create_time__lt=value)
                elif operator == 'eq':
                    query &= Q(create_time=value)
            else:
                value = request.POST.get(f'{attribute}_{i}')
                if attribute in ['id', 'name', 'jobtitle', 'post', 'degree']:
                    query &= Q(**{f'{attribute}__icontains': value})

        employees = employees.filter(query)
        employees_data = []
        for employee in employees:
            employee_dict = {
                'id': employee.id,
                'name': employee.name,
                'sex': employee.get_sex_display(),
                'password': employee.password,
                'age': employee.age,
                'salary': float(employee.salary),
                'degree': employee.degree,
                'marriage': employee.get_marriage_display(),
                'create_time': employee.create_time.strftime('%Y-%m-%d'),  # 将日期格式化为字符串
                'jobtitle': employee.jobtitle,
                'depart': employee.depart.title if employee.depart else None,  # 如果部门存在，获取部门名称，否则为 None
                'post': employee.post,
                'condition': employee.get_condition_display(),
                'limit': employee.get_limit_display(),
                # 其他字段...
            }
            employees_data.append(employee_dict)

        # 将查询结果存储到 session 中
        request.session['search_results'] = employees_data
        # request.session['search_results'] = list(employees.values())  # 将查询结果存储到 session 中

        return render(request, 'result.html', {'employees': employees})
    else:
        form = EmployeeSearchForm()
        departments = Department.objects.all()
        department_choices = [(dept.id, dept.title) for dept in departments]
        department_choices_json = json.dumps(department_choices)

    return render(request, 'user_search.html', {'form': form, 'department_choices_json': department_choices_json})


def export_to_excel(request):
    employees = request.session.get('search_results', {})
    df = pd.DataFrame(employees)
    print("DataFrame contents:", df)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="employees.xlsx"'
    df.to_excel(response, index=False)
    return response

