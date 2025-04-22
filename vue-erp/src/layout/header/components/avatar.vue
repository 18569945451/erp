

<template>
  <el-avatar shape="square" :size="40" :src="squareUrl" />
    <div class="flex flex-wrap items-center">
    <el-dropdown>
      <el-button type="primary">
        &nbsp;&nbsp;{{currentUser.username}}<el-icon class="el-icon--right"><arrow-down /></el-icon>
      </el-button>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item>
              <router-link :to="{name:'个人中心'}">个人中心</router-link>
          </el-dropdown-item>
          <el-dropdown-item @click="logout">安全退出</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>

</template>

<script setup>
import { ArrowDown } from '@element-plus/icons-vue'
import requestUtil,{getServerUrl} from "@/util/request";
import router  from "@/router";
import store from "@/store";
//头像
const currentUser = JSON.parse(sessionStorage.getItem("currentUser"))
const squareUrl = getServerUrl()+"media/userAvatar/"+currentUser.avatar
//注销
const logout=()=>{
  window.sessionStorage.clear()
  store.commit('RESET_TAB')
  router.replace('/login')
}
</script>

<style lang="scss" scoped>
.el-dropdown-link{
cursor: pointer;
color: var(--el-color-primary);
display: flex;
align-items: center;}
</style>