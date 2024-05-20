from django.db import models
from datetime import datetime


# 部门管理
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="部门", max_length=32)

    class Meta:
        db_table = 'department'


# 员工管理
class UserInfo(models.Model):
    """员工表"""
    id = models.CharField(verbose_name="工号", max_length=16, primary_key=True)
    name = models.CharField(verbose_name="姓名", max_length=16, null=True, blank=True)
    sex_choice = {
        (0, "男"),
        (1, "女")
    }
    sex = models.SmallIntegerField(verbose_name="性别", choices=sex_choice, null=True, blank=True)
    password = models.CharField(verbose_name="密码", max_length=64, default="1234")
    age = models.IntegerField(verbose_name="年龄", null=True, blank=True)
    # 总长度是10，小数位是2, 默认值是0
    salary = models.DecimalField(verbose_name="基础工资", max_digits=10, decimal_places=2, default=0)
    degree = models.CharField(verbose_name="学历", max_length=8, default="本科")
    marriage_choice = {
        (0, "未婚"), (1, "已婚")
    }
    marriage = models.SmallIntegerField(verbose_name="婚姻状况", choices=marriage_choice, default=0, null=True, blank=True)
    create_time = models.DateField(verbose_name="入职时间")
    jobtitle = models.CharField(verbose_name="职称", max_length=8, null=True, blank=True)
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    post = models.CharField(verbose_name="岗位", max_length=16, null=True, blank=True)
    condition_choice = {
        (0, "在职"), (1, "辞职"), (2, "辞退"), (3, "退休"), (4, "转出")
    }
    condition = models.SmallIntegerField(verbose_name="状态", choices=condition_choice, default=0)
    limit_choice = {
        (0, "admin"), (1, "user")
    }
    limit = models.SmallIntegerField(verbose_name="权限", choices=limit_choice, default=1)

    class Meta:
        db_table = 'person'


class RewardsAndPunishments(models.Model):
    uid = models.ForeignKey(UserInfo, to_field="id", on_delete=models.CASCADE)
    isrewards = models.BooleanField(verbose_name="是奖金", null=True, blank=True)
    amount = models.IntegerField(verbose_name="数额")
    text = models.TextField(verbose_name="说明", null=True)
    time = models.DateTimeField(verbose_name="时间")

    class Meta:
        db_table = 'rewardsandpunishments'




