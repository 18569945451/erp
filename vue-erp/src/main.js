import { createApp } from 'vue'
import svgIcon from '@/icons' // 引入 svgIcon 插件
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'

import 'element-plus/dist/index.css'
// 分页汉化
import zhCn from "element-plus/es/locale/lang/zh-cn";

const app = createApp(App)

svgIcon(app)

app.use(store).use(router).use(ElementPlus, { locale: zhCn }).mount('#app')
