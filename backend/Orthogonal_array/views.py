
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
        cluster = MongoClient("mongodb+srv://newuser1:Abuzarm2@cluster0.qqe5xei.mongodb.net/?retryWrites=true&w=majority")
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
        
        file=open('text1.txt','w')
        scenerio="@"+data['tag']+'\n'+"Scenerio Outline:"
        scenerio+=data['scenerio']
        scenerio=scenerio+'\n'

        string1=data['pre']
        string1=string1+'\n'
        string2="""Funrnish the information """
        
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
    return HttpResponse("ok")