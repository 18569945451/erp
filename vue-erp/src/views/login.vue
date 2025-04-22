<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="login-title">用户登录</h1>
      <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="text" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin">登录</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { post } from '@/util/request';
import {ElMessage} from "element-plus";
import router from "@/router";

// 初始化表单引用
const loginFormRef = ref(null);
// 初始化表单数据
const loginForm = ref({
  username: '',
  password: ''
});
// 初始化表单验证规则
const loginRules = ref({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
});

// 登录
const handleLogin = async () => {
  // 先验证表单
  loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        // 发送 POST 请求并传递表单数据
        let result = await post("user/login", loginForm.value);
        let data = result.data;
        if (data.code === 200) {
          const token = data.token;
          console.log('成功，token=' + token);
          window.sessionStorage.setItem("token", token);
          const currentUser = data.user
          currentUser.roles=data.roles  //添加用户角色到currentUser
          window.sessionStorage.setItem("currentUser", JSON.stringify(currentUser));
          window.sessionStorage.setItem("menuList", JSON.stringify(data.menuList));
          ElMessage.success(data.info)
          router.replace("/")
        } else {
          ElMessage.error(data.info)
        }
      } catch (error) {
        ElMessage.error(error)
      }
    }
  });
};

// 重置表单函数
const resetForm = () => {
  loginFormRef.value.resetFields();
};
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.login-box {
  width: 360px;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}
</style>