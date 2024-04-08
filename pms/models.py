from django.db import models


# 部门管理
class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="部门", max_length=32)

    class Meta:
        db_table = 'department'


# 员工管理
class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    sex_choice = {
        (0, "男"),
        (1, "女")
    }
    sex = models.SmallIntegerField(verbose_name="性别", choices=sex_choice)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    # 总长度是10，小数位是2, 默认值是0
    salary = models.DecimalField(verbose_name="基础工资", max_digits=10, decimal_places=2, default=0)
    degree = models.CharField(verbose_name="学历",max_length=8)
    marriage_choice = {
        (0, "未婚"), (1, "已婚")
    }
    marriage = models.SmallIntegerField(verbose_name="性别", choices=marriage_choice)
    create_time = models.DateTimeField(verbose_name="入职时间")
    jobtitle = models.CharField(verbose_name="职称", max_length=8)
    depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    post = models.CharField(verbose_name="岗位", max_length=16)
    condition_choice = {
        (0, "在职"), (1, "辞职"), (2, "辞退"), (3, "退休"), (4, "转出")
    }
    condition = models.SmallIntegerField(verbose_name="状态", choices=condition_choice)

    class Meta:
        db_table = 'person'


class Rewards(models.Model):
    uid = models.ForeignKey(UserInfo, to_field="id", on_delete=models.CASCADE)
    reward = models.IntegerField(verbose_name="奖金")
    time = models.DateTimeField(verbose_name="时间")

    class Meta:
        db_table = 'rewards'


class Punishments(models.Model):
    uid = models.ForeignKey(UserInfo, to_field="id", on_delete=models.CASCADE)
    punishment = models.IntegerField(verbose_name="罚款")
    time = models.DateTimeField(verbose_name="时间")

    class Meta:
        db_table = 'punishments'


