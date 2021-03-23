from django.http import HttpResponse
from django.shortcuts import render
import datetime
from py2neo import Graph, Node, Relationship
import json
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
    # return render(request, 'testasd.html')

def echarts(request):
    return render(request,'templates/echarts.min.js')
def index(request):
    if  request.method == 'POST':
        username = request.POST.get('username')
        
        # cypher_1="MATCH (n) RETURN n LIMIT 25"
        cypher_1="MATCH p=()-->() RETURN p LIMIT 25"
        # cypher_1 = "MATCH (m:person{name:'"+username+"'}) RETURN m"
        # 通过cypher语句访问neo4j数据库
        nodes_data = graph.run(cypher_1 ).data()
        # return render(request, 'testasd.html',{"data":json.dumps(nodes_data,ensure_ascii=False)})
        # return render(request, 'testasd.html',{"data_name":json.dumps(nodes_data[0]['m']['name'],ensure_ascii=False),"others_1":json.dumps(nodes_data[0]['m']['age'],ensure_ascii=False)})
        tmp=str(nodes_data[0]['p'])
        for i in range(len(tmp)):
            if  tmp[i]=='(':
                from_name_left=i
            elif tmp[i]==')':
                from_name_right=i
                break
        for i in range(20,len(tmp)):
            if  tmp[i]=='(':
                to_name_left=i
            elif tmp[i]==')':
                to_name_right=i
                break
        tmp1=tmp[from_name_left+1:from_name_right]
        tmp2=tmp[to_name_left+1:to_name_right]
        return render(request, 'testasd.html',{"relations_from":json.dumps(tmp1,ensure_ascii=False),"relations_to":json.dumps(tmp2,ensure_ascii=False)})
        # return HttpResponse([tmp[from_name_left+1:from_name_right],tmp[to_name_left+1:to_name_right]])
        # return HttpResponse(tmp[to_name_left+1:to_name_right])
        # return HttpResponse(tmp)
#render返回渲染后的httpresponse对象
# "name":views_name html变量名->views变量名
#Django 会自动对 views.py 传到HTML文件中的标签语法进行转义，令其语义失效。加 safe 过滤器是告诉 Django 该数据是安全的，不必对其进行转义，可以让该数据语义生效。