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
import img0 from '../assets/logo.png'
import { markRaw, ref } from 'vue'
// import SelectComp from '@/components/SelectComp.vue'
// import Footer from '@/components/StartFooter.vue'


const router = useRouter()

function jump_to_login() {
  router.push('/start')
}

var timer  //计时器
var url = img0
const num = ref(1000)
const component_list = ref([])
const component = ref('')    // 工艺名称
const typevalue = ref('')   // 饮料种类名称
const percentage = ref(0)  // 进度条百分比
const if_increase = ref(true)  //是否继续增长
const is_disable = ref(false)

const options = [
  {
    value: '饮用天然矿泉水',
    label: '饮用天然矿泉水',
    process: ['源罐', '粗滤', '精滤', '杀菌', '灌装'],
    src: img1
  },
  {
    value: '碳酸饮料',
    label: '碳酸饮料',
    process: ['源罐', '调配', '制冷', '碳酸化', '杀菌', '灌装'],
    src: img2
  },
  {
    value: '茶饮料',
    label: '茶饮料',
    process: ['源罐', '调配', '过滤', '杀菌', '灌装'],
    src: img3
  },
  {
    value: '果蔬饮料',
    label: '果蔬饮料',
    process: ['源罐', '稀释', '调配', '杀菌', '灌装'],
    src: img4
  },
  {
    value: '含乳饮料',
    label: '含乳饮料',
    process: ['源罐', '加热', '调配', '杀菌', '灌装'],
    src: img5
  },
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
    if (if_increase){
      timer = setInterval(increase, 1500);   
      if_increase.value = false
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
  var step = 100/component_list.value.length
  if (Math.abs(percentage.value - 100)>1) {
    if (Number((percentage.value + step).toFixed(1)) > 100){
      percentage.value = 100
      if_increase.value = false
    }
    else {
      percentage.value = Number((percentage.value +step).toFixed(1));
    }
  }
}




function judgeSelect() {  //选择饮料
  if (typevalue.value != '') {
    is_disable.value = true;
    component_list.value=[];
  }

  for (const item of options) {
    console.log(item);
    if (item.value == typevalue.value) {  //找到配方
      
      url = item.src
      console.log(item.src);
      for (var i = 0; i < item.process.length; i++) {
        addComponent(item.process[i],2);  //添加配方
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
    addComponent(component.value,1);
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

function checkCorrection(){
  for(const item of options){
    if(component_list.value.length==item.process.length){
      var flag=true;
      for(var i=0;i<item.process.length;i++){
        if (component_list.value[i].value!=item.process[i]){
          flag=false;
        }
      }
      if(flag){
        typevalue.value=item.value;
        url = item.src
        console.log(item.src)
      }
    }
  }
}


function addComponent(component, num) {


  switch (component) {
    case '源罐':
      component_list.value.push({ value: "源罐", svg: markRaw(Files)});
      break;
    case '冷却':
      component_list.value.push({ value: "冷却", svg: markRaw(IceCreamRound) })
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
      if (num ==2){
        component_list.value.push({ value: component, svg: markRaw(Operation) })
      }

  }



}

function clearList() {
  typevalue.value = '';
  component_list.value = [];
  component.value = '';
  is_disable.value = false;
  percentage.value = 0;
  if_increase.value = true;
  clearInterval(timer);
  url = img0;
}

</script>

<template>
  <el-container style="width: 100%; min-height:100%; min-width: 100vmin;">
    <el-header style="margin: 0; padding: 0 ;">
      <Header />
    </el-header>
    <el-container>

      <el-aside width="30vmax" style="margin-top: 7vmin;margin-left: 2vmax;">

        <!-- 选择种类部分 -->
        <el-card class="box-card" style="margin-top: 2vmin">
          <div class="card-header">
            <div>选择饮料种类</div>

            <el-select v-model="typevalue" filterable placeholder="选择要生产的饮料" size="large" @change="judgeSelect">

              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </div>
        </el-card>


        <!-- 选择工艺部分 -->
        <el-card class="box-card" style="margin-top: 2vmin;">
          <template #header>
            <div class="card-header">
              <p>自选工艺类型</p>
              <el-button type="info" plain :icon="CirclePlus" :disabled="is_disable" @click="addComponent1">添加</el-button>
            </div>
          </template>
          <div class="mb-2 flex items-center text-sm">

            <el-dialog v-model="dialogFormVisible" title="输入具体工艺名称" draggable style="width:22vmax" align-center>

              <el-select v-model="component" placeholder="输入多功能罐对应的工艺名称" size="large" style="width:100%">
                <el-option v-for="item in otherComp" :key="item.value" :label=item.value :value=item.value />

              </el-select>


              <template #footer>
                <span class="dialog-footer">
                  <el-button @click="dialogFormVisible = false; component = ''">取消</el-button>
                  <el-button type="primary" @click="dialogFormVisible = false; addOtherComponent()">
                    添加
                  </el-button>
                </span>
              </template>
            </el-dialog>

            <el-radio-group v-model="component">
              <!-- <img src="../assets/component_svg/valve_model.svg"  style="width: 35%"/>
              
              <el-radio label="1" size="large" style="width:25% ;margin-left: 3vmax;">阀门(Valve)</el-radio> -->
              <img src="../assets/component_svg/source tank model.svg" style="width: 35%" />
              <el-radio label="源罐" size="large" :disabled="is_disable" style="width:25%;margin-left: 3vmax;">源罐(Source
                Tank)</el-radio>
              <img src="../assets/component_svg/icing machine model.svg" style="width: 35%" />
              <el-radio label="冷却" size="large" :disabled="is_disable" style="width:25%;margin-left: 3vmax;">冷却机(Icing
                Machine)</el-radio>
              <img src="../assets/component_svg/FILLING TANK.svg" style="width: 35%" />
              <el-radio label="灌装" size="large" :disabled="is_disable" style="width:25% ;margin-left: 3vmax;">罐装机(Filling
                Machine)</el-radio>
              <img src="../assets/component_svg/tank model.svg" style="width: 35%" />
              <el-radio label="Tank" size="large" :disabled="is_disable" style="width:25%;margin-left: 3vmax;">多功能罐(Tank
                Model)</el-radio>
              <img src="../assets/component_svg/pasteurization.svg" style="width: 35%" />
              <el-radio label="杀菌" size="large" :disabled="is_disable"
                style="width:25%;margin-left: 3vmax;">巴氏消毒(Pasteurization Machine)</el-radio>
            </el-radio-group>
          </div>
        </el-card>

      </el-aside>

      <el-main width="50vmax"  style="margin: 3vmin;">
        <el-card style="margin-top: 4vmin;">

          <span style="font-weight:bolder; font-size: larger;">工艺流程：</span>
          <el-button style="float:right" type="primary" @click="clearList"> 清除 &nbsp; <el-icon>
              <DeleteFilled />
            </el-icon> </el-button>
          <el-card style="width: 100% ;margin-top: 2vmin;margin-bottom: 2vmin;min-height: 10vmin;">
            <el-steps :active="percentage/20">

              <el-step v-for="item in component_list" :key="item.value" :title=item.value :icon=item.svg />
            </el-steps>
          </el-card>
          <div>
            <el-row>
              <div style="width:30%">
                <span style="font-weight:bolder; font-size: larger; display: inline-flex;">工艺对应产品：</span>
                <span style="color:blue;font-size: large;font-weight: bold;">{{ typevalue }}<el-icon>
                    <IceDrink />
                  </el-icon></span>
              </div>
              <div style="width:50%">
                <span style="font-weight:bolder; font-size: larger; display: inline-flex;">生产数量：</span>
                <el-input-number v-model="num" :precision="0" :step="1000" :max="100000" /> 最小计数单位（瓶、罐、包）
              </div>

              <div style="width:20%;text-align: right;">
                <el-button type="primary" plain size="large" @click="percentage_increase">生产&nbsp;<el-icon>
                    <Shop />
                  </el-icon></el-button>
              </div>

            </el-row>
          </div>

        </el-card>
        <el-card style="margin-top: 4vmin;">
          <div>
            <img :src="url" style=" margin-left: 1vmin; height: 40vmin;" />
          </div>
          <el-progress :percentage="percentage" :color="customColorMethod" :stroke-width="10" />
        </el-card>

      </el-main>
    </el-container>
    <!--    <el-footer height="220px" class="footer">-->
    <!--      <Footer />-->
    <!--    </el-footer>-->
  </el-container>
</template>









<style>
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
