<script setup>
import { useRouter } from 'vue-router'

import Header from '@/components/StartHeader.vue'
import {
  CirclePlus, Files, Select, CloseBold, IceDrink,
  IceCreamRound, Mug, Operation, Shop, DeleteFilled, Refrigerator
} from '@element-plus/icons-vue'
import img1 from '../assets/1.png'
import img2 from '../assets/2.png'
import img3 from '../assets/3.png'
import img4 from '../assets/4.png'
import img5 from '../assets/5.png'
import img6 from '../assets/6.jpg'
import img7 from '../assets/7.jpg'
import img8 from '../assets/8.jpg'
import { markRaw, ref, inject, watch, onUnmounted } from 'vue'
import myimg from '../assets/graphviz/MyPicture.png'


// import SelectComp from '@/components/SelectComp.vue'
// import Footer from '@/components/StartFooter.vue'


const router = useRouter()


const status = ref('') //进度条状态
var timer  //计时器
const url = ref('')
const count = ref(0)  //进度条计数
const num = ref(1000)
const component_list = ref([])
const component = ref('')    // 工艺名称
const typevalue = ref('')   // 饮料种类名称
const percentage = ref(0)  // 进度条百分比
const if_increase = ref(true)  //是否继续增长
const if_disable = ref(false)
const if_show = ref(true)  //是否展示走马灯
const if_show1 =ref(false)  //是否展示自制图片
// const remarkCaruselUp = ref(null)
const if_connection1 = ref(false);
const if_connection2 = ref(false);
const if_connection3 = ref(false);
const axios = inject('axios'); //用于发送状态信息
const product_list = ref([]);
const linestatus = ref('空闲');   //表示生产线状态
const operation = ref(0); // 0-表示正常运行 1-表示暂停 2-表示停止 3-重启 4-reset 5-生成图片

for (var i = 0; i < 9; i++) {
  product_list.value.push(`/src/assets/imgs/page${i}.jpg`)
}

var ws = new WebSocket(
  `ws://localhost:8443/Linestatus`
);
var ws1 = new WebSocket(
  `ws://localhost:8443/operation`
)


ws.onopen = function (evt) {
  console.log("Connection1 open ...");
  if_connection1.value = true;

};

ws1.onopen = function (evt) {
  console.log("Connection2 open ...");
  if_connection2.value = true;

};



function send() {
  if_show1.value=true;
  const send_list = ref([])
  if (if_connection1.value == true) {
    send_list.value.push(num.value)
    for (var i = 0; i < component_list.value.length; i++) {

      send_list.value.push(component_list.value[i]['value'])
    }
    ws.send(send_list.value);
    send_list.value = [];
  }

}

function send_operation() {
  ws1.send(operation.value)
}





ws1.onmessage = function (e) {
  console.log(e.data);
}


ws.onmessage = function (e) {

  console.log(JSON.parse(e.data));
  count.value = JSON.parse(e.data)['pointer']
  percentage.value = Number((JSON.parse(e.data)['current_batch'] * 100 / num.value).toFixed(1))

  linestatus.value = JSON.parse(e.data)['Line']

};
// 4.卸载前, 关闭链接
onUnmounted(() => {
  ws.close();
  ws1.close();

});



// const img_lists = [
//   {
//     value: img1
//   },
//   {
//     value: img2
//   },
//   {
//     value: img3
//   },
//   {
//     value: img4
//   },
//   {
//     value: img5
//   },
// ]

