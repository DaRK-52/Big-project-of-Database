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
# 搜索直接存在的关系

def search_relation(name1,name2):
    return "MATCH (name1: person {name: '"+name1+"'}),(name2: person {name: '"+name2+"'}),p = shortestPath((name1)-[*..15]-(name2)) RETURN p"

def search_node(name):
    return "MATCH (n{name:'"+name+"'}) RETURN n"

def extract_node(str_node):
    count=0
    for i in range(len(str_node)):
        if str_node[i]=='\'':
            count+=1
            if count==5:
                name1_left=i
            elif count==6:
                name1_right=i
            elif count==11:
                name2_left=i
            elif count==12:
                name2_right=i
# 记录两个名字分别的左右端位置
    return str_node[name1_left+1:name1_right],str_node[name2_left+1:name2_right]
#提取关系的两个名字（虽然直接拿输入也行）

def extract_nation(str_node):
    count=0
    for i in range(len(str_node)):
        if str_node[i]=='\'':
            count+=1
            if count==7:
                name1_left=i
            elif count==8:
                name1_right=i
            elif count==13:
                name2_left=i
            elif count==14:
                name2_right=i
# 记录两个国籍分别的左右端位置
    return str_node[name1_left+1:name1_right],str_node[name2_left+1:name2_right]
#提取两个名字的国籍

def extract_relation(str_relation):
    count=0
    rela_left=[]
    rela_right=[]
    rela=''
    for i in range(len(str_relation)):
        if str_relation[i]==':':
            count+=1
            rela_left.append(i)
        elif str_relation[i]=='{':
            rela_right.append(i)
    for i in range(0,count):
        rela+=str_relation[rela_left[i]+1:rela_right[i]]
    return rela

def extract_call(str_relation,str_sex):
    gen=0
    call={(0,'male'):'cousin',(0,'female'):'cousin',(1,'male'):'nephew',(1,'female'):'niece',(2,'male'):'grandson',(3,'male'):'great-grandson',(4,'male'):'great-great-grandson',(5,'male'):'great-great-great-grandson',
    (2,'female'):'granddaughter',(3,'female'):'great-granddaughter',(4,'female'):'great-great-granddaughter',(5,'female'):'great-great-great-granddaughter',
    (8,'female'):'aunt',(9,'female'):'wife',(10,'female'):'daughter in law'}
    for i in range(len(str_relation)):
        if  str_relation[i]=='s':
            gen+=1
            i+=2
        elif str_relation[i]=='d':
            gen+=1
            i+=7
        elif str_relation[i]=='b':
            i+=6
        elif str_relation[i]=='f':
            gen-=1
            i+=5
        elif str_relation[i]=='w':
            gen+=10
            i+=3
    return call[(gen,str_sex)]

def index(request):
    if  request.method == 'POST':
        character_1 = request.POST.get('character_1')
        character_2 = request.POST.get('character_2')
        cypher_name=search_node(str(character_1))
        character_1_data=graph.run(cypher_name ).data()
        cypher_name=search_node(str(character_2))
        character_2_data=graph.run(cypher_name ).data()
        # cypher_1="MATCH ({name: 'Jonathan'})-[r]-({name:'Kujo Jotaro'}) RETURN type(r)"
        # cypher_1=search_direct_relation(character_1,character_2)
        # 查询两个之间的关系
        # 通过cypher语句访问neo4j数据库
        cypher_1=search_relation(character_1,character_2)
        nodes_data = graph.run(cypher_1 ).data()
        tmp=str(nodes_data[0]['p'])
        relation_name=extract_relation(tmp)
        call=extract_call(relation_name,character_2_data[0]['n']['sex'])
        # 转为字符串进行处理
        # return HttpResponse(nodes_data[0]['p'])
        # return HttpResponse(relation_name)
        # 节点与关系

        name1=character_1_data[0]['n']['name']
        name2=character_2_data[0]['n']['name']
        nationality1=character_1_data[0]['n']['nationality']
        nationality2=character_2_data[0]['n']['nationality']
        sex1=character_1_data[0]['n']['sex']
        sex2=character_2_data[0]['n']['sex']
        nationality1+=','
        nationality2+=','
        nationality1+=sex1
        nationality2+=sex2
        #关系计算定义son,daughter,grandson,granddaughter,father,mother,grandfather,grandmother,wife,husband为元关系
        # return render(request,'testasd.html',{"name_1":json.dumps(name1,ensure_ascii=False),"name_2":json.dumps(name2,ensure_ascii=False),"nation_1":json.dumps(nationality1,ensure_ascii=False),"nation_2":json.dumps(nationality2,ensure_ascii=False),"relation":json.dumps(relation_name,ensure_ascii=False)})
        return render(request,'testasd.html',{"name_1":json.dumps(name1,ensure_ascii=False),"name_2":json.dumps(name2,ensure_ascii=False),"nation_1":json.dumps(nationality1,ensure_ascii=False),"nation_2":json.dumps(nationality2,ensure_ascii=False),"relation":json.dumps(call,ensure_ascii=False)})
        # return render(request, 'testasd.html',{"relations_from":json.dumps(tmp1,ensure_ascii=False),"relations_to":json.dumps(tmp2,ensure_ascii=False)})
        # return HttpResponse(tmp[from_name_left+1:from_name_right])
#render返回渲染后的httpresponse对象