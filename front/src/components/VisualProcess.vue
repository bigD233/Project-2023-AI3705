<template>
    <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span>选择饮料种类</span>
        <el-button class="button" text>按钮</el-button>
      </div>
    </template>
    <div v-for="o in 4" :key="o" class="text item">{{ '饮料 ' + o }}</div>
  </el-card>
</template>

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