const options = [
  {
    value: '饮用天然矿泉水',
    label: '饮用天然矿泉水',
    process: ['源罐', '粗滤', '精滤', '杀菌', '灌装'],
    src: img1,
    index: 0
  },
  {
    value: '碳酸饮料',
    label: '碳酸饮料',
    process: ['源罐', '调配', '制冷', '碳酸化', '杀菌', '灌装'],
    src: img2,
    index: 1
  },
  {
    value: '茶饮料',
    label: '茶饮料',
    process: ['源罐', '调配', '过滤', '杀菌', '灌装'],
    src: img3,
    index: 2
  },
  {
    value: '果蔬饮料',
    label: '果蔬饮料',
    process: ['源罐', '稀释', '调配', '杀菌', '灌装'],
    src: img4,
    index: 3
  },
  {
    value: '含乳饮料',
    label: '含乳饮料',
    process: ['源罐', '加热', '调配', '杀菌', '灌装'],
    src: img5,
    index: 4
  },
  {
    value: '蜂蜜饮料',
    label: '蜂蜜饮料',
    process: ['源罐', '稀释', '调配', '过滤', '杀菌', '灌装'],
    src: img6,
    index: 5
  },
  {
    value: '功能饮料',
    label: '功能饮料',
    process: ['源罐', '调配', '加热', '杀菌', '灌装'],
    src: img7,
    index: 6
  }, {
    value: '植物蛋白饮料',
    label: '植物蛋白饮料',
    process: ['源罐', '调配', '过滤', '杀菌', '灌装'],
    src: img8,
    index: 7
  }
]

const otherComp = [
  {
    value: '调配'
  },
  {
    value: '粗滤'
  }, {
    value: '精滤'
  }, {
    value: '碳酸化'
  }, {
    value: '过滤'
  }, {
    value: '稀释'
  }, {
    value: '加热'
  },
]

const dialogFormVisible = ref(false);


function percentage_increase() {
  if (component_list.value.length != 0) {
    if (if_increase) {
      timer = setInterval(increase, 1500);
      if_increase.value = false;
    }
  }
  else {
    ElMessage({
      message: '您未选择任何一项加工工艺！',
      type: 'warning',
    })
  }
}


function increase() {
  var step = 100 / component_list.value.length
  if (percentage.value < 100) {
    if (Math.abs(percentage.value + step - 100) > 1) {
      percentage.value = Number((percentage.value + step).toFixed(1));
      count.value += 1;
      console.log(count.value)
    }
    else {
      status.value = 'success'
      percentage.value = 100;
      count.value += 1;
      console.log(count.value)
    }
  }

}




function judgeSelect() {  //选择饮料
  if (typevalue.value != '') {
    if_disable.value = true;  //配方确定，停止选择
    component_list.value = [];
    if_show.value = false;
  }

  for (const item of options) {
    console.log(item);
    if (item.value == typevalue.value) {  //找到配方
      // remarkCaruselUp.value.setActiveItem(item.index)
      url.value = item.src
      console.log(item.src);
      for (var i = 0; i < item.process.length; i++) {
        addComponent(item.process[i], 2);  //添加配方
      }
      break;
    }
    // console.log(component_list.value)

  }
}


function addOtherComponent() {
  if (component.value != '') {
    component_list.value.push({ value: component.value, svg: markRaw(Operation) })
  }
}

function addComponent1() {  //加单个装置
  if (component.value != '') {
    addComponent(component.value, 1);
    component.value = '';
    checkCorrection();
  }
  else {
    ElMessage({
      message: '您未选择任何一项加工工艺！',
      type: 'warning',
    })
  }

}

function checkCorrection() {
  for (const item of options) {
    if (component_list.value.length == item.process.length) {
      var flag = true;
      for (var i = 0; i < item.process.length; i++) {
        if (component_list.value[i].value != item.process[i]) {
          flag = false;
        }
      }
      if (flag) {  //找到饮料
        if_disable.value = true
        typevalue.value = item.value;
        // setActiveItem(item.index)
        url.value = item.src
        if_show.value = false;
        console.log(item.src)
      }
    }
  }
}


