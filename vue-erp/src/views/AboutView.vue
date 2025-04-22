<template>

    <el-button type="primary" @click="handeLogin">测试登录</el-button>
    <el-button type="success"  @click="handeUserList">测试获取用户信息列表</el-button>

</template>

<script setup>
import requestUtil from '@/util/request'
//登录
const handeLogin = async() => {
  let result = await requestUtil.get("user/jwt_test");
  let data = result.data;
  console.log(data)
  if (data.code == 200){
    console.log('成功，token='+token)
    const token = data.token
    window.sessionStorage.setItem("token",token)
  }else {
    console.log('失败')
  }
}
//获取信息列表
const handeUserList = async() => {
  let result = await requestUtil.get("user/test");
  let data = result.data;
  if (data.code == 200){
    console.log('成功，列表信息='+data)
  }else {
    console.log('失败')
  }
}
</script>

