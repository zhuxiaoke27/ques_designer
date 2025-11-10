/**
 * 问卷状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { generateSurvey } from '@/api/survey'

export const useSurveyStore = defineStore('survey', () => {
  // 状态
  const loading = ref(false)
  const error = ref(null)
  const surveyData = ref(null)
  const isEditing = ref(false)
  const lastRequirement = ref('')  // 保存最后一次的需求

  // Actions
  const generate = async (requirement) => {
    loading.value = true
    error.value = null
    surveyData.value = null
    lastRequirement.value = requirement  // 保存需求用于重新生成

    try {
      const response = await generateSurvey(requirement)

      if (response.status === 'success') {
        surveyData.value = response.data
        return response.data
      } else {
        throw new Error(response.message || '生成失败')
      }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 重新生成（使用相同的需求）
  const regenerate = async () => {
    if (!lastRequirement.value) {
      throw new Error('没有可用的需求描述')
    }
    return await generate(lastRequirement.value)
  }

  const updateSurvey = (newData) => {
    surveyData.value = newData
  }

  const toggleEditMode = () => {
    isEditing.value = !isEditing.value
  }

  const reset = () => {
    loading.value = false
    error.value = null
    surveyData.value = null
    isEditing.value = false
    lastRequirement.value = ''
  }

  return {
    // State
    loading,
    error,
    surveyData,
    isEditing,
    lastRequirement,
    // Actions
    generate,
    regenerate,
    updateSurvey,
    toggleEditMode,
    reset
  }
})
