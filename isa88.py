import time
import threading
import json
from opcua import ua, Server,Client


def get_Device(recipe):
    Device = []
    Source_Tank = {'源罐','水源水','基料','茶叶的水提取物','浓缩汁','乳（复原乳）'}
    Tank_Model = {'调配', '粗滤', '精滤', '碳酸化', '过滤', '稀释', '加热'}
    P_machine = {'杀菌'}
    Filling_Machine = {'灌装'}
    Icing_Machine = {'制冷'}
    for r in recipe:
        if r in Source_Tank:
            Device.append('Source_Tank')
            continue
        if r in Tank_Model:
            Device.append('Tank_Model')
            continue
        if r in P_machine:
            Device.append('P_machine')
            continue
        if r in Filling_Machine:
            Device.append('Filling_Machine')
            continue
        if r in Icing_Machine:
            Device.append('Icing_Machine')
            continue

    print('Device:', Device)
    return Device

class Device:
    def __init__(self, device_type, batch):
        self.device_type = device_type
        self.device_status = "空闲"  # 默认设备状态为"空闲"
        self.batch = batch
        self.start_time = 0
        self.pause_time = 0
        self.run_time = batch/1000  # 设备运行总时长为batch/1000秒
        
    def run(self):
        self.device_status = "运行中"
        self.start_time = time.time()  # 记录设备运行开始的时间
        time.sleep(self.run_time)  # 模拟设备运行的时间
        self.device_status = "已完成"
        # if (self.device_status == "已完成"):
        return self.device_type            

        
    # def pause(self):
    #     if (self.device_status == "运行中")


class ProductionLine:
    def __init__(self, batch, quantity, drink, recipe, Devices,send,client):
        self.Line_status = "空闲"  # 默认生产线状态为"空闲"
        self.drink_type = drink
        self.recipe = recipe
        self.Devices = []
        self.quantity = quantity
        self.batch = batch
        self.current_batch = 0
        self.pointer = 0
        self.thread = None
        self.stop_event = threading.Event()
        self.func_send=send
        self.opcua_client=client

        for device in Devices:
            self.Devices.append(Device(device, self.batch))
        

    def start_production(self):
        self.thread = threading.Thread(target=self._production_process)
        self.thread.start()


    def clear(self):
        # self.stop_event.set()
        self.pointer = 0
        self.current_batch = 0
        self.set_opcua()

    def _production_process(self):        
        self.Line_status = "运行中"
        self.func_send(self.get_state())
        print("生产线开始运行...")
        print(f"生产饮料种类及数量：{self.drink_type}, {self.batch}")
        print(f"配方：{self.recipe}")
        print(f"已生产饮料数量：{self.current_batch}")


        while self.Line_status == "运行中" and self.pointer < len(self.recipe)and not self.stop_event.is_set():
            print("当前生产流程：", self.Devices[self.pointer].run() + '已完成')
            self.set_opcua()
            self.pointer += 1
            
            self.func_send(self.get_state())

        if self.Line_status == "暂停中" and self.pointer < len(self.recipe):
            self.Line_status = "已暂停"
            self.func_send(self.get_state())
            print('生产线当前状态：' + self.Line_status)

        elif self.pointer == len(self.recipe):
            self.current_batch += self.batch
            self.func_send(self.get_state())

            # 判断是否达到总的生产数量，如果没有，则开始新一批的生产
            if self.current_batch < self.quantity:
                self.pointer = 0
                self.func_send(self.get_state())
                self.thread = threading.Thread(target=self._production_process)
                self.thread.start()
            else:
                self.Line_status = "已完成"
                self.func_send(self.get_state())
                print("生产线全部生产结束", f"生产饮料种类及数量：{self.drink_type}, {self.current_batch}")
                self.clear()

    def pause(self):
        if (self.pointer < len(self.recipe) and self.Line_status=='运行中'):
            self.Line_status = "暂停中"
            self.func_send(self.get_state())
            print('当前状态：'+self.Line_status)

    def restart(self):
        if self.Line_status == "已暂停" or self.Line_status == "已停止":
            self.Line_status = "运行中"
            self.func_send(self.get_state())
            print('生产线当前状态：'+self.Line_status)
            # if self.Line_status == "已停止":
            #     self.stop_event.clear()
            self.thread = threading.Thread(target=self._production_process)
            self.thread.start()
        elif self.Line_status == "暂停中":
            print("restart alarm: 现在正在暂停中")
        elif self.Line_status == "运行中":
            print("restart alarm: 现在正在运行中")

    def stop(self):
        if (self.Line_status=='运行中'):
            self.Line_status='停止中'
            self.func_send(self.get_state())
            self.clear()
            self.Line_status = '已停止'
            self.func_send(self.get_state())
            print('生产线当前状态：' + self.Line_status)
    def get_state(self):
        dic={'Line':self.Line_status,'pointer':self.pointer,'current_batch':self.current_batch}
        return json.dumps(dic)
    
    def set_opcua(self):
        if self.pointer<len(self.recipe):
            node = self.opcua_client.get_node("ns=2;i=2")
            datavalue = ua.DataValue(ua.Variant(self.recipe[self.pointer], ua.VariantType.String))
            print(datavalue,self.recipe[self.pointer])
            node.set_value(datavalue)
            



if __name__ == '__main__':
    drink = ' 碳酸饮料'
    recipe = ['基料','调配','制冷','碳酸化','杀菌','灌装']
    Devices = get_Device(recipe)
    # states = ['水源水','已调配', '已制冷','已碳酸化','已杀菌',' 碳酸饮料']
    Line = ProductionLine(1000, 2000, drink, recipe, Devices)
    Line.start_production()


    # time.sleep(2)
    # Line.pause()
    # print("first time restart")
    # Line.restart()
    # time.sleep(1)
    # print('seconde time restart')
    # Line.restart()


    time.sleep(2)
    print('stop')    
    Line.stop()
    time.sleep(2)
    print('restart')
    Line.restart()