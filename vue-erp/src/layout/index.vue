<template>
  <div class="app-container">
    <!-- 侧边栏 -->
    <MenuComponent />
    <!-- 主内容区 -->
    <el-container class="main-container">
      <el-header><HeaderComponent /></el-header>
      <el-main><TabsComponent /><router-view />></el-main>
      <el-footer><FooterComponent /></el-footer>
    </el-container>
  </div>
</template>

<script setup>
import MenuComponent from '@/layout/menu/index.vue'
import HeaderComponent from '@/layout/header/index.vue'
import TabsComponent from '@/layout/tabs/index.vue'
import FooterComponent from '@/layout/footer/index.vue'
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100vh;
}

.main-container {
  flex: 1;
  padding: 10px;
  box-sizing: border-box;
}
</style>