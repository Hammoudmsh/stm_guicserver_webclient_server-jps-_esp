
const getpath_btn = document.getElementById('getpath_id');
const cancelorder_btn=document.getElementById('cancelorder_id');
const order_btn = document.getElementById('order_id');
const getnumoforders_btn = document.getElementById('getnumoforders_id');
const  getallorders_btn=document.getElementById('getallorders_id');
const  server_ip_id=document.getElementById('server_ip_idd');
const  server_port_id=document.getElementById('server_port_id');
const  islocal_check_id=document.getElementById('islocal_id');
const node=document.getElementById('user_id');

const getpath_txt='/getpath';
const order_txt='/order';
const cancelorder_txt='/cancelorder';
const getnumoforders_txt='/getnumoforders';
const getallorders_txt='/getallorders';

function validate(s){
var val=node.value; //var val=document.forms["form1"]["text1"].value;
if(val==""){
    node.style.background="red";
    console.log("Please enter valid!");
    return false;
  }
  else{
    return true;
	console.log("valid accepted!");
}
}


//..................................................................... selectip()

function selectip(){
/*
  if(islocal_check_id.checked==true){
	server_ip_idd.disabled=false;
  alert("ff");
}
else
	server_ip_idd.disabled=true;
*/
}
//..................................................................... order()
function orderbtn(){

if(validate("Are you sure Order ?")!=true) return;
var s="";
if(islocal_check_id.checked){
s="127.0.0.1";
}
else{
s=document.getElementById("server_ip_id").value;
}
var val=document.getElementById("user_id").value;
window.open(s  + ":" + server_port_id.value+order_txt+"/"+val); 
  //SEND(order_txt,val);
}
//..................................................................... cancelorder()
function cancelorderbtn(){
var s;
if(islocal_check_id.checked){
s="127.0.0.1";
}
else{
s=document.getElementById("server_ip_id").value;
}
var main_url =s  + ":" + document.getElementById("server_port_id").value; 
 
 if(validate("Are you sure Cancel ?")!=true) return;
  var val=document.getElementById("user_id").value; 
  window.open(main_url+cancelorder_txt+"/"+val);  
}
//..................................................................... getpath1()
function getpathbtn(){ 
var s;
if(islocal_check_id.checked){
s="127.0.0.1";
}
else{
s=document.getElementById("server_ip_id").value;
}
var main_url =s  + ":" + document.getElementById("server_port_id").value;   
 if(validate("Are you sure Getpath ?")!=true) return;
 var val=document.getElementById("user_id").value; 
  window.open(main_url+getpath_txt+"/"+val); 
 }
 //..................................................................... getnumoforders()
function getnumoforders(){ 
var s;
if(islocal_check_id.checked){
s="127.0.0.1";
}
else{
s=document.getElementById("server_ip_id").value;
}
var main_url =s  + ":" + document.getElementById("server_port_id").value; 
  
window.open(main_url+getnumoforders_txt);
  GET(getnumoforders_txt); 
 }
 //..................................................................... getallorders()
function getallorders(){ 
var s="";
if(islocal_check_id.checked){
s="127.0.0.1";
}
else{
s=server_ip_id.value;
}
var main_url =s  + ":" + document.getElementById("server_port_id").value;   
window.open(main_url+getallorders_txt);
  GET(getallorders_txt); 
 }
 
 //..................................................................... sendHttpRequest()
var sendHttpRequest = (method, url, data) => {
  const promise = new Promise((resolve, reject) => {
  const xhr = new XMLHttpRequest();
      xhr.open(method, url);
      xhr.responseType = 'json';
      if (data) {
        xhr.setRequestHeader('Content-Type', 'application/json');
      }
      xhr.onload = () => {
        if (xhr.status >= 400) {
          reject(xhr.response);
        } else {
          resolve(xhr.response);
        }
      };
      xhr.onerror = () => {
        reject('Something went wrong!');
      };
      xhr.send(JSON.stringify(data));
    });
    return promise;
};
//..................................................................... get()
var GET = (url) => {
  sendHttpRequest('GET', url).then(responseData => {
  alert(responseData);
  console.log(responseData);
  });
};
//..................................................................... send()
var SEND= (s,data) => {
  alert("kddddddd");
  var nodee=document.getElementById("user_id").value;
  sendHttpRequest('POST', s, {
    val:data
    // password: 'pistol'
  })
    .then(responseData => {
      console.log(responseData);
    })
    .catch(err => {
      console.log(err);
    });
};

//..................................................................... action listener()
/*  don't work.
getpathbtn.addEventListener('click', getpath);
orderbtn.addEventListener('click', order);
cancelorderbtn.addEventListener('click', cancelorder);
*/
