from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    # views_name={"title":"asdasdasd"}
    views_name=0
    return render(request,'dark52.html',{"name":views_name})
# "name":views_name html变量名->views变量名