function addComponent(component, num) {


  switch (component) {
    case '源罐':
      component_list.value.push({ value: "源罐", svg: markRaw(Files) });
      break;
    case '冷却':
      component_list.value.push({ value: "制冷", svg: markRaw(IceCreamRound) })
      break;
    case '灌装':
      component_list.value.push({ value: "灌装", svg: markRaw(Mug) })
      break;
    case '杀菌':
      component_list.value.push({ value: "杀菌", svg: markRaw(Refrigerator) })
      break;
    default:
      if (num == 1) {  //多功能罐
        component = ''
        dialogFormVisible.value = true;
      }
      if (num == 2) {
        component_list.value.push({ value: component, svg: markRaw(Operation) })
      }

  }



}

function clearList() {
  typevalue.value = '';
  component_list.value = [];
  component.value = '';
  if_disable.value = false;
  percentage.value = 0;
  if_increase.value = true;
  clearInterval(timer);
  url.value = '';
  count.value = 0;
  if_show.value = true;
  status.value = '';
  linestatus.value = '空闲';
  num.value = 1000;
}

//监听count变化
// watch(count, (newCount) => {
//   // 在 count 变量发生变化时发送 POST 请求
//   if (newCount != 0) {
//     axios
//       .post('stage', { stage: component_list.value[newCount - 1].value, end: component_list.value.length - newCount }, {
//         headers: {
//           'Access-Control-Allow-Origin': 'http://localhost:5173'  // 替换为实际的前端域名
//         }
//       })
//       .then((response) => {
//         // console.log(component_list.value[newCount - 1])
//         console.log("Send the process stage successfully!");
//       })
//       .catch((error) => {
//         ElMessage.error("向服务器传输工艺指令过程中出错！")
//       })
//   }
//   else {
//     axios
//       .post('stage', { stage: '无', end: 0 }, {
//         headers: {
//           'Access-Control-Allow-Origin': 'http://localhost:5173'  // 替换为实际的前端域名
//         }
//       })
//       .then((response) => {
//         // console.log(component_list.value[newCount - 1])
//         console.log("Send the process stage successfully!");
//       })
//       .catch((error) => {
//         ElMessage.error("向服务器传输工艺指令过程中出错！")
//       })
//   }
// });





</script>

