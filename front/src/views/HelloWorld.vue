<script setup>
import { useRouter } from 'vue-router'
import Header from '@/components/StartHeader.vue'
import SelectType from '@/components/SelectType.vue'
import SelectComp from '@/components/SelectComp.vue'
// import Footer from '@/components/StartFooter.vue'

const router = useRouter()

function jump_to_login() {
  router.push('/start')
}
</script>

<template>
  <el-container style="width: 100%; min-height:100%; min-width: 95vmax;">
    <el-header style="margin: 0; padding: 0 ;">
      <Header />
    </el-header>
    <el-container>
    <el-aside width="35vmax" style="margin-top: 7vmin;margin-left: 2vmax;">
       <SelectType style="margin-top: 2vmin;"/>
       <SelectComp style="margin-top: 2vmin;"/>
    </el-aside>
    <el-main style="margin: 3vmin;">
      
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
</style>
