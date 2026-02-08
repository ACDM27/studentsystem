<template>
  <n-modal :show="props.show" @update:show="emit('update:show', $event)" preset="card" title="作业详情" style="width: 700px">
    <n-descriptions bordered>
      <n-descriptions-item label="课程名称">
        {{ assignment?.courseName }}
      </n-descriptions-item>
      <n-descriptions-item label="指导老师">
        {{ assignment?.teacher }}
      </n-descriptions-item>
      <n-descriptions-item label="状态">
        <n-tag :type="getStatusType(assignment?.status)">
          {{ assignment?.status }}
        </n-tag>
      </n-descriptions-item>
      <n-descriptions-item label="发布时间">
        {{ formatDate(assignment?.publishDate) }}
      </n-descriptions-item>
      <n-descriptions-item label="截止时间">
        {{ assignment?.deadline }}
      </n-descriptions-item>
      <n-descriptions-item label="可提交次数">
        {{ assignment?.maxSubmissions }}
      </n-descriptions-item>
      <n-descriptions-item label="作业要求" :span="3">
        <div style="white-space: pre-wrap;">{{ assignment?.requirements }}</div>
      </n-descriptions-item>
    </n-descriptions>

    <template #footer>
      <n-space justify="end">
        <n-button @click="emit('update:show', false)">关闭</n-button>
        <n-button 
          type="primary" 
          @click="openSubmitModal"
          :disabled="assignment?.status === '已截止'"
        >
          {{ assignment?.status === '已截止' ? '已截止' : '提交作业' }}
        </n-button>
      </n-space>
    </template>
  </n-modal>

  <!-- 提交作业弹窗 -->
  <n-modal v-model:show="submitShow" preset="card" title="提交作业" style="width: 600px">
    <n-form
      ref="submitFormRef"
      :model="submitForm"
      :rules="submitRules"
      label-placement="left"
      label-width="100px"
    >
      <n-form-item label="作业标题" path="title">
        <n-input v-model:value="submitForm.title" placeholder="请输入作业标题" />
      </n-form-item>

      <n-form-item label="作业说明" path="content">
        <n-input
          v-model:value="submitForm.content"
          type="textarea"
          placeholder="请输入作业说明"
          :autosize="{ minRows: 3, maxRows: 6 }"
        />
      </n-form-item>

      <n-form-item label="作业文件" path="file">
        <n-upload
          v-model:file-list="submitForm.file_list"
          :max="5"
          multiple
          :accept="acceptFileTypes"
          :max-size="10 * 1024 * 1024"
        >
          <n-upload-dragger>
            <div style="padding: 20px 0">
              <n-space vertical>
                <n-icon size="48" :depth="3">
                  <FileUpload :size="24" />
                </n-icon>
                <n-text style="font-size: 16px">
                  点击或者拖动文件到该区域来上传
                </n-text>
                <n-text depth="3" style="font-size: 14px">
                  支持PDF、Word、ZIP等文档格式，单个文件最大10MB，最多可上传5个文件
                </n-text>
              </n-space>
            </div>
          </n-upload-dragger>
        </n-upload>
      </n-form-item>
    </n-form>

    <template #footer>
      <n-space justify="end">
        <n-button @click="submitShow = false">取消</n-button>
        <n-button type="primary" @click="submitAssignment" :loading="submitting">
          提交作业
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, reactive, defineProps, defineEmits } from 'vue'
import { useMessage } from 'naive-ui'
import { IconFileUpload as FileUpload } from '@tabler/icons-vue'
import { postAssignmentsSubmit } from '../../../apis'
import type { IPostAssignmentsSubmitReq } from '../../../types/api'

// 消息提示
const message = useMessage()

// 定义组件属性
const props = defineProps<{
  show: boolean
  assignment: {
    id: number
    courseName: string
    teacher: string
    requirements: string
    publishDate: string
    deadline: string
    maxSubmissions: string
    status: string
  } | null
}>()

// 定义组件事件
const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'refresh'): void
}>()

// 提交弹窗状态
const submitShow = ref(false)
const submitting = ref(false)
const submitFormRef = ref<any>(null)

// 提交表单数据
const submitForm = reactive({
  title: '',
  content: '',
  file_list: [] as any[]
})

// 表单验证规则
const submitRules = {
  title: {
    required: true,
    message: '请输入作业标题',
    trigger: 'blur'
  },
  file_list: {
    required: true,
    type: 'array',
    min: 1,
    message: '请上传作业文件',
    trigger: 'change'
  }
}

// 允许的文件类型
const acceptFileTypes = '.pdf,.doc,.docx,.zip,.rar,.7z'

// 打开提交弹窗
const openSubmitModal = () => {
  // 检查作业状态
  if (!props.assignment) {
    message.error('作业信息不完整，无法提交')
    return
  }
  
  // 如果作业已截止，显示提示信息并阻止提交
  if (props.assignment.status === '已截止') {
    message.warning('该作业已截止，无法提交')
    return
  }
  
  // 预填写标题
  submitForm.title = `${props.assignment.courseName}作业提交`
  submitShow.value = true
}

// 提交作业
const submitAssignment = async () => {
  if (!submitFormRef.value) return
  if (!props.assignment) {
    message.error('作业信息不完整，无法提交')
    return
  }
  
  try {
    await submitFormRef.value.validate()
    submitting.value = true
    
    // 构建提交数据
    const formData = new FormData()
    formData.append('assignmentId', String(props.assignment.id))
    formData.append('content', submitForm.content)
    
    // 添加文件
    if (submitForm.file_list.length > 0) {
      submitForm.file_list.forEach((fileInfo: any, index: number) => {
        if (fileInfo && fileInfo.file) {
          formData.append('attachments', fileInfo.file)
        }
      })
    }
    
    // 调用API提交
    // 注释掉实际API调用，使用模拟成功响应
    // await postAssignmentsSubmit(formData)
    
    // 模拟提交成功
    setTimeout(() => {
      submitting.value = false
      message.success('作业提交成功')
      submitShow.value = false
      resetSubmitForm()
      emit('refresh') // 通知父组件刷新数据
    }, 1000)
  } catch (error) {
    console.error('提交作业失败:', error)
    submitting.value = false
    message.error('提交作业失败，请重试')
  }
}

// 重置提交表单
const resetSubmitForm = () => {
  if (submitFormRef.value) {
    submitFormRef.value.restoreValidation()
  }
  Object.assign(submitForm, {
    title: '',
    content: '',
    file_list: []
  })
}

// 获取状态对应的标签类型
const getStatusType = (status?: string) => {
  const statusMap: Record<string, string> = {
    '已完成': 'success',
    '待提交': 'warning',
    '未开始': 'default',
    '已截止': 'error'
  }
  return statusMap[status || ''] || 'default'
}

// 格式化日期
const formatDate = (dateString?: string): string => {
  if (!dateString || dateString === '未设置') return '未设置'
  
  try {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    
    return `${year}年${month.toString().padStart(2, '0')}月${day.toString().padStart(2, '0')}日`
  } catch (error) {
    console.error('日期格式化错误:', error)
    return dateString
  }
}
</script>

<style scoped>
/* 可以添加自定义样式 */
</style>