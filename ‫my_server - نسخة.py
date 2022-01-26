import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk,Image
import time
import datetime
from socket import *
import time
from time import ctime
import _thread
from flask import Flask, render_template, make_response, jsonify, request,redirect,url_for
import os


IP='192.168.43.163'
PORT='3300'

LARGE_FONT= ("Verdana", 12)

def my_server(show_1,HOST,PORT):

    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(10)
    currentDT = datetime.datetime.now()

    while True:
        show_1.insert(tk.END,"waiting for connection...")
        show_1.insert(tk.END,"\n")
        tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()
        show_1.insert(tk.END,"connected {}".format(addr))
        show_1.insert(tk.END,"\n")
        ss=str(tcpTimeClientSock.recv(50).decode())#.decode
        
        xxx=ss[ss.find("GET")+5:ss.find("HTTP")]
        operation,data=xxx.split("/")
     
        show_1.insert(tk.END,operation)
        show_1.insert(tk.END,"\n")
        show_1.insert(tk.END,data)
        show_1.insert(tk.END,"\n")
        
            
        if operation=="order":
            
            s="order"
        elif operation=="cancel":

            s="cancel"

        elif operation=="allorders":

            s="allorders"

        elif operation=="getpath":

            s="getpath"


        

        path=[22,44,55,77]
        #oo=bytearray()
        #for i in path:
        #    oo.append(i)
        #=" ".join(path)
        #show_1.insert(tk.END,s+"\n")

        #tcpTimeClientSock.send(oo)
        #show_1.insert(tk.END,"'Done sending'\n")
        http_response='HTTP/1.0 200 OK\n\n'+s
                #tcpTimeClientSock.send(oo)
        tcpTimeClientSock.sendall(http_response.encode())

        """
        msg='Thank you for connecting'
        m1=msg.encode('utf-8')
        HEADER_LENGTH=10
        m2h=f"{len(m1):<{HEADER_LENGTH}}".encode("UTF-8")
        tcpTimeClientSock.send(m1+m2h)
        """
        tcpTimeClientSock.close() 
    #tcpTimeSrvrSock.close()
       
    """
        while True:
            data = tcpTimeClientSock.recv(BUFSIZE)
            if not data:
                break
            tcpTimeClientSock.send(bytes(currentDT.strftime("%I:%M:%S %p"),'utf-8'))
            show_1.insert(tk.END,data.decode('utf-8'))
            show_1.insert(tk.END,"\n")
            print(data.decode('utf-8'))
        tcpTimeClientSock.close()
    tcpTimeSrvrSock.close()
    """

