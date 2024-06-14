from django import forms
from .models import Department

class EmployeeSearchForm(forms.Form):
    ATTRIBUTE_CHOICES = [
        ('id', '工号'),
        ('name', '姓名'),
        ('sex', '性别'),
        ('age', '年龄'),
        ('salary', '基础工资'),
        ('degree', '学历'),
        ('marriage', '婚姻状况'),
        ('create_time', '入职时间'),
        ('jobtitle', '职称'),
        ('depart', '部门'),
        ('post', '岗位'),
        ('condition', '状态'),
        ('limit', '权限'),
    ]

    attribute = forms.ChoiceField(choices=ATTRIBUTE_CHOICES)

    DEPARTMENT_CHOICES = [(dept.id, dept.title) for dept in Department.objects.all()]

    sex = forms.ChoiceField(choices=[(0, '男'), (1, '女')], required=False)
    marriage = forms.ChoiceField(choices=[(0, '未婚'), (1, '已婚')], required=False)
    condition = forms.ChoiceField(choices=[(0, '在职'), (1, '辞职'), (2, '辞退'), (3, '退休'), (4, '转出')], required=False)
    limit = forms.ChoiceField(choices=[(0, 'admin'), (1, 'user')], required=False)
    depart = forms.ChoiceField(choices=DEPARTMENT_CHOICES, required=False)

    salary_operator = forms.ChoiceField(choices=[('gt', '大于'), ('lt', '小于'), ('eq', '等于')], required=False)
    salary = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    age_operator = forms.ChoiceField(choices=[('gt', '大于'), ('lt', '小于'), ('eq', '等于')], required=False)
    age = forms.IntegerField(required=False)

    create_time_operator = forms.ChoiceField(choices=[('gt', '大于'), ('lt', '小于'), ('eq', '等于')], required=False)
    create_time = forms.DateField(required=False)

    name = forms.CharField(max_length=16, required=False)
    id = forms.CharField(max_length=16, required=False)
    jobtitle = forms.CharField(max_length=8, required=False)
    post = forms.CharField(max_length=16, required=False)
    degree = forms.CharField(max_length=8, required=False)
    email = forms.EmailField(required=False)
