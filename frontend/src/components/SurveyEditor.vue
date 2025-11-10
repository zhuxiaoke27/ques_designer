<template>
  <div class="w-full">
    <div class="card p-6">
      <!-- 顶部工具栏 -->
      <div class="flex items-center justify-between mb-6 pb-4 border-b border-gray-200">
        <h2 class="text-2xl font-semibold text-gray-800">编辑问卷</h2>
        <div class="flex items-center gap-3">
          <button
            @click="handleSave"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            保存修改
          </button>
          <button
            @click="handleCancel"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            取消
          </button>
        </div>
      </div>

      <!-- 问卷基本信息编辑 -->
      <div class="mb-8 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">问卷标题</label>
          <input
            v-model="editData.survey_name"
            type="text"
            class="input-base"
            placeholder="请输入问卷标题"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">问卷介绍</label>
          <textarea
            v-model="editData.survey_intro"
            class="input-base min-h-[80px]"
            placeholder="请输入问卷介绍（可选）"
          ></textarea>
        </div>
      </div>

      <!-- 问题列表编辑 -->
      <div class="space-y-6">
        <div
          v-for="(question, qIndex) in editData.questions"
          :key="qIndex"
          class="pb-6 border-b border-gray-100 last:border-b-0"
        >
          <!-- 问题编辑区 -->
          <div class="mb-4">
            <div class="flex items-start gap-3 mb-3">
              <span class="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-primary-100 text-primary-700 rounded-full font-medium text-sm">
                {{ qIndex + 1 }}
              </span>
              <div class="flex-1">
                <input
                  v-model="question.question_text"
                  type="text"
                  class="input-base"
                  placeholder="请输入问题"
                />
              </div>
              <button
                @click="deleteQuestion(qIndex)"
                class="flex-shrink-0 p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                title="删除题目"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>

          <!-- 选项编辑区 -->
          <div class="ml-11 space-y-2">
            <div
              v-for="(option, oIndex) in question.options"
              :key="oIndex"
              class="flex items-center gap-3"
            >
              <span class="flex-shrink-0 w-6 h-6 flex items-center justify-center border-2 border-gray-300 rounded-full text-xs text-gray-500">
                {{ String.fromCharCode(65 + oIndex) }}
              </span>
              <input
                v-model="question.options[oIndex]"
                type="text"
                class="input-base flex-1"
                placeholder="请输入选项"
              />
              <button
                @click="deleteOption(qIndex, oIndex)"
                class="flex-shrink-0 p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                title="删除选项"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- 添加选项按钮 -->
            <button
              @click="addOption(qIndex)"
              class="ml-9 px-3 py-2 text-sm text-primary-600 hover:bg-primary-50 rounded-lg transition-colors flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              添加选项
            </button>
          </div>
        </div>
      </div>

      <!-- 添加题目按钮 -->
      <div class="mt-6 pt-6 border-t border-gray-200">
        <button
          @click="addQuestion"
          class="w-full py-3 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-primary-500 hover:text-primary-600 hover:bg-primary-50 transition-colors flex items-center justify-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          添加新题目
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useSurveyStore } from '@/stores/survey'

const props = defineProps({
  surveyData: {
    type: Object,
    required: true
  }
})

const surveyStore = useSurveyStore()

// 编辑数据（深拷贝）
const editData = ref(JSON.parse(JSON.stringify(props.surveyData)))

// 监听原始数据变化
watch(() => props.surveyData, (newData) => {
  editData.value = JSON.parse(JSON.stringify(newData))
}, { deep: true })

// 添加题目
const addQuestion = () => {
  editData.value.questions.push({
    question_text: '',
    options: ['', '']
  })
}

// 删除题目
const deleteQuestion = (index) => {
  if (confirm('确定要删除这道题目吗？')) {
    editData.value.questions.splice(index, 1)
  }
}

// 添加选项
const addOption = (questionIndex) => {
  editData.value.questions[questionIndex].options.push('')
}

// 删除选项
const deleteOption = (questionIndex, optionIndex) => {
  const question = editData.value.questions[questionIndex]
  if (question.options.length <= 2) {
    alert('至少需要保留两个选项')
    return
  }
  question.options.splice(optionIndex, 1)
}

// 保存修改
const handleSave = () => {
  // 验证数据
  if (!editData.value.survey_name.trim()) {
    alert('请输入问卷标题')
    return
  }

  if (editData.value.questions.length === 0) {
    alert('至少需要一道题目')
    return
  }

  for (let i = 0; i < editData.value.questions.length; i++) {
    const q = editData.value.questions[i]
    if (!q.question_text.trim()) {
      alert(`第 ${i + 1} 题的问题文本不能为空`)
      return
    }
    if (q.options.some(opt => !opt.trim())) {
      alert(`第 ${i + 1} 题的选项不能为空`)
      return
    }
  }

  // 更新数据
  surveyStore.updateSurvey(editData.value)
  surveyStore.toggleEditMode()
}

// 取消编辑
const handleCancel = () => {
  if (confirm('确定要取消编辑吗？未保存的修改将会丢失。')) {
    surveyStore.toggleEditMode()
  }
}
</script>
