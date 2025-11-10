<template>
  <div class="w-full">
    <div class="card p-8">
      <div class="flex flex-col items-center justify-center space-y-6">
        <!-- 加载动画 -->
        <div class="relative">
          <div class="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin"></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
        </div>

        <!-- 加载文本 -->
        <div class="text-center">
          <h3 class="text-xl font-semibold text-gray-800 mb-2">正在生成问卷...</h3>
          <p class="text-gray-500">AI 正在分析您的需求并生成专业问卷，请稍候</p>
        </div>

        <!-- 进度指示 -->
        <div class="w-full max-w-md">
          <div class="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span>{{ currentStep }}</span>
            <span>{{ Math.round(progress) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div
              class="bg-primary-600 h-2 rounded-full transition-all duration-500"
              :style="{ width: progress + '%' }"
            ></div>
          </div>
        </div>

        <!-- 加载提示 -->
        <div class="text-center space-y-2">
          <p class="text-sm text-gray-500 animate-pulse">{{ loadingTips[currentTipIndex] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const progress = ref(0)
const currentStep = ref('检索历史问卷')
const currentTipIndex = ref(0)

const steps = [
  { text: '检索历史问卷', duration: 2000 },
  { text: '分析需求内容', duration: 3000 },
  { text: 'AI 生成问卷', duration: 5000 },
  { text: '优化问卷结构', duration: 2000 }
]

const loadingTips = [
  '正在从知识库中检索相似问卷...',
  '正在理解您的调研需求...',
  '正在构建专业问卷框架...',
  '正在优化问题和选项...',
  '即将完成，请稍候...'
]

let progressInterval = null
let tipInterval = null
let stepTimeout = null
let currentStepIndex = 0

onMounted(() => {
  // 进度条动画
  progressInterval = setInterval(() => {
    if (progress.value < 95) {
      progress.value += Math.random() * 3
    }
  }, 300)

  // 提示文本轮换
  tipInterval = setInterval(() => {
    currentTipIndex.value = (currentTipIndex.value + 1) % loadingTips.length
  }, 3000)

  // 步骤更新
  const updateStep = () => {
    if (currentStepIndex < steps.length - 1) {
      currentStepIndex++
      currentStep.value = steps[currentStepIndex].text
      stepTimeout = setTimeout(updateStep, steps[currentStepIndex].duration)
    }
  }
  stepTimeout = setTimeout(updateStep, steps[0].duration)
})

onUnmounted(() => {
  if (progressInterval) clearInterval(progressInterval)
  if (tipInterval) clearInterval(tipInterval)
  if (stepTimeout) clearTimeout(stepTimeout)
})
</script>
