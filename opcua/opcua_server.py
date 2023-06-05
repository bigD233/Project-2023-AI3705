from opcua import ua, Server
import time
# 创建 OPC UA 服务器
server = Server()
server.set_endpoint("opc.tcp://localhost:4840")  # 设置服务器端点
namespace = server.register_namespace("MyNamespace")  # 注册命名空间

# 创建对象节点
objects = server.get_objects_node()
my_object = objects.add_object(namespace, "MyObject")

# 创建 "process_stage" 变量节点
process_stage = my_object.add_variable(namespace, "process_stage", "")
process_stage.set_writable()  # 设置变量可写

# 启动 OPC UA 服务器
try:
    server.start()
except KeyboardInterrupt:
    server.stop()

# 模拟不同饮料的工艺流程，并将其写入 OPC UA 变量
drink_processes = {
    "coke": ["Mix ingredients", "Carbonation", "Bottling"],
    "orange_juice": ["Extract juice", "Filtration", "Pasteurization", "Packaging"],
    "coffee": ["Grinding", "Brewing", "Filtering", "Packaging"]
}