<template>
  <el-container style="width: 100%; min-height:100%; min-width: 100vmin;">
    <el-header style="margin: 0; padding: 0 ;">
      <Header />
    </el-header>
    <el-container>

      <el-aside width="30vmax" style="margin-top: 7vmin;margin-left: 2vmax;">

        <!-- 选择种类部分 -->
        <el-card class="box-card" style="margin-top: 2vmin ;background-color: #2F5597;">
          <div class="card-header">
            <div style="font-weight: bold;color: white;">选择饮料种类</div>

            <el-select v-model="typevalue" filterable placeholder="选择要生产的饮料" size="large" @change="judgeSelect">

              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </div>
        </el-card>


        <!-- 选择工艺部分 -->
        <el-card class="box-card" style="margin-top: 2vmin;background-color: #2F5597;">
          <template #header>
            <div class="card-header">
              <p style="font-weight: bold;color: white;">自选工艺类型</p>
              <el-button type="info" plain :icon="CirclePlus" :disabled="if_disable" @click="addComponent1();">添加</el-button>
            </div>
          </template>
          <div class="mb-2 flex items-center text-sm">

            <el-dialog v-model="dialogFormVisible" title="输入具体工艺名称" draggable
              style="width:22vmax;background-color: #d9ecff;" align-center>

              <el-select v-model="component" placeholder="输入多功能罐对应的工艺名称" size="large" style="width:100%">
                <el-option v-for="item in otherComp" :key="item.value" :label=item.value :value=item.value />

              </el-select>


              <template #footer>
                <span class="dialog-footer">
                  <el-button @click="dialogFormVisible = false; component = ''">取消</el-button>
                  <el-button type="primary" @click="dialogFormVisible = false; addOtherComponent();">
                    添加
                  </el-button>
                </span>
              </template>
            </el-dialog>

            <el-radio-group v-model="component">
              <!-- <img src="../assets/component_svg/valve_model.svg"  style="width: 35%"/>
              
              <el-radio label="1" size="large" style="width:25% ;margin-left: 3vmax;">阀门(Valve)</el-radio> -->
              <img src="../assets/component_svg/source tank model.svg" style="width: 35%;" />
              <el-radio label="源罐" size="large" :disabled="if_disable"
                style="width:25%;margin-left: 3vmax;color: white;">源罐(Source
                Tank)</el-radio>
              <img src="../assets/component_svg/icing machine model.svg" style="width: 35%;margin-top: 1vmin;" />
              <el-radio label="冷却" size="large" :disabled="if_disable"
                style="width:25%;margin-left: 3vmax;color: white;">冷却机(Icing
                Machine)</el-radio>
              <img src="../assets/component_svg/FILLING TANK.svg" style="width: 35%;margin-top: 1vmin;" />
              <el-radio label="灌装" size="large" :disabled="if_disable"
                style="width:25% ;margin-left: 3vmax;color: white;">罐装机(Filling
                Machine)</el-radio>
              <img src="../assets/component_svg/tank model.svg" style="width: 35%;margin-top: 1vmin;" />
              <el-radio label="Tank" size="large" :disabled="if_disable"
                style="width:25%;margin-left: 3vmax;color: white;">多功能罐(Tank
                Model)</el-radio>
              <img src="../assets/component_svg/pasteurization.svg" style="width: 35%;margin-top: 1vmin;" />
              <el-radio label="杀菌" size="large" :disabled="if_disable"
                style="width:25%;margin-left: 3vmax;color: white;">巴氏消毒(Pasteurization Machine)</el-radio>
            </el-radio-group>
          </div>
        </el-card>

      </el-aside>

      <el-main width="50vmax" style="margin-top: 3vmin;margin-right: 3vmin;">
        <!-- 图片部分-->

        <!-- <el-card style="margin-top: 4vmin;">
          <div>
            <img :src="url" style=" margin-left: 1vmin; height: 40vmin;" />
          </div>
          <el-progress :percentage="percentage" :color="customColorMethod" :stroke-width="10" />
        </el-card> -->

        <el-card style="margin-top: 4vmin;background-color: #2F5597;;">

          

          <div v-if="!if_show " style="height:43vmin">
            <img :src="url" style="  width:100%" />
            <el-progress :percentage="percentage" :stroke-width="20" striped :striped-flow="status == ''" :duration="1"
              :text-inside="true" :status="status" style="margin-top: 3vmin;" />
          </div>


          <el-carousel v-if="if_show" ref="remarkCaruselUp" autoplay :interval="4000" type="card"
            style=" margin-left: 1vmin; height: 43vmin; ">
            <el-carousel-item v-for="(sr, index) in product_list" :key="index" style="height: 40vmin; ">

              <el-card style=" height: 96% ;width:96%;margin-top: 1vmin;" shadow="always">
                <div v-if="index == 0">
                  <img :src="sr" style=" width: 105%;" />
                </div>

                <div v-if="index != 0" style="position:relative;left:35%;height: 100%;">
                  <img :src="sr" style=" height: 100%;" />
                </div>
              </el-card>

            </el-carousel-item>
          </el-carousel>
        </el-card>

        <!-- <el-progress :percentage="percentage" :color="customColorMethod" :stroke-width="10" style="margin-top: 1vmin;"/> -->




        <!-- 流程部分-->
        <el-card style="margin-top: 3vmin;background-color: #2F5597;;">

          <span style="font-weight:bolder; font-size: larger;color: white;">工艺流程：</span>

          <i class="dotClass" v-if="linestatus == '空闲'"
            style="background-color: springgreen;width:10px;  height:10px;  border-radius: 50%;  display: inline-block ;margin-left: 3vmax;"></i>
          <i class="dotClass" v-if="linestatus == '运行中'"
            style="background-color: orange;width:10px;  height:10px;  border-radius: 50%;  display: inline-block ;margin-left: 3vmax;"></i>
          <i class="dotClass" v-if="linestatus == '已完成'"
            style="background-color: yellow;width:10px;  height:10px;  border-radius: 50%;  display: inline-block ;margin-left: 3vmax;"></i>
          <i class="dotClass" v-if="linestatus == '已暂停' || linestatus == '暂停中'"
            style="background-color: gray;width:10px;  height:10px;  border-radius: 50%;  display: inline-block ;margin-left: 3vmax;"></i>
          <i class="dotClass" v-if="linestatus == '已停止' || linestatus == '停止中'"
            style="background-color: red;width:10px;  height:10px;  border-radius: 50%;  display: inline-block ;margin-left: 3vmax;"></i>
          <span style="font-weight:bolder; font-size: larger;color: rgba(255, 255, 255, 0.693);margin-left: 1vmax;">
            {{ linestatus }}</span>

          <div style="width:45%;display:inline-block;float:right;">
            <el-button style="" type="primary" size="large" @click="operation = 3; send_operation()"> 重启 &nbsp; <el-icon>
                <DeleteFilled />
              </el-icon> </el-button>
            <el-button style="" type="primary" size="large" @click="operation = 2; send_operation()"> 停止 &nbsp; <el-icon>
                <DeleteFilled />
              </el-icon> </el-button>
            <el-button style="" type="primary" size="large" @click="operation = 1; send_operation()"> 暂停 &nbsp; <el-icon>
                <DeleteFilled />
              </el-icon> </el-button>
            <el-button style="" type="primary" size="large" @click="operation=4;clearList();send_operation()"> 清除/复位 &nbsp; <el-icon>
                <DeleteFilled />
              </el-icon> </el-button>
            </div>

          <el-card style="width: 100% ;margin-top: 4vmin;margin-bottom: 4vmin;min-height: 10vmin;">
            <el-steps :active="count">

              <el-step v-for="item in component_list" :key="item.value" :title=item.value :icon=item.svg />
            </el-steps>
          </el-card>
          <div>
            <el-row>
              <div style="width:35%">
                <span style="font-weight:bolder; font-size: larger; display: inline-flex;color: white;">工艺对应产品：</span>
                <span style="color:rgb(7, 228, 248);font-size: large;font-weight: bold;">{{ typevalue }}<el-icon>
                    <IceDrink />
                  </el-icon></span>
              </div>
              <div style="width:50%;color: white;">
                <span style="font-weight:bolder; font-size: larger; display: inline-flex;color: white;">生产数量：</span>
                <el-input-number v-model="num" :precision="0" :step="1000" :max="100000" /> 最小计数单位（瓶、罐、包）
              </div>

              <div style="width:15%;text-align: right;">
                <el-button type="primary" size="large" color="#626aef" @click="send">生产&nbsp;<el-icon>
                    <Shop />
                  </el-icon></el-button>
              </div>

            </el-row>
          </div>

        </el-card>


      </el-main>
    </el-container>
    <!--    <el-footer height="220px" class="footer">-->
    <!--      <Footer />-->
    <!--    </el-footer>-->
  </el-container>
</template>









<style>
.status-point {
  display: inline-block;
  width: 2vmax;
  height: 1vmax;
  border-radius: 50%;
}

.quote-box {
  width: 100%;
  margin: 0px;
  padding: 10px;
  border-left: 4px solid #D4D7DE;
  background-color: #FAFAFA;
}

.quote-author::before {
  content: "——";
}

.quote-text {
  font-size: 20px;
  margin: 5px;
}

.quote-author {
  font-style: italic;
  font-size: 16px;
  color: #909399;
  text-align: right;
}

.footer {
  background-color: #F5F7FA;
}


.card-header {
  display: flex;
  justify-content: space-between;

  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: 480px;
}
</style>
