<template>
  <div class="w-full">
    <!-- 输入区域 -->
    <div class="card p-6">
      <h2 class="text-2xl font-semibold mb-4 text-gray-800">问卷需求</h2>

      <textarea
        v-model="requirement"
        @keydown.ctrl.enter="handleSubmit"
        @keydown.meta.enter="handleSubmit"
        placeholder="请详细描述您的问卷调研需求、背景及目的...&#10;&#10;例如：我想针对统一版客户端做一个满意度的调研"
        class="input-base min-h-[200px] resize-y"
        :disabled="loading"
      ></textarea>

      <div class="mt-4 flex items-center justify-between">
        <p class="text-sm text-gray-500">
          提示：按 Ctrl+Enter 或 ⌘+Enter 快速提交
        </p>
        <button
          @click="handleSubmit"
          :disabled="!requirement.trim() || loading"
          class="btn-primary"
        >
          {{ loading ? '生成中...' : '生成问卷' }}
        </button>
      </div>
    </div>

    <!-- 示例需求 -->
    <div class="mt-6">
      <h3 class="text-sm font-medium text-gray-700 mb-3">示例需求</h3>
      <div class="grid grid-cols-1 gap-3">
        <div
          v-for="(example, index) in examples"
          :key="index"
          @click="selectExample(example)"
          class="card p-4 cursor-pointer hover:border-primary-500 hover:shadow-md transition-all duration-200"
        >
          <p class="text-sm text-gray-700">{{ example }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useSurveyStore } from '@/stores/survey'

const surveyStore = useSurveyStore()
const requirement = ref('')

// 是否正在加载
const loading = ref(false)

// 示例需求
const examples = [
  '我想针对统一版客户端做一个满意度的调研',
  '需要设计一份员工满意度调查问卷，用于评估公司的工作环境、薪酬福利和管理制度',
  '设计一份市场调研问卷，了解用户对新产品的接受度和改进建议',
  '想了解大学生的消费习惯，调研当代大学生的消费观念和消费结构'
]

// 选择示例
const selectExample = (example) => {
  requirement.value = example
}

// 提交生成
const handleSubmit = async () => {
  if (!requirement.value.trim() || loading.value) return

  loading.value = true
  try {
    await surveyStore.generate(requirement.value)
  } catch (error) {
    console.error('生成失败:', error)
  } finally {
    loading.value = false
  }
}
</script>
