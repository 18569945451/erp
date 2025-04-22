<template>
  <router-view/>
</template>

<script setup>
import {watch} from "vue";
import  {useRoute} from "vue-router";
import store from "@/store";
const route = useRoute()

watch(route,(to,from)=>{
  if (to.name =='个人中心'){
    let obj={
      name:to.name,
      path:to.path
    }
    store.commit('ADD_TABS',obj)
  }
},{deep:true,immediate:true})
</script>


<style>
</style>
