<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-3">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h1 class="text-xl font-bold text-gray-900">问卷设计助手</h1>
          </div>
          <div class="text-sm text-gray-500">
            基于 AI 的智能问卷生成工具
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="h-[calc(100vh-64px)] overflow-hidden">
      <!-- 错误提示（固定在顶部） -->
      <div v-if="surveyStore.error" class="bg-red-50 border-b border-red-200 p-4">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-start gap-3">
          <svg class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div class="flex-1">
            <h3 class="text-sm font-medium text-red-800">生成失败</h3>
            <p class="text-sm text-red-700 mt-1">{{ surveyStore.error }}</p>
          </div>
          <button
            @click="surveyStore.error = null"
            class="flex-shrink-0 text-red-500 hover:text-red-700"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- 左右分栏布局 -->
      <div class="h-full grid grid-cols-1 lg:grid-cols-2 gap-0">
        <!-- 左侧：问卷需求输入 -->
        <div class="flex flex-col border-r border-gray-200 bg-white overflow-y-auto">
          <div class="p-6">
            <InputPanel v-if="!surveyStore.isEditing" />
          </div>
        </div>

        <!-- 右侧：问卷预览/编辑/加载状态 -->
        <div class="flex flex-col bg-gray-50 overflow-y-auto">
          <div class="p-6">
            <!-- 加载状态 -->
            <LoadingState v-if="surveyStore.loading" />

            <!-- 问卷展示 - 非编辑模式 -->
            <SurveyDisplay
              v-else-if="surveyStore.surveyData && !surveyStore.isEditing"
              :survey-data="surveyStore.surveyData"
            />

            <!-- 问卷编辑器 - 编辑模式 -->
            <SurveyEditor
              v-else-if="surveyStore.surveyData && surveyStore.isEditing"
              :survey-data="surveyStore.surveyData"
            />

            <!-- 空状态提示 -->
            <div
              v-else-if="!surveyStore.loading && !surveyStore.surveyData"
              class="flex flex-col items-center justify-center h-full min-h-[400px] text-center"
            >
              <svg class="w-24 h-24 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 class="mt-4 text-lg font-medium text-gray-600">
                开始设计您的专业问卷
              </h3>
              <p class="mt-2 text-sm text-gray-500 max-w-md">
                在左侧输入您的调研需求，AI 将为您生成符合专业规范的问卷设计
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useSurveyStore } from '@/stores/survey'
import InputPanel from '@/components/InputPanel.vue'
import LoadingState from '@/components/LoadingState.vue'
import SurveyDisplay from '@/components/SurveyDisplay.vue'
import SurveyEditor from '@/components/SurveyEditor.vue'

const surveyStore = useSurveyStore()
</script>
