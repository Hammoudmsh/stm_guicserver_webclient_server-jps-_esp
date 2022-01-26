from flask import Flask, render_template, make_response, jsonify, request,redirect,url_for
import jps
import mapp
app=Flask(__name__)

# Image test to load a map from an image
HOST='192.168.43.163'
PORT = 3300
[field,MAP_WIDTH,MAP_HEIGHT]=mapp.init_map(map_name="map1")    




cur_node=""
paths={}#
orders=[]
commands={'home': "/home",
    'order':"/order/<parameters>"
}
global points
points=[]
#.........................................................................................................debug
COLORS={0:"Green",1:"Blue",2:"Black",3:"Green Light",4:"Yellow",5:"Blue Light",6:"Brown",7:"Red"}
'''
Dir_clrs=[]
RIGHT,DIG1,UP,DIG2,LEFT,DIG3,DOWN,DOG4=0,1,2,3,4,5,6,7
def Get_DIRECTIONS_COLORS(r,c): 
    Dir_clrs[RIGHT]=0 if c%2==0 else 1
    Dir_clrs[DIG1]=5 if r%2==0 else 4
    Dir_clrs[UP]=3 if r%2==0 else 2
    Dir_clrs[DIG2]=4 if r%2==0 else 5
    Dir_clrs[LEFT]=1 if c%2==0 else 0
    Dir_clrs[DIG3]=2 if r%2==0 else 3
    Dir_clrs[DOWN]=2 if r%2==0 else 3
    Dir_clrs[DOG4]=7 if r%2==0 else 6
    return Dir_clrs
    '''
def Directionfrompoints():
    dirs=[]
    dx,dy=0,0
    for idx in range(len(points)-1):
        x0,y0=points[idx]
        x1,y1=points[idx+1]
        dx,dy=x1-x0,y1-y0
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
#---------------------------------------------------------------------------------------

#............................................................
#@app.route("/")
# def home():
#  #return render_template('index.html')
 #return "<h1 style='color:blue'>Enter where to go</h1>"
#...........................................................Home
@app.route("/home",methods=["GET","POST"])
def home():
    return render_template('index.html')
#..........................................................(x1,y1)---(x2,y2)
@app.route("/order/<parameters>",methods=["GET","POST"])
def order(parameters):
    state=add2orders_n(parameters)

    #res = make_response(jsonify(mmm="Order registered"), 200)
    #return res
    return state   

@app.route("/cancelorder/<parameters>",methods=["GET","POST"])
def cancelorder(parameters):
    state=deleteorders_n(parameters)  
    return state

@app.route("/getnumoforders",methods=["GET","POST"])
def getnumoforders():
    state=getnumoforders()  
    return state

@app.route("/getallorders",methods=["GET","POST"])
def getallorders():
    state="  ".join([str(e) for e in orders]) 
    state="<h1>"+state+"</h1>"

    return state



