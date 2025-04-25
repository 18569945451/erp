<template>
  <div id="app">
    <h1>数据拉取页面</h1>
    <div>
      <label for="pageSize">分页数：</label>
      <input type="number" id="pageSize" v-model="pageSize" placeholder="请输入分页数" />
    </div>
    <div>
      <label for="startDate">开始日期：</label>
      <input type="date" id="startDate" v-model="startDate" />
    </div>
    <div>
      <label for="endDate">结束日期：</label>
      <input type="date" id="endDate" v-model="endDate" />
    </div>
    <div>
      <label for="dataSource">数据源：</label>
      <select id="dataSource" v-model="dataSource">
        <option v-for="source in dataSources" :key="source" :value="source">
          {{ source }}
        </option>
      </select>
    </div>
    <button @click="fetchData">拉取数据</button>
    <div v-if="loading">加载中...</div>
    <div v-if="error">{{ error }}</div>
    <pre v-if="data">{{ JSON.stringify(data, null, 2) }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import requerUntil from '@/util/request'

// 定义响应式变量
const pageSize = ref(10);
const startDate = ref('');
const endDate = ref('');
const dataSource = ref('');
const dataSources = ref(['销售订单历史', '运输记录']);
const data = ref(null);
const loading = ref(false);
const error = ref(null);

// 模拟拉取数据的函数
const fetchData = async () => {
  loading.value = true;
  error.value = null;
  data.value = null;

  try {
    // 这里只是模拟数据请求，实际应用中需要替换为真实的 API 地址
    const response = await requerUntil.get('datas/pull');
    if (response.status !== 200) {
      throw new Error('网络请求失败');
    }
    data.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
}
div {
  margin: 10px 0;
}
label {
  display: inline-block;
  width: 100px;
}
input,
select {
  padding: 5px;
}
button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>