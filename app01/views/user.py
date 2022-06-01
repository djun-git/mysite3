from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination

from app01.utils.form import UserModelForm,PrettyModeForm,PrettyEditModelForm





def user_list(request):
    """用户管理"""
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request,queryset)
    context = {
        "queryset":page_object.page_queryset,
        "page_string":page_object.html()
    }

    return render(request,'user_list.html',context)


################################### ModelForm


def user_add(request):
    """增加用户"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_add.html', {"form": form})

        # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT运维部门>}
        # print(form.cleaned_data)
        # models.UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, "user_add.html", {"form": form})


def user_edit(request,nid):
    """修改用户信息"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":

        form = UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{'form':form})


    form = UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        #form.instanc.字段名= 值
        form.save()
        return redirect('/user/list/')
    return render(request,'user_edit.html',{"form":form})


def user_delete(request):
    nid = request.GET.get('nid')
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')
