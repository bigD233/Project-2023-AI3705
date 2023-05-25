<script setup>
import { useRouter } from 'vue-router'
import Header from '@/components/StartHeader.vue'
import {
  CirclePlus, Files, Select, CloseBold, IceDrink,
  IceCreamRound, Mug, Operation, Shop, DeleteFilled
} from '@element-plus/icons-vue'
// import SelectComp from '@/components/SelectComp.vue'
// import Footer from '@/components/StartFooter.vue'

const router = useRouter()

function jump_to_login() {
  router.push('/start')
}

import { ref } from 'vue'

const num = ref(1000)
const component_list = ref([])
const component = ref('')    // 工艺名称
const typevalue = ref('')   // 饮料种类名称

const is_disable = ref(false)

const options = [
  {
    value: '饮用天然矿泉水',
    label: '饮用天然矿泉水',
  },
  {
    value: '碳酸饮料',
    label: '碳酸饮料',
  },
  {
    value: '茶饮料',
    label: '茶饮料',
  },
  {
    value: '果蔬饮料',
    label: '果蔬饮料',
  },
  {
    value: '含乳饮料',
    label: '含乳饮料',
  },
]

const otherComp = [
  {
    value: '调配（混合）'
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

function judgeSelect() {
  if (typevalue.value != '') {
    is_disable.value = true;
  }
}


function addOtherComponent() {
  if (component.value != '') {
    component_list.value.push({ value: component.value, svg: Operation })
  }
}


function addComponent() {

  if (component.value != '') {
    switch (component.value) {
      case 'Source':
        component_list.value.push({ value: "源罐", svg: Files });
        break;
      case 'Icing':
        component_list.value.push({ value: "冷却机", svg: IceCreamRound })
        break;
      case 'Filling':
        component_list.value.push({ value: "罐装机", svg: Mug })
        break;
      default:
        dialogFormVisible.value = true;
    }

    component.value = '';
    console.log(component_list.value)
  }
  else {
    ElMessage({
      message: '您未选择任何一项加工工艺！',
      type: 'warning',
    })
  }
}

function clearList() {
  typevalue.value = '';
  component_list.value = [];
  component.value = '';
  is_disable.value = false;
}

</script>

<template>
  <el-container style="width: 100%; min-height:100%; min-width: 100vmax;">
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
              <el-button type="info" plain :icon="CirclePlus" :disabled="is_disable" @click="addComponent">添加</el-button>
            </div>
          </template>
          <div class="mb-2 flex items-center text-sm">

            <el-dialog v-model="dialogFormVisible" title="输入具体工艺名称" draggable style="width:22vmax" align-center>

              <el-select v-model="component" placeholder="输入多功能罐对应的工艺名称" size="large" style="width:100%">
                <el-option v-for="item in otherComp" :label=item.value :value=item.value />

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
              <el-radio label="Source" size="large" :disabled="is_disable" style="width:25%;margin-left: 3vmax;">源罐(Source
                Tank)</el-radio>
              <img src="../assets/component_svg/icing machine model.svg" style="width: 35%" />
              <el-radio label="Icing" size="large" :disabled="is_disable" style="width:25%;margin-left: 3vmax;">冷却机(Icing
                Machine)</el-radio>
              <img src="../assets/component_svg/FILLING TANK.svg" style="width: 35%" />
              <el-radio label="Filling" size="large" :disabled="is_disable"
                style="width:25% ;margin-left: 3vmax;">罐装机(Filling Machine)</el-radio>
              <img src="../assets/component_svg/tank model.svg" style="width: 35%" />
              <el-radio label="Tank" size="large" :disabled="is_disable" style="width:25%;margin-left: 3vmax;">多功能罐(Tank
                Model)</el-radio>
            </el-radio-group>
          </div>
        </el-card>

      </el-aside>

      <el-main style="margin: 3vmin;">
        <el-card style="margin-top: 4vmin;">

          <span style="font-weight:bolder; font-size: larger;">工艺流程：</span>
          <el-button style="float:right" type="primary" @click="clearList"> 清除 &nbsp; <el-icon>
              <DeleteFilled />
            </el-icon> </el-button>
          <el-card style="width: 100% ;margin-top: 2vmin;margin-bottom: 2vmin;min-height: 10vmin;">
            <el-steps :active="1">

              <el-step v-for="item in component_list" :title=item.value :icon=item.svg />
            </el-steps>
          </el-card>
          <div>
            <el-row>
              <div style="width:30%">
                <span style="font-weight:bolder; font-size: larger; display: inline-flex;">工艺对应产品：</span>
                <span style="color:red;font-size: large;font-weight: bold;">{{ typevalue }}<el-icon>
                    <IceDrink />
                  </el-icon></span>
              </div>
              <div style="width:50%">
                <span style="font-weight:bolder; font-size: larger; display: inline-flex;">生产数量：</span>
                <el-input-number v-model="num" :precision="0" :step="1000" :max="100000" /> 最小计数单位（瓶、罐、包）
              </div>

              <div style="width:20%;text-align: right;">
                <el-button type="primary" plain size="large">生产&nbsp;<el-icon>
                    <Shop />
                  </el-icon></el-button>
              </div>

            </el-row>
          </div>

        </el-card>
        <img src="../assets/logo.png" style="width: 400px;" />

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
