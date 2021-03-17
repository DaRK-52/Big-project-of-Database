from django.http import HttpResponse
from django.shortcuts import render
import datetime
from py2neo import Graph, Node, Relationship
# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph("http://localhost:7474", username="neo4j", password='Accelerator2')


from django.http import HttpResponseRedirect

def create_blogpost(request):
    if request.method == 'POST':
        BlogPost(
            title=request.POST.get('title'),
            body=request.POST.get('body'),
            timestamp=datetime.now()
        ).save()
    return HttpResponseRedirect('/HelloWorld/')

def login(request):
    return render(request,'login.html')
def inp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    return render(request,'archive.html')

def hello(request):
    # views_name={"title":"asdasdasd"}
    views_name=50
    her=50
    return render(request,'dark52.html',{"name":views_name,"her":her})

def time(request):
    now = datetime.datetime.now()
    html = '现在的时间为%s'%now
    return HttpResponse(html)

def index(request):
    if  request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cypher_1 = "MATCH (m:person{name:'"+username+"'}) RETURN m"
        # 通过cypher语句访问neo4j数据库
        # cypher_1 = "MATCH (m:person{name:'bobo'}) return m"
        nodes_data = graph.run(cypher_1 ).data()
        # return render(request, nodes_data)
        return HttpResponse(nodes_data)
#render返回渲染后的httpresponse对象
# "name":views_name html变量名->views变量名
#Django 会自动对 views.py 传到HTML文件中的标签语法进行转义，令其语义失效。加 safe 过滤器是告诉 Django 该数据是安全的，不必对其进行转义，可以让该数据语义生效。