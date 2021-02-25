from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    # views_name={"title":"asdasdasd"}
    views_name=50
    her=50
    return render(request,'dark52.html',{"name":views_name,"her":her})
#render返回渲染后的httpresponse对象
# "name":views_name html变量名->views变量名
#Django 会自动对 views.py 传到HTML文件中的标签语法进行转义，令其语义失效。加 safe 过滤器是告诉 Django 该数据是安全的，不必对其进行转义，可以让该数据语义生效。