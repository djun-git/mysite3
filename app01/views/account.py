import platform
from io import BytesIO

from django.shortcuts import render, redirect,HttpResponse
from django.core.exceptions import ValidationError
from django import forms

from app01.utils.bootstrap import BootStrapForm
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import PrettyModeForm,PrettyEditModelForm
from app01.utils.encrypt import md5


from app01.utils.code import check_code

# class LoginForm (forms.Form):
#     #从数据库拿数据
#     username = forms.CharField(
#         label = "用户名",
#         widget=forms.TextInput(attrs={"class":"form-control"})
#     )
#     password = forms.CharField(
#         label= "密码",
#         widget=forms.PasswordInput(attrs={"class":"form-control"})
#     )

# #用于和form做对比
# class LoginModelForm (forms.ModelForm):
#     #从数据库拿数据
#     class Meta:
#         model = models.Admin
#         fields = ['username','password']

class LoginForm (BootStrapForm):
    #从数据库拿数据
    username = forms.CharField(
        label = "用户名",
        widget=forms.TextInput,
        required = True,
    )
    password = forms.CharField(
        label= "密码",
        widget=forms.PasswordInput,
        required=True,
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request,'login.html',{'form':form})

    form = LoginForm(data = request.POST)
    if form.is_valid():
        #admin_object = models.Admin.objects.filter(username=form.cleaned_data['username'],password=form.cleaned_data['password']).first()
        #user_input_code = form.cleaned_data['code']

        #验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get("image_code","")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")

            return render(request, 'login.html', {'form': form})



        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("username", "用户名或者密码错误")
            #form.add_error("password", "用户名或者密码错误")
            return render(request,'login.html',{'form':form})
        #用户名和密码正确
        #网站生成随机字符串，写到用户浏览器的cookie中，在写入到session中
        request.session["info"] = {'id': admin_object.id,'name':admin_object.username}
        #session 可以保存七天，七天不需要登录
        request.session.set_expiry(60*60*24*7)
        return redirect("/admin/list/")
    return render(request,'login.html',{'form':form})



def image_code(request):
    """生成图片验证码"""
    #调用plw函数，生成图片

    img, code_string = check_code()
    print(code_string)

    #写入到用户登录时产生的session中
    request.session['image_code']= code_string
    #给session设置60秒超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream,'png')
    return HttpResponse(stream.getvalue())



def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')