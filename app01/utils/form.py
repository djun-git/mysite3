
from app01 import models


from app01.utils.bootstrap import BootStrapModelForm
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class UserModelForm(BootStrapModelForm):
    #自定义数据有效性
    # name = forms.CharField(
    #     min_length=3,
    #     label="用户名称"
    # )

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }





class PrettyModeForm(BootStrapModelForm):
    #验证有效性方法一
    num = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1\d{10}$',"正则，手机号格式错误")]
    )


    class Meta:
        model =models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        fields = ["num","price","level","status"]


    # 验证有效性方法二
    def clean_num(self):
        txt_num = self.cleaned_data["num"]

        exists = models.PrettyNum.objects.filter(num=txt_num).exists()
        if exists:
            raise ValidationError("钩子验证，手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_num




class PrettyEditModelForm(BootStrapModelForm):

    # num = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$',"正则验证，手机号格式错误"),]
    # )

    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        # exclude = ['level']
        fields = ["num", "price", "level", "status"]



    # 验证有效性方法二
    def clean_num(self):
        txt_num = self.cleaned_data['num']
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(num = txt_num).exists()
        if exists:
            raise ValidationError("钩子验证，手机号已存在")
        return txt_num