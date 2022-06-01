from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination

from app01.utils.form import PrettyModeForm,PrettyEditModelForm




def pretty_list(request):
    """靓号列表"""
    data_dict = {}
    search_data = request.GET.get('q',"")
    if search_data:
        data_dict["num__contains"]=search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request,queryset)


    context = {
        "search_data": search_data,
        'queryset': page_object.page_queryset, # 分完页的数据
        'page_string': page_object.html() #页码
    }

    return render(request, "pretty_list.html",
                  context)



def pretty_add(request):
    if request.method == "GET":
        form = PrettyModeForm()
        return render(request,'pretty_add.html',{"form":form})
    form = PrettyModeForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request,'pretty_add.html',{"form":form})





def pretty_edit(request,nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request,'pretty_edit.html',{'form':form})
    form = PrettyEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request,'pretty_edit.html',{'form':form})

def pretty_delete(request):
    nid= request.GET.get("nid")
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
