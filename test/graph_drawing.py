from graphviz import Graph

import shutil

def get_Devices_img(Devices):
    dot = Graph("Structure graph",format='png')
    # dot.attr(font)
    dot.attr(rankdir='LR')
    last_Device_name = None
    usd_Devices = set()
    cnt = 0
    for Device in Devices:
        Device_name = Device
        if Device in usd_Devices:
            Device_name += str(cnt)
        dot.node(Device_name, shapefile='./test/'+Device+'.png')
        if(last_Device_name != None):
            dot.edge(last_Device_name, Device_name,fontsize="60pt",minlen='1')
        last_Device_name = Device_name
        usd_Devices.add(Device)
        cnt += 1

    # 跟view一样的用法(render跟view选择一个即可)，一般用render生成图片，不使用view=True,view=True用在调试的时候
    dot.render(filename='MyPicture')

def get_Devices(recipe):
    Devices = []
    Source_Tank = {'水源水','基料','茶叶的水提取物','浓缩汁','乳（复原乳）','源罐'}
    Tank_Model = {'调配', '粗滤', '精滤', '碳酸化', '过滤', '稀释', '加热'}
    P_machine = {'杀菌'}
    Filling_Machine = {'灌装'}
    Icing_Machine = {'制冷'}
    for r in recipe:
        if r in Source_Tank:
            Devices.append('Source_Tank')
            continue
        if r in Tank_Model:
            Devices.append('Tank_Model')
            continue
        if r in P_machine:
            Devices.append('P_machine')
            continue
        if r in Filling_Machine:
            Devices.append('Filling_Machine')
            continue
        if r in Icing_Machine:
            Devices.append('Icing_Machine')
            continue

    print('Device:', Devices)
    return Devices


def copy_image():

# 指定图片的文件名和路径
    image_filename = 'MyPicture.png'

# 指定目标文件夹路径
    destination_folder = './front/src/assets/graphviz/'

# 使用 shutil 模块的 copy 函数复制图片到目标文件夹
    shutil.copy(image_filename, destination_folder)


def generate_image(recipe):
    Devices = get_Devices(recipe)
    
    get_Devices_img(Devices)
    copy_image()



if __name__ == '__main__':
    recipe = ['基料','调配','制冷','灌装']
    generate_image(recipe)