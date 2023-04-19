import pandas as pd
import json
import re
import os
from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .models import Array
import pymongo
import webbrowser
from pymongo import MongoClient

import certifi


from django.views.decorators.csrf import csrf_exempt

def func_generator_js(keyword,argument,result_file):
    func1=''
    if 'launch' in argument.split(" ") and keyword=="Given":
        func1='ApplicationLaunch()'
    if 'logout' in argument.split(" ") and keyword=="And":
        func1='ApplicationExit()'
    if 'login' in argument.split(" ") and keyword=="When":
        func1='ApplicationLogin()'
    structure=keyword+'(\''+argument.strip()+'\',()=>{'+'\n'+ func1 +'\n'+'})'+'\n'
    result_file.write(structure)

def func_generator_java(keyword,argument,result_file,o_w_f='',param='',returnparam='',flag=False):
    if flag==True:
        if returnparam == 'nan':
            returnparam=''
        else:
            o_w_f=returnparam+'='+o_w_f
        if param=='nan':
            param=''
        
        structure='@'+keyword+'(\"^'+argument.strip()+'$\")\n\t'+'public void '+argument.replace(" ", "_")[1:]+'() throws InterruptedException { '+'\n\t\t'+o_w_f+'('+param+')\n\n\t}\n\n\t'
    else:
        structure='@'+keyword+'(\"^'+argument.strip()+'$\")\n\t'+'public void '+argument.replace(" ", "_")[1:-1]+'() throws InterruptedException { \n\n\t'+returnparam+'}\n\n\t'

    print(structure)
    result_file.write(structure)

def func_generator_cs(keyword,argument,result_file):

    structure='['+keyword+'(@\"'+argument.strip()+'\")]\n\t\t'+'public void '+keyword+argument.replace(" ", "")+'() \n\t\t{\n\n\t\t}\n\n\t\t'
    result_file.write(structure)

def func_generator_with_variable_cs(keyword,line,result_file):
    preced_place_holder=""
    variable_string="("
    removing_word_list=[]
    removing_word_list.append(keyword)
    removing_word_list.append(',')
    for data in re.findall("<[A-Za-z_0-9]*>", line):
        preced_place_holder=preced_place_holder+"\"\"([^\"\"]*)\"\","
        #print(preced_place_holder)
        variable_string=variable_string+'String '+data[1:-1]+','
        temp="\"<"+data[1:-1]+">\""
        removing_word_list.append(temp)
    preced_place_holder=preced_place_holder[:-1]
    variable_string=variable_string[:-1]+')'
    for rem in removing_word_list:
        if rem in line:
            #print("rem:"+rem)
            line=line.replace(rem,"")
    structure='['+keyword+'(@\"'+line.strip()+preced_place_holder+'\")]\n\t\t'+'public void '+keyword+line.replace(" ", "")+variable_string+' \n\t\t{\n\n\t\t}\n\n\t\t'
    result_file.write(structure)

def func_generator_with_variable_java(keyword,line,result_file):
    preced_place_holder=""
    variable_string="("
    removing_word_list=[]
    removing_word_list.append(keyword)
    removing_word_list.append(',')
    for data in re.findall("<[A-Za-z_0-9]*>", line):
        preced_place_holder=preced_place_holder+"(.*)"
        #print(preced_place_holder)
        variable_string=variable_string+'String '+data[1:-1]+','
        temp="\"<"+data[1:-1]+">\""
        removing_word_list.append(temp)
    variable_string=variable_string[:-1]+')'
    for rem in removing_word_list:
        if rem in line:
            #print("rem:"+rem)
            line=line.replace(rem,"")
    structure='@'+keyword+'(\"^'+line.strip()+preced_place_holder+'$\")\n\t'+'public void '+line.replace(" ", "_")[1:-1]+variable_string+' throws InterruptedException {\n\n\t}\n\t\n\t'
    result_file.write(structure)

