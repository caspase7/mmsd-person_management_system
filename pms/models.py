from django.db import models


# 部门管理
class Department(models.Model):
    """部门表"""
    # 没有写id，因为django自动创建id，并且是主键、自增的。这里我们自己写一个
    # id = models.BigAutoField(verbose_name='ID', primary_key=True)
    title = models.CharField(verbose_name="部门", max_length=32)


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
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    degree = models.CharField(verbose_name="学历",max_length=8)
    marriage_choice = {
        (0, "未婚"), (1, "已婚")
    }
    marriage = models.SmallIntegerField(verbose_name="性别", choices=marriage_choice)
    create_time = models.DateTimeField(verbose_name="入职时间")
    jobtitle = models.CharField(verbose_name="职称",max_length=8)
    # 1. 关联Department
    #       -to， 与哪张表关联
    #       -to_field  与表中哪一列关联
    # 2. 在实际生成的时候会自动变成depart_id
    # 3. 如果Department中没有相关id，我们就删除这个部门的员工信息
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # 3.1 如果不想把员工删除，可以将部门id置空
    depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    post = models.CharField(verbose_name="岗位", max_length=16)

    # 约束

