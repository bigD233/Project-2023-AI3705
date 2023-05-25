<template>
    <el-card class="box-card">
   
      <div class="card-header">
        <div >选择饮料种类</div>
        
        <el-select v-model="value" filterable placeholder="选择要生产的饮料" size="large">
          
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
      </div>
  </el-card>
</template>



<script  setup>
import { ref } from 'vue'

const value = ref('')
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
</script>



<style>
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