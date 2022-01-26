import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import simpledialog
from PIL import ImageTk,Image
import time
import datetime
from socket import *
import time
from time import ctime
import _thread
from flask import Flask, render_template, make_response, jsonify, request,redirect,url_for
import http.client
import os
import jps
import mapp 
#

html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"><style>body { text-align: center; font-family: "Trebuchet MS", Arial;}
  table { border-collapse: collapse; width:35%; margin-left:auto; margin-right:auto; }
  th { padding: 12px; background-color: #0043af; color: white; }
  tr { border: 1px solid #ddd; padding: 12px; }
  tr:hover { background-color: #bcbcbc; }
  td { border: none; padding: 12px; }
  .sensor { color:white; font-weight: bold; background-color: #bcbcbc; padding: 1px;
  </style></head><body><h1>ESP with BME280</h1>
  <table><tr><th>MEASUREMENT</th><th>VALUE</th></tr>
  <tr><td>Temp. Celsius</td><td><span class="sensor">""" + str(1) + """</span></td></tr>
  <tr><td>Temp. Fahrenheit</td><td><span class="sensor">""" + str(2) + """F</span></td></tr>
  <tr><td>Pressure</td><td><span class="sensor">""" + str(3) + """</span></td></tr>
  <tr><td>Humidity</td><td><span class="sensor">""" + str(4) + """</span></td></tr> 
  </body></html>"""
#.................................................................................Server
IP='192.168.43.163'
PORT='3300'
#.................................................................................
LARGE_FONT= ("Verdana", 12)
#......................

Dire={ "01":'0',
       "0-1":'4',
       "10":'6',
       "1-1":'5',
       "11":'7',
       "-10":'2',
       "-1-1":'3',
       "-11":'1'}
#.................................................................................maps
available_map=["map1","map2","Build own"]
defaultmap="map2"
[field,MAP_WIDTH,MAP_HEIGHT]=mapp.init_map(defaultmap)
#.................................................................................
global points
paths={}
orders=[]
points=[]
cur_node=""
from http.server import BaseHTTPRequestHandler, HTTPServer

#.........................................................................................................debug and get directions from points
COLORS={0:"Green",1:"Blue",2:"Black",3:"Green Light",4:"Yellow",5:"Blue Light",6:"Brown",7:"Red"}
"""
class Page(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title("MIET Server RoboCar")
        #self.iconbitmap("E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\stm_guicserver_webclient_server(jps)_esp\roboticon.png")
        #self.iconbitmap(False,tk.PhotoImage(file="E:/Mohammed/Micro Controller/STM/Thesis/Master_Project/Project_code/w/stm_guicserver_webclient_server(jps)_esp/roboticon.png"))
        self.resizable(False,False)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.configure()
        
        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Frame.height=3
        l_title=tk.Label(self, text="Server Software",
                         font=('times', 20, 'bold'))

        l_title.grid(row=0,column=0,columnspan=3, sticky="NSEW",padx=30,pady=10)
     
        img=ImageTk.PhotoImage(Image.open("E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\stm_guicserver_webclient_server(jps)_esp\MIET.png"))
        panel=tk.Label(self,image=img)
        panel.image=img
        panel.grid(row=1, column=1,columnspan=3)
        
        label_username = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")

        entry_username = tk.Entry(self,show="*",width=50)

        entry_password = tk.Entry(self, show="*",width=50)

        label_username.grid(row=2, column=0, sticky='NSEW',padx=10,pady=10)
        label_password.grid(row=3, column=0, sticky='NSEW',padx=10,pady=10)
        entry_username.grid(row=2, column=1,sticky='NSEW',padx=10,pady=10)
        entry_password.grid(row=3, column=1,sticky='NSEW',padx=10,pady=10)

        logbtn = tk.Button(self, text="Login", bg="BlACK", fg="White",command=lambda: login_btn_clicked())
        logbtn.grid(row=5, column=1,sticky='NSEW', padx=10, pady=10)

        def login_btn_clicked(): 
            controller.show_frame(PageOne)
"""
    
class PageOne(tk.Tk):#tk.Frame
    def __init__(self):#, parent, controller):
        
        tk.Tk.__init__(self)#), parent)
        self.title("MIET Server RoboCar")
        self.resizable(False,False)

        flag = True

        self.label = tk.Label(self, text="Server Software ", font=('times', 20, 'bold'),fg="Black")
        self.label.grid(row=0, column=2, columnspan=1, padx=8, pady=8, sticky="NSNESWSE")

        self.labelframe=tk.LabelFrame(self,text="Configuration")
        self.labelframe.grid(row=1, column=0,rowspan=2,columnspan=10,padx=4, pady=4, sticky="NSNESWSE")

        self.l_host=tk.Label(self.labelframe,text="Host Ip",font=('times', 12, 'bold'))
        self.l_host.grid(row=1, column=0, padx=4, pady=4, sticky="NSNESWSE")
        self.varcheck=tk.IntVar()
        self.checkbox = tk.Checkbutton(self.labelframe, text="Local",command=lambda: islocal(),variable=self.varcheck)
        self.checkbox.grid(row=1, column=3,padx=1,pady=1)
        
        self.label1 = tk.Label(self.labelframe, text="Map", font=('times', 10, 'bold'),fg="Black")
        self.label1.grid(row=1, column=4, columnspan=1, padx=2, pady=2, sticky="NSNESWSE")

        self.usedmap=tk.StringVar()
        
        def onChangeValue(object):
            if self.maps.get() != available_map[2]:
                [field,MAP_WIDTH,MAP_HEIGHT]=mapp.init_map(self.maps.get())
            #else:
            #    execfile("E:/a8.py")
        self.maps=ttk.Combobox(self.labelframe,values=available_map,state='readonly',textvariable=self.usedmap,width=8)
        self.maps.grid(row=1, column=5,rowspan=1,columnspan=1,padx=4,pady=4)
        self.maps.current(available_map.index(defaultmap))
        self.maps.bind("<<ComboboxSelected>>",onChangeValue)
        
        self.label1 = tk.Label(self.labelframe, text="Algorithim", font=('times', 10, 'bold'),fg="Black")
        self.label1.grid(row=2, column=4, columnspan=1, padx=2, pady=2, sticky="NSNESWSE")

        self.alg=tk.StringVar()
        self.cb=ttk.Combobox(self.labelframe,values=["JPS"],state='readonly',textvariable=self.alg,width=8)
        self.cb.grid(row=2, column=5,rowspan=1,columnspan=1,padx=4,pady=4)
        self.cb.current(0)
        """
        img=ImageTk.PhotoImage(Image.open("E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\stm_guicserver_webclient_server(jps)_esp\MIET.png"))
        panel=tk.Label(self,image=img)
        panel.image=img
        panel.grid(row=0, column=3,columnspan=2)
        """
        
        self.e_host=tk.Entry(self.labelframe)
        self.e_host.grid(row=1, column=1, columnspan=1, padx=2, pady=2, sticky="NSNESWSE")
        self.e_host.insert(tk.END,IP)

        self.l_port=tk.Label(self.labelframe,text="Port   ",font=('times', 12, 'bold'))
        self.l_port.grid(row=2, column=0, padx=4, pady=4, sticky="NSNESWSE")
        
        self.e_port=tk.Entry(self.labelframe)
        self.e_port.grid(row=2, column=1, columnspan=1, padx=2, pady=2, sticky="NSNESWSE")
        self.e_port.insert(tk.END,PORT)
        
        self.lf2=tk.LabelFrame(self,text="Debug")
        self.lf2.grid(row=4, column=0,rowspan=2,columnspan=5,padx=4, pady=4, sticky="NSNESWSE")

        self.b_connect=tk.Button(self,text="ON",bg="green",command=lambda: connect(),font=('times', 12),width=8,height=1)
        self.b_connect.grid(row=3,column=0,columnspan=8,rowspan=1,padx=10,pady=5,sticky="nsew")
        
        self.b_order=tk.Button(self.lf2,text="   Order",command=lambda: b_order(),font=('times', 12),width=8,height=1)
        self.b_order.grid(row=4,column=0,padx=2,pady=2,sticky="nsew")
        
        self.b_cancel=tk.Button(self.lf2,text="  cancel",command=lambda: b_cancel(),font=('times', 12),width=8,height=1)
        self.b_cancel.grid(row=4,column=1,padx=2,pady=2,sticky="nsew")      

        self.b_getpath=tk.Button(self.lf2,text="Getpath",command=lambda: b_getpath(),font=('times', 12),width=8,height=1)
        self.b_getpath.grid(row=4,column=2,padx=2,pady=2,sticky="nsew")
        
        self.b_clear=tk.Button(self.lf2,text=" Clear",command=lambda: cleartxt(),font=('times', 12),width=8,height=1)
        self.b_clear.grid(row=4,column=3,padx=2,pady=2,sticky="nsew")
        
        self.b_exit=tk.Button(self.lf2,text=" Exit",command=lambda: exit(),font=('times', 12),width=8,height=1)
        self.b_exit.grid(row=4,column=4,padx=2,pady=2,sticky="nsew")
        
        self.n=tk.StringVar()
        self.orders_pop=ttk.Combobox(self.lf2,values=["Orders"],state='readonly',textvariable=self.n,width=15)
        self.orders_pop.grid(row=6, column=1,rowspan=1,columnspan=1)
        self.orders_pop.current(0)

        self.n1=tk.StringVar()
        self.path_combo=ttk.Combobox(self.lf2,values=["Path"],state='readonly',textvariable=self.n1,width=10)
        self.path_combo.grid(row=6, column=2,rowspan=1,columnspan=1)
        self.path_combo.current(0)

        self.message_label=tk.Label(self.lf2,text="Client Message",font=("Arial",10,'bold'))
        self.message_label.grid(row=6,column=0,columnspan=1,padx=4,pady=0,sticky="NSEW")      
        
        self.scrollbar_y = tk.Scrollbar(self.lf2)
        self.scrollbar_y.grid(row=7, column=7,rowspan=8,sticky="NSEW")
        self.show_1=tk.Text(self.lf2,height=8, width=60, yscrollcommand=self.scrollbar_y.set,bg="white",fg="black")
        self.show_1.grid(row=7, column=0,rowspan=8,columnspan=7,sticky="NSEW")
        self.scrollbar_y.config(command=self.show_1.yview)

        self.status=tk.Label(self,text="Mohammed Sameeh Hammoud, Russia,Zelenograd,University MIET",font=("Arial",10,'bold'))
        self.status.grid(row=8, column=0,columnspan=7)
        
        def my_pop(e):
            self.menuclick.tk_popup(e.x_root,e.y_root)
        def hs_config_hide():
            self.labelframe.grid_forget()
            #self.labelframe.grid(row=1, column=0,rowspan=2,columnspan=10,padx=4, pady=4, sticky="NSNESWSE")
        def hs_config_show():
            self.labelframe.grid(row=1, column=0,rowspan=2,columnspan=10,padx=4, pady=4, sticky="NSNESWSE")
            #self.lf2.grid(row=4, column=0,rowspan=2,columnspan=5,padx=4, pady=4, sticky="NSNESWSE")
        def exitt():
            #self.quit()
            pass
        self.menuclick=tk.Menu(self,tearoff=0)
        self.menuclick.add_command(label="Show configurations",command=hs_config_show)
        self.menuclick.add_command(label="Hide configurations",command=hs_config_hide)
        self.menuclick.add_separator()
        self.menuclick.add_command(label="Exit",command=exitt)
        self.bind("<Button-3>",my_pop)
        def send_header(client, status_code=200, content_length=None ):
            client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
            client.sendall("Content-Type: text/html\r\n")
            if content_length is not None:
                client.sendall("Content-Length: {}\r\n".format(content_length))
            client.sendall("\r\n")


        def send_response(client, payload, status_code=200):
            content_length = len(payload)
            send_header(client, status_code, content_length)
            if content_length > 0:
                client.send(payload)
            client.close()
        

        def my_server(HOST,PORT):
            global tcpTimeSrvrSock,state
            BUFSIZE = 1024
            ADDR = (HOST, PORT)
            tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
            tcpTimeSrvrSock.bind(ADDR)
            tcpTimeSrvrSock.listen()
            #currentDT = datetime.datetime.now()
            while state:
                self.show_1.insert(tk.END,"Waiting........................\n")
                tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()
                
                #while not addr:
                #    tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()
                #    self.show_1.insert(tk.END,add+"")
                self.show_1.insert(tk.END,"ggg")
                ss=str(tcpTimeClientSock.recv(512).decode())#.decode
                xxx=ss[ss.find("GET")+5:ss.find("HTTP")]
                operation,data=xxx.split("/")
                host_ip="{}".format(addr)#ss.split('/')[3].split(":")[1]
                self.show_1.insert(tk.END,"      "+host_ip+"  "+operation+"    "+data+"\n")       
                if operation=="order":
                    ss=add2orders(data)
                    addtocombobox(self.orders_pop,orders,0)
                elif operation=="cancelorder":
                    ss=deleteorders(data)
                elif operation=="getallorders":
                    ss=getallorders()
                elif operation=="getnumoforders":
                    ss=getnumoforders()
                elif operation=="getpath":
                    ss=getpath(data)

                """m = bytes('order ok',"utf-8")
                BaseHTTPRequestHandler.send_response(200)
                BaseHTTPRequestHandler.send_header('Content-Type', 'text/plain')
                BaseHTTPRequestHandler.send_header('Content-Length', len(m))
                BaseHTTPRequestHandler.end_headers()
                BaseHTTPRequestHandler.wfile.write(m)
                "
                BODY="***KKKK***"
                c=http.client.HTTPConnectionn("192.168.43.221",80)
                c.request("PUT","/file",BODY)
                res=c.getresponse()
                print(res.response,res.status)
                """
                #print(ss[1])
                #send_response(tcpTimeClientSock,ss,200)
                #http_response='HTTP/1.1 200 OK\n\n'+"<h1>"+ss[1]+"</h1>"
                #time.sleep(0.5)    
                #tcpTimeClientSock.send(http_response.encode())
                #tcpTimeClientSock.shutdown(socket.SHUT_WR)
                #tcpTimeClientSock.send(b"hello")
                msg="<h1>"+ss[1]+"</h1>"
            tcpTimeClientSock.send(msg.encode())
            tcpTimeSrvrSock.close()
            if state==0:
                return
            my_server(HOST,PORT)
        def Directionfrompoints(points):
            dirs=[]
            dx,dy=0,0
            for idx in range(len(points)-1):
                x0,y0=points[idx]
                x1,y1=points[idx+1]
                dx,dy=x1-x0,y1-y0
                ss=str(dx)+str(dy)
                print(ss)
                
                #print(Dire.get(ss))
                #dirs.append(Dire.keys[ss])
                

                if dx==0:
                    if dy==1:
                        dirs.append('0')
                    elif dy==-1:
                        dirs.append('4')   
                elif dx==1:
                    if dy==0:
                        dirs.append('6')
                    elif dy==-1:
                        dirs.append('5')
                    elif dy==1:
                        dirs.append('7')
                    elif dx==-1:
                        if dy==0:
                            dirs.append('2')
                        elif dy==-1:
                            dirs.append('3')
                        elif dy==1:
                            dirs.append('1')
                
            return dirs
        #.........................................................................................................Operations(add,cancel,getpath,addtocombobox,getnumoforders,getallorders)
        def add2orders(ord):
            msg=""
            s=int(ord)
            s=[s//MAP_WIDTH,s%MAP_HEIGHT]
            if s[0]>MAP_WIDTH or s[1]>MAP_HEIGHT  or field[s[0]][s[1]]==jps.OBSTACLE:
                return (0,"err")
            print(s)
            if ord not in orders:
                orders.append(ord)
                msg=str(ord)+"  Added, all("+str(len(orders)-1)+")\n"
                return (1,msg)
            else:
                tmp_pos=orders.index(ord)
                msg=str(ord)+"  exist,before("+str(tmp_pos)+")\n"
                return (0,msg)
        #.......................................................
        def deleteorders(ord):
            msg=""
            if ord not in orders:
                msg="Order( "+ord+" )not exist  "+str(len(orders))+" person\n"
                return (1,msg)
            else:
                orders.remove(ord)
                msg="Order( "+ord+" )deleted  "+str(len(orders))+" person\n"
                return (0,msg)
        #.......................................................
        def getnumoforders():
            return "Number of ordesrs is: "+str(len(orders))
        #.......................................................
        def getallorders():
            return "Orders are:"+ ' '.join(orders)
        #.......................................................
        def getpath(parameters):
            global points
            #try: 
            [field,MAP_WIDTH,MAP_HEIGHT]=mapp.init_map(self.usedmap.get())
            [s,g]=parameters.split('_')
            s=int(s)
            g=int(g)
            sx,sy,gx,gy=[s//MAP_HEIGHT,s%MAP_HEIGHT,g//MAP_HEIGHT,g%MAP_HEIGHT]
            print([sx,sy,gx,gy])
        
            if s>MAP_WIDTH*MAP_HEIGHT or g>MAP_WIDTH*MAP_HEIGHT or field[sx][sy]==jps.OBSTACLE or field[gx][gy]==jps.OBSTACLE:
                return [0,"Outborders"]  
            
            path=jps.jps(field, sx,sy,gx,gy)
            print(path)
            
            points=jps.get_full_path(path)
            if len(points)==2 and points[0][0]==0:
                return points
            dir=Directionfrompoints(points)
            clr=[]
            for item in dir:
                clr.append(COLORS.get(int(item)))
            return [1,dir,clr]
            #except:
            #    return [0,"error"]
        def addtocombobox(cb,data,p):
            cb["values"]=""
            #for item in data:
                #if str(item) not in cb["values"]:
            #    cb["values"]+=item
            # ",".join(data)
            if p==0:
                tmp="Orders( "+str(len(data))+" ),"+ ",".join(data)
                cb["values"]=tmp.split(",")
            else:
                cb["values"]=data
            cb.current(0)
            #else:
            #self.labelo.config(text="Orders( "+str(len(data))+" )")
        def b_order():
            #gloabl show_1
            val=simpledialog.askstring("Input","Input node to order",parent=self)
            msg=""
            s=int(val)
            s=[s//MAP_WIDTH,s%MAP_HEIGHT]

            if val is not None:
                x=add2orders(val)
                self.show_1.insert(tk.END,x[1])
                addtocombobox(self.orders_pop,orders,0)
            
        def b_cancel():
            #gloabl show_1
            val=simpledialog.askstring("Input","Input node to order",parent=self)
            if val is not None:
                x=deleteorders(val)
                self.show_1.insert(tk.END,x[1])
                addtocombobox(self.orders_pop,orders,0)
        def b_getpath():
            #gloabl show_1
            val=simpledialog.askstring("Input","Input S_G to order",parent=self)

            if val is not None:
                x=getpath(val)

                print(x)
                
                   

                if x[0]!=0:
                    t=["path( "+str(len(x[1]))+" )"]
                    for i in range(len(x[1])):
                        t.append(str(i)+" : "+x[2][i]+"  "+x[1][i]) 
                    addtocombobox(self.path_combo,t,1)
                #self.path_combo.configure()
                else:
                    self.show_1.insert(tk.END,x[1])

        def islocal():
            #global varcheck
            if self.varcheck.get():
                self.e_host.configure(state='disabled')
            else:
                self.e_host.configure(state='normal')
       
        def cleartxt():
            self.show_1.delete("1.0","end")
        def exit():
            self.quit()
            #cc=http.client.HTTOConnection("192.168.43.221",80,timeout=10)
            #cc.getres
            #cc.set_tunnel("192.168.43.221")
            #cc.request("HEAD","/index.html")

        def connect():
            global state
            global tcpTimeSrvrSock
            if  state==0:
                e_host_v,e_port_v=(self.e_host.get(),int(self.e_port.get()))                
                _thread.start_new_thread(my_server,(e_host_v,e_port_v))
                #start_new_thread(my_server,(show_1,e_host_v,e_port_v))
                self.b_connect.config(text="OFF",bg="red")
                state=1
            else:
                tcpTimeSrvrSock.close()
                self.b_connect.config(text="ON",bg="green")
                state=0
'''
def http_get(url):
    try:
        import usocket as socket
    except:
        import socket
    print(url)
    host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    """getaddrinfo: get the IP address of the server
    getaddrinfo function actually returns a list of addresses, and each address has more information than we need. We want to get just the first valid address, and then just the IP address and port of the server.
    """
    s = socket.socket()#Using the IP address we can make a socket and connect to the server
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    """
    HTTP uses port 80 and you first need to send a “GET” request before you can download anything
    """

    while True:
        data = s.recv(500)
        if data:
            print(str(data, 'utf8'), end='')        
        else:
            break
    s.close()
#you can use http_get('http://micropython.org/ks/test.html')
'''
#....................................................................
app = PageOne()
global state
state=0
#os.startfile("E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\www\index.html")#debug
app.mainloop()

