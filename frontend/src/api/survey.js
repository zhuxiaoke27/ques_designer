/**
 * 问卷 API 接口封装
 */
import axios from 'axios'

// 获取 API 基础 URL（支持环境变量配置）
const getBaseURL = () => {
  // 生产环境使用环境变量或者相对路径
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  // 开发环境使用代理
  return '/api'
}

// 创建 axios 实例
const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 60000, // 60秒超时（AI 生成可能需要较长时间）
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    // 错误处理
    const errorMessage = error.response?.data?.message || error.message || '请求失败'
    return Promise.reject(new Error(errorMessage))
  }
)

/**
 * 生成问卷
 * @param {string} requirement - 用户需求描述
 * @returns {Promise} 问卷数据
 */
export const generateSurvey = async (requirement) => {
  try {
    const response = await api.post('/generate', { requirement })
    return response
  } catch (error) {
    throw error
  }
}

/**
 * 健康检查
 * @returns {Promise}
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health')
    return response
  } catch (error) {
    throw error
  }
}

export default {
  generateSurvey,
  healthCheck
}
