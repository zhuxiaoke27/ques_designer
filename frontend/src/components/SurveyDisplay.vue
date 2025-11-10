<template>
  <div class="w-full">
    <div class="card p-6">
      <!-- 顶部工具栏 -->
      <div class="flex items-center justify-between mb-6 pb-4 border-b border-gray-200">
        <h2 class="text-2xl font-semibold text-gray-800">问卷预览</h2>
        <div class="flex items-center gap-3">
          <button
            @click="handleEdit"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            编辑问卷
          </button>
          <button
            @click="handleCopy"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            {{ copied ? '已复制' : '复制 JSON' }}
          </button>
          <button
            @click="handleReset"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            重新生成
          </button>
        </div>
      </div>

      <!-- 问卷标题和介绍 -->
      <div class="mb-8">
        <h3 class="text-2xl font-bold text-gray-900 mb-3">
          {{ surveyData.survey_name }}
        </h3>
        <p v-if="surveyData.survey_intro" class="text-gray-600 leading-relaxed">
          {{ surveyData.survey_intro }}
        </p>
      </div>

      <!-- 问卷题目 -->
      <div class="space-y-6">
        <div
          v-for="(question, index) in surveyData.questions"
          :key="index"
          class="pb-6 border-b border-gray-100 last:border-b-0"
        >
          <!-- 题目 -->
          <div class="flex items-start gap-3 mb-4">
            <span class="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-primary-100 text-primary-700 rounded-full font-medium text-sm">
              {{ index + 1 }}
            </span>
            <div class="flex-1">
              <h4 class="text-lg font-medium text-gray-800">
                {{ question.question_text }}
              </h4>
            </div>
          </div>

          <!-- 选项 -->
          <div class="ml-11 space-y-2">
            <div
              v-for="(option, optIndex) in question.options"
              :key="optIndex"
              class="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <span class="flex-shrink-0 w-6 h-6 flex items-center justify-center border-2 border-gray-300 rounded-full text-xs text-gray-500">
                {{ String.fromCharCode(65 + optIndex) }}
              </span>
              <span class="text-gray-700">{{ option }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部统计 -->
      <div class="mt-8 pt-6 border-t border-gray-200">
        <div class="flex items-center justify-between text-sm text-gray-500">
          <span>共 {{ surveyData.questions?.length || 0 }} 道题目</span>
          <span>预计完成时间：{{ estimatedTime }} 分钟</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSurveyStore } from '@/stores/survey'

const props = defineProps({
  surveyData: {
    type: Object,
    required: true
  }
})

const surveyStore = useSurveyStore()
const copied = ref(false)

// 估算完成时间（每题约30秒）
const estimatedTime = computed(() => {
  const questionCount = props.surveyData.questions?.length || 0
  return Math.ceil(questionCount * 0.5)
})

// 编辑问卷
const handleEdit = () => {
  surveyStore.toggleEditMode()
}

// 复制 JSON
const handleCopy = async () => {
  try {
    const jsonStr = JSON.stringify(props.surveyData, null, 2)
    await navigator.clipboard.writeText(jsonStr)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (error) {
    console.error('复制失败:', error)
    alert('复制失败，请手动复制')
  }
}

// 重新生成
const handleReset = async () => {
  if (confirm('确定要重新生成问卷吗？当前内容将会丢失。')) {
    try {
      await surveyStore.regenerate()
    } catch (error) {
      console.error('重新生成失败:', error)
    }
  }
}
</script>
