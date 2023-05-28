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
# try:
#     while True:
#         for drink, process_steps in drink_processes.items():
#             print(f"Processing {drink}:")
#             for step in process_steps:
#                 # 写入当前步骤到 OPC UA 变量
#                 process_stage.set_value(step)
#                 print(f"Current process stage: {step}")
#                 # 在这里可以进行其他处理或等待一段时间，模拟实际的工艺过程
#                 time.sleep(1)
#             print()
# except KeyboardInterrupt:
#     pass


# 停止 OPC UA 服务器

# server.stop()