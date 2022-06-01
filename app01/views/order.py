import json
import random
from datetime import datetime
from django import forms
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from django.views.decorators.csrf import  csrf_exempt
from app01.utils.pagination import Pagination

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        #fields = "__all__"
        exclude = ['oid','admin']


def order_list(request):
    queryset = models.Order.objects.all().order_by("-id")

    page_object = Pagination(request, queryset)
    form = OrderModelForm()

    context = {
        'form':form,
        'queryset': page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html()  # 页码
    }


    return render(request,'order_list.html',context)


@csrf_exempt
def order_add(request):
    """新建订单（ajax)请求"""
    form = OrderModelForm(data= request.POST)
    if form.is_valid():
        #生成随机的订单号码
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") +str(random.randint(1000,9999))

        #管理员，当前登录系统的管理员
        form.instance.admin_id = request.session["info"]["id"]


        form.save()
        return JsonResponse({"status":True})
        #return HttpResponse(json.dumps({"status":True}))#等价于上一个

    return JsonResponse({"status":False,'error':form.errors})

def order_delete(request):
    """删除订单"""
    uid = request.GET.get("uid")

    models.Order.objects.filter(id = uid).delete()
    return JsonResponse({"status":True})


def order_detail(request):
    """ 根据ID获取订单详细 """
    # 方式1
    """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        }
    }
    return JsonResponse(result)
    """

    # 方式2
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title", 'price', 'status').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})