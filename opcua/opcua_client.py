from opcua import Client

# OPC UA 服务器的地址
server_url = "opc.tcp://localhost:4840"

# 连接到 OPC UA 服务器
client = Client(server_url)
client.connect()

# 获取根节点
root_node = client.get_root_node()

# 获取 "process_stage" 变量节点
process_stage_node = root_node.get_child(["0:Objects", "2:MyObject", "2:process_stage"])

# 定义回调函数来处理变量值的更新
def process_stage_changed(node, value, data_type):
    print(f"Process stage updated: {value}")

# 订阅 "process_stage" 变量的值更新
handle = client.subscribe_value_change(process_stage_node, process_stage_changed)

# 保持客户端连接，以接收变量值的更新
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# 取消订阅和断开与 OPC UA 服务器的连接
client.unsubscribe(handle)
client.disconnect()