import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ModalService } from 'src/app/_modal/modal.service';
import {
  FormGroup,
  FormBuilder,
  Validators,
  FormControl,
  FormArray,
  NgForm,
} from '@angular/forms';
import { Arr } from 'src/app/model';
/**
 * @title Basic expansion panel
 *
 */
import * as $ from 'jquery';

@Component({
  selector: 'app-oa',
  templateUrl: './oa.component.html',
  styleUrls: ['./oa.component.css']
})
export class OAComponent {
  table_generated=false;
  firstScreen:boolean=true;
  secondScreen:boolean=false;
  map_col={}
  arr: Arr = { Factors: '0', Levels: '0' };
  addForm: FormGroup;
  displayedColumns=[]
  rows=[];
  flag=false;
  flagoa=false;
  flagnext=true;
  flagrefresh=false;
  Scenerio=""
  tag=""
  file_content=""
  content={}
  id:string=''
  Factors=0
  Pre_Requisite=""
  Post_Requisite=""
  Number_of_factor: string = '0';
  onscreen=[]
  obj: any;
  fetched_list=[];
  radio_list=[]
  SelectedItem='';
  Fac=0;
  data: Array<{}> = [];
  one_time_flag=false
  flag_table:boolean=false;
  previous_state=[]
  /**Initializing row as array of form builder*/
  constructor(private http: HttpClient,private modalService: ModalService) {
    
  }
  Home(){
    this.initialise_back_to_home();

  }

  initialise_back_to_home(){
    
    this.table_generated=false;
    this.firstScreen=true;
    this.secondScreen=false;
    this.map_col={}
    this.displayedColumns=[]
    this.rows=[]
    this.flagoa=false
    this.flagnext=true
    this.id=''
    this.Factors=0
    this.Number_of_factor='0'
    this.onscreen=[]
    this.obj={}
    this.fetched_list=[]
      this.radio_list=[]
      this.displayedColumns=[]
      this.data=[]
      this.flag_table=false
      this,this.one_time_flag=false
  }
  /**Adding rows to form group */


  ngOnInit() {
    
  }
  
  /**Getting the factor value and generating columns based on Factor value*/
  onSave() {
    this.Pre_Requisite=""
    this.Post_Requisite=""
    this.Scenerio=""
    this.tag=""
    for (let index = 0; index < Number(this.Factors); index++) {
      this.displayedColumns.push(String(index));
    }
    this.firstScreen=false;
    this.secondScreen=true;
    console.log(this.displayedColumns);

    for(let i=0 ; i< Number(this.Factors); i++)
    {
      this.rows.push({
        Factor_name:'',
        Level_count: '',
        Level_value:[],
        Level_values:''
      });
    }
  }
  refresh(){
   
   
    
    for(let index=0;index<Number(this.Factors);index++){
      this.rows[index].Factor_name=this.previous_state[index].Factor_name
      this.rows[index].Level_count=this.previous_state[index].Level_count
      this.rows[index].Level_value=[]
      this.rows[index].Level_values=''
    }
  }
  display(){
    
    for(let i=0;i<Number(this.Factors);i++){
      for(let j=0;j<Number(this.rows[i].Level_count);j++){
        this.rows[i].Level_value.push({value:'0'})
      }
    }
    console.log("level_values:")
    console.log(this.rows)
    this.flag=true;
    this.flagoa=true;
    this.flagnext=false;
    $('.inputId').prop('readonly', true);
    this.flagrefresh=false
  }
  /**used to create element of form array*/
  emptylist(){
    if(this.flagnext==true){
      this.previous_state=this.rows
      $(".inputId").val(' ');
      this.rows=[]
      this.displayedColumns=[]
      this.onSave()
      
    }
    else if(this.flagoa==true)
    {
      $(".inputlevels").val(' ');
      for(let i=0;i<Number(this.Factors);i++){
        this.rows[i].Level_value=[] 
      }
      for(let i=0;i<Number(this.Factors);i++){
        for(let j=0;j<Number(this.rows[i].Level_count);j++){
          this.rows[i].Level_value.push({value:''})
        }
      }
    }
    this.flagrefresh=true
  }
  sleep(milliseconds: number) {
    let resolve: any;
    let promise = new Promise((_resolve) => {
      resolve = _resolve;
    });
    setTimeout(() => resolve(), milliseconds);
    return promise;
  }

