from django.http import HttpResponse
from django.shortcuts import render
import datetime
from py2neo import Graph, Node, Relationship
import json
# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph("http://localhost:7474", username="neo4j", password='Accelerator2')


from django.http import HttpResponseRedirect

def login(request):
    return render(request,'login.html')
def echarts(request):
    return render(request,'templates/echarts.min.js')


def search_direct_relation(name1,name2):
    return "MATCH ({name: '"+name1+"'})-[r]-({name:'"+name2+"'}) RETURN r,type(r)"

def index(request):
    if  request.method == 'POST':
        character_1 = request.POST.get('character_1')
        character_2 = request.POST.get('character_2')
        # cypher_1="MATCH p=()-->() RETURN p LIMIT 25"
        # cypher_1="MATCH ({name: 'Jonathan'})-[r]-({name:'Kujo Jotaro'}) RETURN type(r)"
        # cypher_1="MATCH ({name: '"+character_1+"'})-[r]-({name:'"+character_2+"'}) RETURN r,type(r)"
        cypher_1=search_direct_relation(character_1,character_2)
        # 查询两个之间的关系
        # 通过cypher语句访问neo4j数据库
        nodes_data = graph.run(cypher_1 ).data()
        return HttpResponse(nodes_data)
        # return render(request, 'testasd.html',{"data_name":json.dumps(nodes_data[0]['m']['name'],ensure_ascii=False),"others_1":json.dumps(nodes_data[0]['m']['age'],ensure_ascii=False)})
        tmp=str(nodes_data[0]['p'])
        # 将cypher语句返回过来的东西字符串化，然后从中提取出想要的东西
        for i in range(len(tmp)):
            if  tmp[i]=='(':
                from_name_left=i
            elif tmp[i]==')':
                from_name_right=i
                break
        p=i
        # p是上次搜到的i的位置
        for i in range(p,len(tmp)):
            if  tmp[i]=='(':
                to_name_left=i
            elif tmp[i]==')':
                to_name_right=i
                break
        tmp1=tmp[from_name_left+1:from_name_right]
        tmp2=tmp[to_name_left+1:to_name_right]
        return render(request, 'testasd.html',{"relations_from":json.dumps(tmp1,ensure_ascii=False),"relations_to":json.dumps(tmp2,ensure_ascii=False)})
        # return HttpResponse(tmp[from_name_left+1:from_name_right])
#render返回渲染后的httpresponse对象
# "name":views_name html变量名->views变量名
#Django 会自动对 views.py 传到HTML文件中的标签语法进行转义，令其语义失效。加 safe 过滤器是告诉 Django 该数据是安全的，不必对其进行转义，可以让该数据语义生效。