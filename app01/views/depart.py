from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination

from app01.utils.form import UserModelForm,PrettyModeForm,PrettyEditModelForm

def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()

    return render(request,'depart_list.html',{'queryset':queryset})

def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request,'depart_add.html')
    #获取用户POST
    title = request.POST.get("title")

    #保存到数据库
    models.Department.objects.create(title=title)

    return redirect("/depart/list/")

def depart_delete(request):

    """删除部门"""
    #获取id
    nid = request.GET.get("nid")

    #删除
    models.Department.objects.filter(id=nid).delete()


    return redirect("/depart/list/")

def depart_edit(request,nid):
    if request.method =="GET":
        row_object = models.Department.objects.filter(id=nid).first()

        return render(request,'depart_edit.html',{"row_object":row_object})
    title=request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)

    return redirect("/depart/list/")
