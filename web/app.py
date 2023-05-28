from flask import Flask,request
from flask_cors import CORS
from opcua import ua, Server,Client
import time

opcua_client = Client("opc.tcp://localhost:4840") 

app = Flask(__name__)
CORS(app)

@app.route('/api/stage',methods=["POST","GET"])
def set_process():
    data= request.get_json()
    if not data:
        print("empty")
    
    node = opcua_client.get_node("ns=2;i=2")
    
    print(data['stage'])
    print(data['end'])

    if int(data['end'])==0:
        if data['stage']!='无':
            datavalue = ua.DataValue(ua.Variant(data['stage'], ua.VariantType.String))
            node.set_value(datavalue)
            time.sleep(3)
            datavalue = ua.DataValue(ua.Variant('无', ua.VariantType.String))
            node.set_value(datavalue)
    else:
        datavalue = ua.DataValue(ua.Variant(data['stage'], ua.VariantType.String))
        node.set_value(datavalue)

            



    return "Hello"

if __name__ == '__main__':
    opcua_client.connect()
    app.run(port=8443)