from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    views_name="Helloqaq"
    return render(request,'dark52.html',{"name":views_name})
# "name":views_name html变量名->views变量名