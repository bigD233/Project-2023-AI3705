from flask import Flask,request
from flask_cors import CORS
from opcua import ua, Server,Client
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from flask_socketio import SocketIO, emit
from isa88 import *


opcua_client = Client("opc.tcp://localhost:4840") 

app = Flask(__name__)
sockets = Sockets(app)
CORS(app)

Line=None


@sockets.route('/Linestatus',methods=["POST","GET"])
def get_status(ws):
    print("hello")
    while not ws.closed:
        global Line
        msg = ws.receive()
        
        msg=msg.split(',')
        recipe=msg[1:]
        quantity=int(msg[0])
        
        print("generate image")
        Devices = get_Device(recipe)
        
        Line = ProductionLine(1000, quantity, 'drink', recipe, Devices,ws.send,opcua_client)
        Line.start_production()
        now = 'hhhhh'
        
@sockets.route('/operation',methods=["POST","GET"])
def get_status(ws):
    print("hello")
    while not ws.closed:
        global Line
        msg = ws.receive()
        print(msg)
        if Line ==None:
            ws.send("Your Line has been not started!")
        else:
            if int(msg)==1 :
                print("Try to pause!")
                Line.pause()
                ws.send("Pause successfully!")
            if int(msg)==2:
                print("Try to stop")
                Line.stop()
                ws.send("Stop successfully!")
            if int(msg)==3:
                print("Try to restart!")
                Line.restart()
                ws.send("Restart successfully!")
            if int(msg)==4:
                print("Try to reset!")
                Line.clear()
                ws.send("Ret successfully!")

    return "Hello"

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8443), app, handler_class=WebSocketHandler)
    opcua_client.connect()
    server.serve_forever()