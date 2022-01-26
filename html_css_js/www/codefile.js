/*
var getpath_btn = document.getElementById('getpath_id');
var cancelorder_btn=document.getElementById('cancelorder_id');
var order_btn = document.getElementById('order_id');
var getnumoforders_btn = document.getElementById('getnumoforders_id');
var  getallorders_btn=document.getElementById('getallorders_id');
var  document.getElementById('server_ip_idd')=document.getElementById('document.getElementById('server_ip_idd')d');
var  document.getElementById('server_port_id')=document.getElementById('document.getElementById('server_port_id')');
var  =document.getElementById('islocal_id');
var document.getElementById('user_id')=document.getElementById('user_id');
*/
var getpath_txt='/getpath';
var order_txt='/order';
var cancelorder_txt='/cancelorder';
var getnumoforders_txt='/getnumoforders';
var getallorders_txt='/getallorders';

function validate(s){
var val=document.getElementById('user_id').value;
if(val==""){
    document.getElementById('user_id').style.background="red";
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

  if(document.getElementById('islocal_id').checked==true){
	document.getElementById('server_ip_idd').disabled=true;
}
else{
	document.getElementById('server_ip_idd').disabled=false;
}
}
//..................................................................... order()
function orderbtn(){

if(validate("Are you sure Order ?")!=true) return;
var s="";
if(document.getElementById('islocal_id').checked){
s="0.0.0.0";
}
else{
       s=document.getElementById('server_ip_idd').value;
}
var val=document.getElementById("user_id").value;
window.open("http://"+s  + ":" + document.getElementById('server_port_id').value+order_txt+"/"+val,'_blank'); 
  //SEND(order_txt,val);
}
//..................................................................... cancelorder()
function cancelorderbtn(){
  if(validate("Are you sure Order ?")!=true) return;
  var s="";
  if(document.getElementById('islocal_id').checked){
  s="0.0.0.0";
  }
  else{
  s=document.getElementById('server_ip_idd').value;
  }
  var val=document.getElementById("user_id").value;
  window.open("http://"+s  + ":" + document.getElementById('server_port_id').value+cancelorder_txt+"/"+val,'_blank'); 

}

//..................................................................... getpath1()
function getpathbtn(){ 
  if(validate("Are you sure Order ?")!=true) return;
  var s="";
  if(document.getElementById('islocal_id').checked){
  s="0.0.0.0";
  }
  else{
  s=document.getElementById('server_ip_idd').value;
  }
  var val=document.getElementById("user_id").value;
  window.open("http://"+s  + ":" + document.getElementById('server_port_id').value+cagetpath_txt+"/"+val,'_blank'); 
 }
 //..................................................................... getnumoforders()
function getnumoforders(){ 
  if(validate("Are you sure Order ?")!=true) return;
  var s="";
  if(document.getElementById('islocal_id').checked){
  s="0.0.0.0";
  }
  else{
  s=document.getElementById('server_ip_idd').value;
  }
  var val=document.getElementById("user_id").value;
  window.open("http://"+s  + ":" + document.getElementById('server_port_id').value+getnumoforders_txt,'_blank');

 }
 //..................................................................... getallorders()
function getallorders(){ 
  if(validate("Are you sure Order ?")!=true) return;
  var s="";
  if(document.getElementById('islocal_id').checked){
  s="0.0.0.0";
  }
  else{
  s=document.getElementById('server_ip_idd').value;
  }
  var val=document.getElementById("user_id").value;
  window.open("http://"+s  + ":" + document.getElementById('server_port_id').value+getallorders_txt,'_blank');
 }
 //..................................................................... sendHttpRequest()
var sendHttpRequest = (method, url, data) => {
  var promise = new Promise((resolve, reject) => {
  var xhr = new XMLHttpRequest();
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
  var node=document.getElementById("user_id").value;
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