class Page(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        #container.resizable(False,False)
        
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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

        label_username = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")

        entry_username = tk.Entry(self,show="*",width=50)

        entry_password = tk.Entry(self, show="*",width=50)

        label_username.grid(row=2, column=0, sticky='NSEW',padx=10,pady=10)
        label_password.grid(row=3, column=0, sticky='NSEW',padx=10,pady=10)
        entry_username.grid(row=2, column=1,sticky='NSEW',padx=10,pady=10)
        entry_password.grid(row=3, column=1,sticky='NSEW',padx=10,pady=10)

        #checkbox = tk.Checkbutton(self, text="Keep me logged in")
        #checkbox.grid(row=4, column=1,sticky='NSEW',padx=10,pady=10)


        logbtn = tk.Button(self, text="Login", bg="BlACK", fg="White",command=lambda: login_btn_clicked())
        logbtn.grid(row=5, column=1,sticky='NSEW', padx=10, pady=10)
    
        def login_btn_clicked():
             
            # print("Clicked")
            username = entry_username.get()
            password = entry_password.get()

            #if len(username) and len(password) > 2:
                # print(username, password)

                #if username == "admin" and password == "admin":
            controller.show_frame(PageOne)
                # display a ,essage if username and password is incorrect!
                #else:
                #    messagebox.showinfo(self,"Invalid username or password ! ")

            #else:
            #    messagebox.showinfo(self,"Enter Username and Password")
       

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True

        clock = tk.Label(self, font=('times', 10, 'bold'),fg="Black")
        clock.grid(row=0,column=5, sticky="NSNESWSE",padx=8,pady=8)

        def tick():
            time2=time.strftime('%H:%M:%S')
            clock.config(text=time2)
            clock.after(200,tick)
        tick()

        label = tk.Label(self, text="Server Software ", font=('times', 20, 'bold'),fg="Black")
        label.grid(row=0, column=2, columnspan=1, padx=8, pady=8, sticky="NSNESWSE")

        l_host=tk.Label(self,text="Host Ip",font=('times', 14, 'bold'))
        l_host.grid(row=1, column=0, padx=8, pady=8, sticky="NSNESWSE")

        
        checkbox = tk.Checkbutton(self, text="Local")
        checkbox.grid(row=1, column=3,padx=10,pady=10)

        img=ImageTk.PhotoImage(Image.open("E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\stm_guicserver_webclient_server(jps)_esp\MIET.png"))

        '''
        canvas=tk.Label(self,image=img)
        canvas=tk.Canvas(self,width=50,height=50)
        canvas.create_image(20,20,anchor="ne",image=img)
        canvas.grid(row=1,rowspan=5,columnspan=5,column=5)
        '''
        e_host=tk.Entry(self)
        e_host.grid(row=1, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_host.insert(tk.END,IP)


        l_port=tk.Label(self,text="Port",font=('times', 14, 'bold'))
        l_port.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_port=tk.Entry(self)
        e_port.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_port.insert(tk.END,PORT)

        message_label=tk.Label(self,text="Client Message",font=("Arial",12,'bold'))
        message_label.grid(row=3,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")


        
        scrollbar_y = tk.Scrollbar(self)
        scrollbar_y.grid(row=4, column=3,rowspan=8,sticky="NSEW")


        show_1=tk.Text(self,height=8, width=35, yscrollcommand=scrollbar_y.set,
                       bg="Grey",fg="White")
        show_1.grid(row=4, column=0,rowspan=4,columnspan=3,sticky="NSEW")

      


        b_connect=tk.Button(self,text=" Connect",command=lambda: connect())
        b_connect.grid(row=4,column=4,padx=10,pady=5,sticky="nsew")

        b_disconnect=tk.Button(self,text=" disconnect",command=lambda: disconnec())
        b_disconnect.grid(row=4,column=5,padx=10,pady=5,sticky="nsew")

        b_order=tk.Button(self,text=" Order",command=lambda: order())
        b_order.grid(row=5,column=4,padx=10,pady=10,sticky="nsew")
        
        b_cancel=tk.Button(self,text=" cancel",command=lambda: cancel())
        b_cancel.grid(row=5,column=5,padx=10,pady=10,sticky="nsew")

        b_getpath=tk.Button(self,text=" Getpath",command=lambda: getpath())
        b_getpath.grid(row=6,column=4,padx=10,pady=10,sticky="nsew")


        b_clear=tk.Button(self,text=" Clear",command=lambda: cleartxt())
        b_clear.grid(row=6,column=5,padx=10,pady=10,sticky="nsew")

        n=tk.StringVar()
        cb=ttk.Combobox(self,values=["Orders"],state='readonly',textvariable=n,width=7)
        cb.grid(row=7, column=4,rowspan=1,columnspan=1)
        cb.current(0)
        
        

        def runner():
            global after_id
            global secs
            secs += 1
            if secs % 2 == 0:  # every other second
                e_host_v=e_host.get()
                e_port_v=int(e_port.get())

            #after_id = self.after(1000, runner)  # check again in 1 second

        def connect():
            # CONNECT COM PORT
            e_host_v=e_host.get()
            e_port_v=int(e_port.get())
            _thread.start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            #start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            global secs
            secs = 0
            #runner()  # start repeated checking
        def disconnec():
            global after_id,cccc
            if after_id:
                self.after_cancel(after_id)
                after_id = None
            
            show_1.insert(tk.END,"Disconnected")


app = Page()

os.startfile("E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\www\index.html")#debug
app.mainloop()

