from django.db import models

class Department(models.Model):
    """部门表格"""
    #id = models.BigAutoField(verbose_name= 'ID', primary_key = True)
    title = models.CharField(verbose_name= "标题",max_length=32)

    def __str__(self):
        return self.title


# class yuangong(models.Model):
#     """员工表"""
#     #id = models.BigAutoField(verbose_name= 'ID', primary_key = True)
#     title = models.CharField(verbose_name= "标题",max_length=32)

class UserInfo(models.Model):
    """用户表"""
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额",max_digits=10, decimal_places=2, default=0)
    #create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")


    depart = models.ForeignKey(verbose_name="部门",to='Department',null=True, blank=True,to_field='id', on_delete=models.CASCADE)

    gender_choices = (
        (1,"男"),
        (2,"女"),
    )

    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)


class PrettyNum(models.Model):
    """靓号管理"""
    num= models.CharField(verbose_name="手机号",max_length=16)
    price = models.IntegerField(verbose_name="价格",default=0)

    level_chaoices = (
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_chaoices,default=1)

    status_choices=(
        (0,"未占用"),
        (1,"已占用"),
    )

    status = models.BooleanField(verbose_name="状态",choices=status_choices,default=0)


class Admin(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)

    def __str__(self):
        return self.username


class Task(models.Model):
    """任务"""
    level_choices = (
        (1,"紧急"),
        (2,"重要"),
        (3,"临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choices,default=3)
    title = models.CharField(verbose_name="标题",max_length=64)
    detail = models.TextField(verbose_name="详细信息")

    user = models.ForeignKey(verbose_name="负责人",to="Admin",on_delete=models.CASCADE)


class Order(models.Model):
    """ 订单"""
    oid = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="商品名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choices = (
        (0,"待支付"),
        (1,"已支付"),
    )
    status = models.BooleanField(verbose_name="订单状态",choices=status_choices,default=0)
    admin  = models.ForeignKey(verbose_name="管理员",to = "Admin",on_delete=models.CASCADE)


class Timu(models.Model):
    timu = models.CharField(verbose_name="题目",max_length=1000)
