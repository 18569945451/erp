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
    // 响应成功返回响应数据
    function (response) {
        return response;
    },
    // 响应失败返回失败信息
    async function (error) {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                // 调用刷新 token 的接口
                const refreshResponse = await httpService.post("user/refreshToken", {
                    // 这里可能需要传递一些刷新 token 所需的参数
                });
                const newToken = refreshResponse.data.token;
                window.sessionStorage.setItem("token", newToken);
                originalRequest.headers.Authorization = newToken;
                return httpService(originalRequest);
            } catch (refreshError) {
                // 刷新 token 失败，跳转到登录页
                window.sessionStorage.clear();
                window.location.href = "/login";
                return Promise.reject(refreshError);
            }
        }
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