def func_generator_with_variable_js(keyword,line,result_file,func1):
    variable_string="("
    removing_word_list=[]
    removing_word_list.append(keyword)
    removing_word_list.append(',')
    preced_place_holder=""
    for data in re.findall("<[A-Za-z_0-9]*>", line):
        preced_place_holder=preced_place_holder+"{"+"string"+"},"
        #print(preced_place_holder)
        variable_string=variable_string+data[1:-1]+','
        temp="\"<"+data[1:-1]+">\""
        removing_word_list.append(temp)
    #print(removing_word_list)
    preced_place_holder=preced_place_holder[:-1]
    variable_string=variable_string[:-1]+')'
    for rem in removing_word_list:
        if rem in line:
            #print("rem:"+rem)
            line=line.replace(rem,"")
    #print("precedence:"+preced_place_holder)
    structure=keyword+'(\''+line.strip()+' '+preced_place_holder+'\','+variable_string+'=>{'+'\n'+func1+variable_string+'\n'+'})'+'\n'
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
            
            for doc in collection.find({}):
                F_total_factor=0
                for i in range(0,len(doc['id'])):
                    
                    if doc['id'][i]=='^' and int(doc['id'][i-1])>=list_of_level_pattern[0]:

                        F_total_factor+=int(doc['id'][i+1])
                    else:
                        continue
                if F_total_factor>=E_total_factor:
                    list_.append({'id':doc['id'],'tab':doc['tab'],'E_factor':int(E_total_factor),'F_factor':int(F_total_factor),'rows':len(doc['tab'].split("\n"))})
            
            list_.sort(key=myFunc)
           
            return HttpResponse(json.dumps({"result":(False,list_)}))


@csrf_exempt
def bdd(request):
    if request.method=='POST':
        values=[]
        variables=[]
        data=json.loads(request.body.decode('utf-8'))
        table_data=data['table_data']
        factor_name=data['column_data']
        
        file=open('features\BddScenario.feature','w')
        scenerio="@"+data['tag']+"\nFeature:Low code App\nScenario Outline:"
        scenerio+=data['scenerio']
        scenerio=scenerio+'\n'

        string1=''
        string_variables=''
        string_values=''
        for dat in data['pre_req']:
            string1+=dat['pre']+' '
            if(dat['pre_variables']!=''):
                string_variables=dat['pre_variables'].split(',')
                string_values=(dat['pre_values']).split(',')
                for i in string_variables:
                    string1+='\"<'+i+'>\",'
                    variables.append(i)
                for j in string_values:
                    values.append(j)
                string1=string1[:-1]
            string1+='\n'
        string1+='\n'

        string2="""And Funrnish the information """
        for factor in factor_name:
            string2+="\"<"
            string2+=factor
            string2+=">\","
        string2=string2[:-1]
        string2=string2+'\n\n'

        string3=''
        string_variables=''
        string_values=''
        for dat in data['post_req']:
            string3+=dat['post']+' '
            if(dat['post_variables']!=''):
                string_variables=dat['post_variables'].split(',')
                string_values=(dat['post_values']).split(',')
                for i in string_variables:
                    string3+='\"<'+i+'>\",'
                    variables.append(i)
                for j in string_values:
                    values.append(j)
                string3=string3[:-1]
            string3+='\n'
        print(string3)
        string3+='\n'


        string3=string3+'\n'+'Examples:'+'\n'
        for i in factor_name:
            string3+='|'
            string3+=i
        for i in variables:
            string3+='|'
            string3+=i
        string3+='|'
        string3+='\n'

        
        for line in table_data:
            for i in line:
                string3+='|'
                string3+=line[i]
            for j in values:
                string3+='|'
                string3+=j  
            string3+='|'
            string3+='\n'
            
        result=scenerio+string1+string2+string3
        file.write(result)
    return HttpResponse(json.dumps({"file_content":result}))