  backfunction(){
    if(this.flagoa==true)
    {
      $(".inputlevels").val('0');
      for(let i=0;i<Number(this.Factors);i++){
        this.rows[i].Level_value=[] 
      }

      console.log("data:")
      console.log(this.data)
      console.log("row value:")
    console.log(this.rows)
      this.flagoa=false
      this.flagnext=true
      
      this.onscreen=[]
      this.map_col={}
      this.obj={}
      this.fetched_list=[]
      this.radio_list=[]
      
      this.data=[]
      this.flag_table=false
      $('.inputId').prop('readonly', false);
    }
    else if(this.flagnext==true)
    {
      $(".inputId").val(' ');
      this.rows=[]
      this.displayedColumns=[]
      this.firstScreen=true
      this.secondScreen=false
      this.onscreen=[]
      this.map_col={}
      this.obj={}
      this.fetched_list=[]
      this.radio_list=[]
      this.displayedColumns=[]
      this.data=[]
      this.flag_table=false
      
    }
  }
  
  CreateOA(id:string){
    if(this.one_time_flag==false){
      for(let i=0;i<Number(this.Factors);i++){
        for(let j=0;j<this.rows[i].Level_value.length;j++){
          
          this.rows[i].Level_values+=this.rows[i].Level_value[j].value
          this.rows[i].Level_values+=','
        }
        this.rows[i].Level_values=this.rows[i].Level_values.slice(0,this.rows[i].Level_values.length-1)
    }
    this.one_time_flag=true
    }
    
  
  console.log(this.rows)
  this.id=id
  let count = {};
  for (let index = 0; index < this.rows.length; index++) {
    let s = this.rows[index]['Level_values'].split(',').length;
    if (s in count) {
      let temp = count[s];
      temp = temp + 1;
      count[s] = temp;
    } else {
      count[s] = 1;
    }
  }
  console.log('count dic is :');
  console.log(count);
  let str = '';
  for (let key in count) {
    str += key;
    str = str + '^' + String(count[key]);
    str += ' ';
  }
  str = str.slice(0, str.length - 1);

  for (let index = 0; index < this.rows.length; index++) {
   let temp=this.rows[index].Factor_name
   this.onscreen.push(temp)
   this.map_col[this.displayedColumns[index]]=this.onscreen[index]
  }
  console.log("onscreen:"+this.map_col)
  this.http
    .post('http://127.0.0.1:8000/', {
      pattern: str,
    })
    .subscribe((data) => (this.obj = data));
  console.log(this.obj);
this.sleep(5000).then(() => {if (this.obj) {
  if(this.obj.result[0]==false)
     {
   this.fetched_list=this.obj.result[1]
  

   for (let index=0;index<=2;index++)
       {
       this.radio_list.push(this.fetched_list[index]['id'])
       }
       this.modalService.open(this.id);
       }
 else{
   this.submit()
   }

 }})
 
 
}
closeModal(id: string) {
  this.modalService.close(id);
}

submit(){
  
  let s='';
  console.log("selectedItem:")
  console.log(this.SelectedItem)
  if(this.obj.result[0]==false)
  {
  for (let index=0;index<this.fetched_list.length;index++)
   {
   
   if (this.fetched_list[index]['id']==this.SelectedItem){
       console.log("fetched_list[index]:")
       console.log(this.fetched_list[index])
   if (this.fetched_list[index]['F_factor']-this.fetched_list[index]['E_index'] == 0){
   
   s=this.fetched_list[index]['tab']
   }
       else{
     this.Fac=this.fetched_list[index]['F_factor'];
     console.log("type")
     console.log(typeof this.fetched_list[index]['E_factor'] )
     let E=this.fetched_list[index]['F_factor']
     let F=this.fetched_list[index]['E_factor'];
 
     let removing_col=E-F
     console.log("removingcol:")
 
     console.log(removing_col)
     let new_=this.fetched_list[index]['tab'].split("\n")
     new_.pop()
 
     console.log("new_")
     console.log(new_)
 
     for (let i=0;i<new_.length;i++){
       s+=new_[i].slice(0,new_[i].length-removing_col);
       s+="\n";
       console.log("x:")
       console.log(s)
 
               }
 
     
           }
    break;
   }
 
   
   }
  }
  else{
    s=this.obj.result[2]
  }
   console.log(" s new:")
     console.log(s)
   if(this.obj.result[0]){
          
     }
     else{
       
          
         let new_fac=this.Fac;
         for (let i=0; i<this.rows.length;i++)
         {
            console.log("rowssss")
            console.log(this.rows)
             if (this.rows[i].Level_values.split(",").length<new_fac)
             
             {
              console.log(this.rows[i].Level_values.split(","))
               for (let j=0; j<new_fac-this.rows[i].Level_values.split(",").length; j++)
               {
                 this.rows[i].Level_values+=',~'
                  console.log("new row:")
                  console.log(this.rows[i])
               }
             }
                 
         }
       
     }
   console.log("row.value:")
   console.log(this.rows)
   console.log("s:")
    console.log(s);
     let list = s.split('\n');
     console.log(list);
     console.log(this.displayedColumns);
     const runs = list.length;
     console.log(this.rows)
     for (let index = 0; index < runs; index++) {
       let d = {};
       for (let j = 0; j < list[index].length; j++) {
         d[String(j)] =
           this.rows[j]['Level_values'].split(',')[list[index][j]];
       }
       this.data.push(d);
     }
     console.log(this.data);
     this.data.pop()
    
 
 ///

 console.log("inside submit data:")
 console.log(this.data)
 this.table_generated=true
 this.flag_table=true;
 this.modalService.close(this.id);
 console.log("flag table:")
 console.log(this.flag_table)
 console.log("columns:")
 console.log(this.displayedColumns)
 console.log("map:")
 console.log(this.map_col)
 }
step(){
  this.http
    .post('http://127.0.0.1:8000/stepdefination',{
      file_data:this.file_content
    }).subscribe()

}
bdd(id:string){
  let factor_names=[]
  let temp=[]
  for (let index = 0; index < this.displayedColumns.length; index++){
    factor_names.push(this.map_col[this.displayedColumns[index]])
  }
  
  console.log("factors")
  console.log(factor_names)
  this.http
    .post('http://127.0.0.1:8000/bdd', {
      table_data: this.data,
      column_data:factor_names,
      pre: this.Pre_Requisite,
      post: this.Post_Requisite,
      scenerio:this.Scenerio,
      tag:this.tag

    })
    .subscribe((data) => (this.content = data));
    this.sleep(3000).then(() => {if (this.content) {
      this.file_content=this.content['file_content']
      console.log("file_content")
      console.log(this.file_content)
      this.modalService.open(id);
    
     }})
}

generate(id:string) {
  this.id=id
  let count = {};
  for (let index = 0; index < this.rows.length; index++) {
    let s = this.rows[index]['Level_values'].split(',').length;
    if (s in count) {
      let temp = count[s];
      temp = temp + 1;
      count[s] = temp;
    } else {
      count[s] = 1;
    }
  }
  console.log('count dic is :');
  console.log(count);
  let str = '';
  for (let key in count) {
    str += key;
    str = str + '^' + String(count[key]);
    str += ' ';
  }
  str = str.slice(0, str.length - 1);

  for (let index = 0; index < this.rows.length; index++) {
   let temp=this.rows[index]['Factor_name']
   this.onscreen.push(temp)
   this.map_col[this.displayedColumns[index]]=this.onscreen[index]
  }
  console.log("onscreen:"+this.map_col)
  this.http
    .post('http://127.0.0.1:8000/', {
      pattern: str,
    })
    .subscribe((data) => (this.obj = data));
  console.log(this.obj);
//
 if (this.obj) {
    this.fetched_list=this.obj.result[1]
 
 for (let index=0;index<=2;index++)
{
this.radio_list.push(this.fetched_list[index]['id'])
}
console.log("radio_list:")
console.log(this.radio_list)
 this.modalService.open(id);
  }
}


}
