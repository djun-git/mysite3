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
from django.utils.safestring import mark_safe

def timu(request):
    form2  =[]
    form1= models.Timu.objects.all()
    for x in form1:
        form2.append(mark_safe(x.timu))
        # form=mark_safe("".join(form2))

    return render(request,'timu.html',{'form':form2})