@csrf_exempt
def step_def(request):
    file=json.loads(request.body.decode('utf-8'))
    content=file['file_data']
    language=file['lang']
    content=content[:content.find("Examples:")]
    to_iter=content.split("\n")[2:]
    
    
    if language=='JavaScript':
        result_file=open('stepdefinition\BddScenario.js','w')
        for line in to_iter: 
            if "Given" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0 :
                print('Given' in line)
                print(len(re.findall("<[A-Za-z_0-9]*>", line)))
                func_generator_js("Given",line[len("Given"):],result_file)

            elif "And" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0:
                func_generator_js("And",line[len("And"):],result_file)

            elif "When" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0:
                func_generator_js("When",line[len("When"):],result_file)

            elif "And" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func1="userDefinedFunction"
                func_generator_with_variable_js("And",line,result_file,func1)

            elif "Given" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func1='ApplicationLaunch'
                func_generator_with_variable_js("Given",line,result_file,func1)

            elif "When" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func1='ApplicationLogin'
                func_generator_with_variable_js("When",line,result_file,func1)
        result_file=open('stepdefinition\BddScenario.js','r')
        
    elif language=='Java':
        result_file=open('stepdefinition\BddScenario.java','w')
        result_file.write('public class seatbooking  {'+'\n'+'\n'+'\t')
        for line in to_iter: 
            if "Given" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0:
                func_generator_java("Given",line[len("Given"):],result_file)
        
            elif "And" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0:
                func_generator_java("And",line[len("And"):],result_file)

            elif "When" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0:
                func_generator_java("When",line[len("When"):],result_file)
        
            elif "And" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func_generator_with_variable_java("And",line,result_file)
        
            elif "Given" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func_generator_with_variable_java("Given",line,result_file)

            elif "When" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func_generator_with_variable_java("When",line,result_file)
        result_file.write('}')
        result_file=open('stepdefinition\BddScenario.java','r')

    elif language=='C#':
        result_file=open('stepdefinition\BddScenario.cs','w')
        result_file.write('namespace TestingPractice.ProjectName.TA.Steps\n{\n\t[Binding]\n\tpublic sealed class BDDScenarios : TestSteps\n\t{\n\t\t')
        for line in to_iter: 
            if "Given" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0:
               
                func_generator_cs("Given",line[len("Given"):],result_file)
                
            elif "And" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0:
                func_generator_cs("And",line[len("And"):],result_file)

            elif "When" in line and len(re.findall("<[A-Za-z_0-9]*>", line))==0:
                func_generator_cs("When",line[len("When"):],result_file)

            elif "And" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func_generator_with_variable_cs("And",line,result_file)        

            elif "Given" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func_generator_with_variable_cs("Given",line,result_file)

            elif "When" in line and len(re.findall("<[A-Za-z_0-9]*>", line))!=0:
                func_generator_with_variable_cs("When",line,result_file)
        result_file.write('}\n}')
        result_file=open('stepdefinition\BddScenario.cs','r')
    return HttpResponse(json.dumps({"file_content":result_file.read()}))


@csrf_exempt
def automatic(request):
    df = pd.read_csv('file.csv')
    return_list=[]
    fetched=json.loads(request.body.decode('utf-8'))
    for data in fetched['row']:
        temp=[]
        for i in df[data['Factor_name']]:
            temp.append(i)
        return_list.append(temp)
    print(return_list)
    return HttpResponse(json.dumps({"result":return_list}))

@csrf_exempt
def automatic_pre_post(request):
    df = pd.read_csv('pre_post.csv')
    fetched=json.loads(request.body.decode('utf-8'))
    row1=fetched['row1']
    row2=fetched['row2']
    return_list_pre=[]
    return_list_post=[]
   
    for data in df['pre']:
        
        return_list_pre.append(data)
    
    for data in df['post']:
        return_list_post.append(data)
      
    return HttpResponse(json.dumps({"result_pre":return_list_pre,"result_post":return_list_post,"tag":df['tag'][0],"scenerios":df['scenerio'][0]}))

@csrf_exempt
def enhance(request):
    df = pd.read_csv('LowCodeApp.csv')
    print(df['FunctionName'])
    return_list=[]
    for i in df['FunctionName']:
        return_list.append(i)
    return HttpResponse(json.dumps({"result":return_list}))

