from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import PrettyModeForm,PrettyEditModelForm



def admin_list(request):
    """管理员列表"""

    # #检查用户是否登录，一登录，------未登录，跳转到登录页面
    # #用户法连请求，获取cookie随机字符串，拿来随机字符串看是否有session中
    # #request.session["info"]
    # info = request.session.get("info")
    # if not info:
    #     return redirect("/login/")

    # info_dict = request.session["info"]


    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_dict)

    #分页
    page_object = Pagination(request,queryset)

    context = {
        "search_data":search_data,
        "queryset":page_object.page_queryset,
        "page_string": page_object.html()
    }

    return render(request,'admin_list.html',context)


from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label = "确认密码",
        widget = forms.PasswordInput(render_value=True)#密码错误后仍然返回密码到客户端
    )

    class Meta:
        model = models.Admin
        fields = ["username","password","confirm_password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise  ValidationError("密码不一致")
        return confirm

def admin_add(request):
    """添加管理员"""

    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request,'add.html',{"form":form,"title":"添加管理员"})

    form = AdminModelForm(data = request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # {'username': 'sdfasdfasdf345345', 'password': '3453453', 'confirm_password': '345345'}

        form.save()
        return redirect('/admin/list/')
    return render(request,'add.html',{"form":form,"title":title})


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

def admin_edit(request,nid):
    """编辑管理员"""

    row_object = models.Admin.objects.filter(id = nid).first()
    if not row_object:
        #return redirect('/admin/list/')
        return render(request,'error.html',{"msg":"检索数据不存在，或许已被别人删除！！！"})
    title = "编辑管理员"

    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request,'add.html',{"form":form,"title":title})
    form = AdminEditModelForm(data = request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request,'add.html',{"form":form,"title":title})


def admin_delete(request,nid):
    """删除管理员"""
    models.Admin.objects.filter(id = nid).delete()
    return redirect('/admin/list/')

class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        #防止密码重复
        md5_pwd = md5(pwd)

        #去数据库消炎当前面膜和新输入的密码是否一致
        print("打印是否为id",self.instance.pk)
        exists = models.Admin.objects.filter(id = self.instance.pk,password = md5_pwd).exists()
        if exists:
            raise ValidationError("不能和当前密码一致")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise  ValidationError("密码不一致")
        return confirm


def admin_reset(request,nid):
    """重置密码"""
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = "重置密码 - {}".format(row_object.username)
    if request.method == "GET":

        form = AdminResetModelForm()
        return  render(request,'add.html',{"form":form,"title":title})
    form=AdminResetModelForm(data = request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request,'add.html',{'form':form,'title':title})