@app.route("/getpath/<parameters>",methods=["GET","POST"])
def getpath(parameters):
    [s,g]=parameters.split('_')
    s=int(s)
    g=int(g)
    if s>MAP_WIDTH*MAP_HEIGHT or g>MAP_WIDTH*MAP_HEIGHT:
        return "<h1 style='color:red'>Wrong numbers</h1>"
    sg=[s//MAP_WIDTH,s%MAP_HEIGHT,g//MAP_WIDTH,g %MAP_HEIGHT]
    path=jps.jps(field, sg[0], sg[1], sg[2], sg[3])
    print(path)
    global points
    points=jps.get_full_path(path)
    if len(points)==1 and points[0][0]==-1:
        return "<h1 style='color:red'>Path not exist:</h1>"
    x=Directionfrompoints()
    state1="<h1 style='color:green'>Path is:</h1><h2>"+''.join(x)+"</h2>" 
    xx=''
    for item in x:
        xx+=" "+COLORS.get(int(item))
    state2="<h1 style='color:green'>Path is:</h1><h2>"+xx+"</h2>"
    #x=request.form["mmm"]
    return redirect(url_for(home))
    #return state1+state2
"""
def add2orders(parameters):
    tmp=int(parameters)
    if tmp not in orders:
        orders.append(tmp)#[tmp//MAP_WIDTH,tmp%MAP_HEIGHT]
        return "<h1 style='color:green'>Order registered </h1><h2> "+str(len(orders)-1)+" person</h2>"
    tmp_pos=orders.index(tmp)
    return "<h1 style='color:red'>Repated order registered </h1><h2> "+str(tmp_pos)+" person</h2>"
"""

def add2orders_n(parameters):
    tmp_order=parameters.split(',')
    state=""
    s=""
    for item in tmp_order:
        tmp=int(item)
        s=[tmp//MAP_WIDTH,tmp%MAP_HEIGHT]
        if s[0]>MAP_WIDTH or s[1]>MAP_HEIGHT  or field[s[0]][s[1]]==jps.OBSTACLE:
            state+="<h1>error( "+item+" )</h1><br>"
        else:
            if tmp not in orders:
                orders.append(tmp)#[tmp//MAP_WIDTH,tmp%MAP_HEIGHT]
                state+="<br><h1 style='color:green'>Order( "+item+" )registered  "+str(len(orders)-1)+" person</h1>"
            else:
                tmp_pos=orders.index(tmp)
                state+="<br><h1 style='color:green'>Order( "+item+" )Not registered  "+str(tmp_pos)+" person</h1>"
    return state
def deleteorders_n(parameters):
    tmp_order=parameters.split(',')
    state=""
    for item in tmp_order:
        tmp=int(item)
        if tmp  in orders:
            orders.remove(tmp)
            #del orders[tmp_order]
            state+="<br><h1 style='color:red'>Order deleted  "+str(len(orders))+" person</h1>"
        else:
            state+="<br><h1 style='color:black'>Order( "+item+" )Not exist </h1>"
    return state
def getnumoforders():
    return "<h1 style='color:gray'>Number of orders "+str(len(orders))+" person</h1>"

"""
    points=[xs,ys,xg,yg]=parameters.split('_')
    print(points)
    if len(points) == 4:
        return [[int(xs),int(ys)] [int(xg),int(yg)]]
    elif len(points) == 2:
        return[[int(xs),int(ys)]]
    elif len(points) == 1:
        pass
    else:
        return -1
    """
"""
@app.route("/qstr")
def qs():
    if request.args:
        req = request.args
        res = {}
        for key, value in req.items():
            res[key] = value
        res = make_response(jsonify(res), 200)
        return res
    res = make_response(jsonify({"error": "No Query String"}), 404)
    return res

@app.route("/json")
def get_json():
    res = make_response(jsonify(INFO), 200)
    return res

@app.route("/json/<collection>/<member>")
def get_data(collection, member):
    print("getting the value of %s in the collection %s"%(member,collection))
    if collection in INFO:
        member = INFO[collection].get(member)
        if member:
            res = make_response(jsonify({"res":member}), 200)
            return res

        res = make_response(jsonify({"error": "Not found"}), 404)
        return res

    res = make_response(jsonify({"error": "Not found"}), 404)
    return res

# Post Method

@app.route("/json/<collection>", methods=["POST"])
def create_col(collection):

    req = request.get_json()

    if collection in INFO:
        res = make_response(jsonify({"error": "Collection already exists"}), 400)
        return res

    INFO.update({collection: req})

    res = make_response(jsonify({"message": "Collection created"}), 201)
    return res

# Put Method

@app.route("/json/<collection>/<member>", methods=["PUT"])
def put_col_mem(collection,member):

    req = request.get_json()

    if collection in INFO:
        if member:
            print(req)
            INFO[collection][member] = req["new"]
            res = make_response(jsonify({"res":INFO[collection]}), 200)
            return res

        res = make_response(jsonify({"error": "Not found"}), 404)
        return res

    res = make_response(jsonify({"error": "Not found"}), 404)
    return res

# Delete Method
@app.route("/json/<collection>", methods=["DELETE"])
def delete_col(collection):

    if collection in INFO:
        del INFO[collection]
        res = make_response(jsonify(INFO), 200)
        return res

    res = make_response(jsonify({"error": "Collection not found"}), 404)
    return res
"""

import os #debug
if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    os.startfile("E:\Mohammed\Micro Controller\STM\Thesis\Master_Project\Project_code\w\www\index.html")#debug
    app.run(host=HOST, port=PORT)
    
    