@csrf_exempt
def integrate(request):
    os.chdir("C:/Users/Ei12974/Downloads/TechUtsav (5)/TechUtsav")
    cwd = os.getcwd()
    
    # print the current directory
    print("Current working directory is:", cwd)
    os.system("mvn clean install")
    os.chdir('C:/Users/Ei12974/Downloads/Techutsav_firstmilestone-java_branch/Techutsav_firstmilestone-java_branch/backend/backend')
    return HttpResponse("ok")

@csrf_exempt
def enhanced_step_def(request):
    df = pd.read_csv('LowCodeApp.csv')
    data=json.loads(request.body.decode('utf-8'))
    language=data['language']
    flag=data['flag']
    
    
    
    if language=='Java':
        result_file=open('stepdefinition\BddScenario.java','w')
        result_file.write('public class seatbooking  {'+'\n'+'\n'+'\t')
        for line in data['pre_req']: 
            if "And" in line['pre']:
                print(True)
                row=df.loc[df['FunctionName'] == line['selectedCar']]
                for index, i in row.iterrows():
                    object_with_func=i['ObjectName']+'.'+i['FunctionName']
                    param=str(i['param1'])
                    returnparam=i['FunctionReturnParam']
                    print(type(param))
                    print(returnparam)
                func_generator_java("And",line['pre'][len("And"):],result_file,object_with_func,param,str(returnparam),flag)
        
            elif "Given" in line['pre']:
                print(True)
                row=df.loc[df['FunctionName'] == line['selectedCar']]
                for index, i in row.iterrows():
                    object_with_func=i['ObjectName']+'.'+i['FunctionName']
                    param=str(i['param1'])
                    returnparam=i['FunctionReturnParam']
                func_generator_java("Given",line['pre'][len("Given"):],result_file,object_with_func,param,str(returnparam),flag)
            
        
            

            elif "When" in line['pre']:
                print(True)
                row=df.loc[df['FunctionName'] == line['selectedCar']]
                for index, i in row.iterrows():
                    object_with_func=i['ObjectName']+'.'+i['FunctionName']
                    param=str(i['param1'])
                    returnparam=i['FunctionReturnParam']
                func_generator_java("When",line['pre'][len("When"):],result_file,object_with_func,param,str(returnparam),flag)
        for line in data['post_req']: 
            
            if "And" in line['post']:
                print(True)
                row=df.loc[df['FunctionName'] == line['selectedCar']]
                for index, i in row.iterrows():
                    object_with_func=i['ObjectName']+'.'+i['FunctionName']
                    param=str(i['param1'])
                    returnparam=i['FunctionReturnParam']
                    print(type(param))
                    print(returnparam)
                func_generator_java("And",line['post'][len("And"):],result_file,object_with_func,param,str(returnparam),flag)
        
            elif "Given" in line['post']:
                print(True)
                row=df.loc[df['FunctionName'] == line['selectedCar']]
                for index, i in row.iterrows():
                    object_with_func=i['ObjectName']+'.'+i['FunctionName']
                    param=str(i['param1'])
                    returnparam=i['FunctionReturnParam']
                func_generator_java("Given",line['post'][len("Given"):],result_file,object_with_func,param,str(returnparam),flag)
            
        
            

            elif "When" in line['post']:
                print(True)
                row=df.loc[df['FunctionName'] == line['selectedCar']]
                for index, i in row.iterrows():
                    object_with_func=i['ObjectName']+'.'+i['FunctionName']
                    param=str(i['param1'])
                    returnparam=i['FunctionReturnParam']
                func_generator_java("When",line['post'][len("When"):],result_file,object_with_func,param,str(returnparam),flag)
        result_file.write('\n}')
        result_file=open('stepdefinition\BddScenario.java','r')

    return HttpResponse(json.dumps({"file_content":result_file.read()}))


@csrf_exempt
def report(request):
    webbrowser.open_new_tab('C:/Users/Ei12974/Downloads/TechUtsav (5)/TechUtsav/target/cucumber-reports/AutomationResults.html')
    return HttpResponse("ok")

