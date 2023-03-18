
import json
import re
from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .models import Array
import pymongo

from pymongo import MongoClient

import certifi


from django.views.decorators.csrf import csrf_exempt

def func_generator(keyword,argument,result_file):
    
    structure=keyword+'(\''+argument+'\',()=>{'+'\n'+'})'+'\n'
    result_file.write(structure)

def func_generator_with_variable(keyword,line,result_file):
    variable_string="("
    removing_word_list=[]
    removing_word_list.append(keyword)
    removing_word_list.append(',')
    preced_place_holder=""
    for data in re.findall("<[a-z_0-9]*>", line):
        preced_place_holder=preced_place_holder+"{"+"string"+"},"
        print(preced_place_holder)
        variable_string=variable_string+data[1:-1]+','
        temp="\"<"+data[1:-1]+">\""
        removing_word_list.append(temp)
    preced_place_holder=preced_place_holder[:-1]
    variable_string=variable_string[:-1]+')'
    for rem in removing_word_list:
        if rem in line:
            print("rem:"+rem)
            line=line.replace(rem,"")
    print("precedence:"+preced_place_holder)
    structure=keyword+'(\''+line+preced_place_holder+'\','+variable_string+'=>{'+'\n'+'})'+'\n'
    result_file.write(structure)

# Create your views here.
@csrf_exempt
def myFunc(e):
  return e['rows']
    
@csrf_exempt
def data_operation(request):
    
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        id=data['pattern'] 
        print("length is :"+ str(len(id)))
        print(id)
        cluster = MongoClient("mongodb://localhost:27017")
        db = cluster["test"]
        collection=db["test"]
        result = collection.find_one({"id":id} )
        list_=[]
        if result:
            return HttpResponse(json.dumps({"result":(True,id,result['tab'])}))
        else:
            E_total_factor=0
            list_of_level_pattern=[]
            for i in range(0,len(str(id))):
                if id[i]=='^':
                    list_of_level_pattern.append(int(id[i-1]))
                    E_total_factor+=int(id[i+1])
            list_of_level_pattern.sort()
            print("list_of_level_pattern:"+str(list_of_level_pattern))
            for doc in collection.find({}):
                F_total_factor=0
                for i in range(0,len(doc['id'])):
                    
                    if doc['id'][i]=='^' and int(doc['id'][i-1])>=list_of_level_pattern[0]:

                        F_total_factor+=int(doc['id'][i+1])
                    else:
                        continue
                if F_total_factor>=E_total_factor:
                    list_.append({'id':doc['id'],'tab':doc['tab'],'E_factor':int(E_total_factor),'F_factor':int(F_total_factor),'rows':len(doc['tab'].split("\n"))})
            print("list_:"+str(list_))
            list_.sort(key=myFunc)
           
            return HttpResponse(json.dumps({"result":(False,list_)}))


@csrf_exempt
def bdd(request):
    if request.method=='POST':
        data=json.loads(request.body.decode('utf-8'))
        table_data=data['table_data']
        factor_name=data['column_data']
        
        file=open('text1.feature','w')
        scenerio="@"+data['tag']+'\n'+"Scenario Outline:"
        scenerio+=data['scenerio']
        scenerio=scenerio+'\n'

        string1=data['pre']
        string1=string1+'\n'
        string2="""And Funrnish the information """
        
        for factor in factor_name:
            string2+="\"<"
            string2+=factor
            string2+=">\","
        string2=string2[:-1]
        string2=string2+'\n'
        string3=data['post']
        string3=string3+'\n'+'Examples:'+'\n'
        for i in factor_name:
            string3+='|'
            string3+=i
        string3+='|'
        string3+='\n'
        for line in table_data:
            
            for i in line:
                string3+='|'
                string3+=line[i]
            string3+='|'
            string3+='\n'
        result=scenerio+string1+string2+string3
        file.write(result)
    return HttpResponse(json.dumps({"file_content":result}))

@csrf_exempt
def step_def(request):
    file=json.loads(request.body.decode('utf-8'))
    content=file['file_data']
    
    content=content[:content.find("Examples:")]

    to_iter=content.split("\n")[2:]
    result_file=open('result.js','w')
    for line in to_iter:
        if "Given" in line and len(re.findall("<[a-z_0-9]*>", line))==0 :
            func_generator("Given",line[len("Given"):],result_file)
        elif "And" in line and len(re.findall("<[a-z_0-9]*>", line))==0:
            func_generator("And",line[len("And"):],result_file)
        elif "When" in line and len(re.findall("<[a-z_0-9]*>", line))==0:
            func_generator("When",line[len("When"):],result_file)
        elif "And" in line and len(re.findall("<[a-z_0-9]*>", line))!=0:
            func_generator_with_variable("And",line,result_file)
        elif "Given" in line and len(re.findall("<[a-z_0-9]*>", line))!=0:
            func_generator_with_variable("Given",line,result_file)
        elif "When" in line and len(re.findall("<[a-z_0-9]*>", line))!=0:
            func_generator_with_variable("When",line,result_file)
    result_file.close()
    return HttpResponse("ok")
