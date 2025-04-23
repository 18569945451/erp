//引入 axios
import axios from "axios";

let baseUrl = "http://127.0.0.1:8000/"
//创建axios实例
const httpService = axios.create({
    baseURL:baseUrl,
    timeout:3000
    })

//添加请求和响应拦截器
//1.添加请求拦截器
httpService.interceptors.request.use(
    function (config){
    //发送请求的时候获取token
    config.headers.Authorization = window.sessionStorage.getItem("token");
    return config;},
    //发送请求失败返回信息
    function (error){
        return Promise.reject(error);
    }
    );

// 2. 添加响应拦截器
httpService.interceptors.response.use(
    function (response) {
        // 对响应数据做什么
        return response;
    },
    function (error) {
        // 对响应错误做什么
        return Promise.reject(error);
    }
);

/* 网络请求部分 */
/*
 * get 请求
 * url: 请求地址
 * params: 参数
 */

export function get(url,params = {}){
    return new Promise((resolve,reject) => {
        httpService({
            url:url,
            method:'get',
            params:params
        }).then(response =>{
            resolve(response);
        }).catch(error =>{
            reject(error);
        });
    });
}

/*
 * post 请求
 * url: 请求地址
 * params: 参数
 */

export function post(url,params = {}){
    return new Promise((resolve,reject) => {
        httpService({
            url:url,
            method:'post',
            params:params
        }).then(response =>{
            resolve(response);
        }).catch(error =>{
            reject(error);
        });
    });
}

/*
 * delete 请求
 * url: 请求地址
 * params: 参数
 */

export function del(url,params = {}){
    return new Promise((resolve,reject) => {
        httpService({
            url:url,
            method:'delete',
            params:params
        }).then(response =>{
            resolve(response);
        }).catch(error =>{
            reject(error);
        });
    });
}

/*
 * 文件上传
 * url: 请求地址
 * params: 参数
 */

export function fileUpload(url,params = {}){
    return new Promise((resolve,reject) => {
        httpService({
            url:url,
            method:'post',
            params:params,
            headers:{'Content-Type':'multipart/form-data'}
        }).then(response =>{
            resolve(response);
        }).catch(error =>{
            reject(error);
        });
    });
}


export function getServerUrl(){
    return baseUrl;
}

export default {
    get,
    post,
    del,
    fileUpload,
    getServerUrl
}