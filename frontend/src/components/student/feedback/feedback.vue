<template>
  <div class="feedback-container">
    <!-- 页面标题 -->
    <div class="page_header">
      <h1>反馈与申诉</h1>
      <p>向学校提交您的意见建议或申诉问题</p>
    </div>

    <!-- 反馈内容区域 -->
    <div class="feedback-header">
      
      <n-tabs type="line" v-model:value="active_tab">
        <n-tab-pane name="submit" tab="提交反馈">
          <n-card>
            <!-- 中部表单区域 -->
            <n-form
              ref="form_ref"
              :model="form_data"
              :rules="form_rules"
              label-placement="left"
              label-width="100%"
              require-mark-placement="right-hanging"
            >
              <!-- 反馈类型选择 -->
              <n-form-item label="反馈类型" path="feed_type" required>
                <n-select
                  v-model:value="form_data.feed_type"
                  :options="feed_types"
                  placeholder="请选择反馈类型"
                />
              </n-form-item>
              
              <!-- 提交方式 -->
              <n-form-item label="提交方式" required>
                <n-radio-group v-model:value="form_data.is_anonym" @update:value="handleAnonymChange">
                  <n-space>
                    <n-radio :value="false">
                      <n-space align="center">
                        <User :size="24" />
                        <span>实名提交</span>
                      </n-space>
                    </n-radio>
                    <n-radio :value="true">
                      <n-space align="center">
                        <EyeOff :size="24" />
                        <span>匿名提交</span>
                      </n-space>
                    </n-radio>
                  </n-space>
                </n-radio-group>
              </n-form-item>
              
              <!-- 个人信息 (仅实名提交时显示) -->
              <div v-if="!form_data.is_anonym">
                <n-form-item label="姓名" path="name" required>
                  <n-input v-model:value="form_data.name" placeholder="请输入您的姓名" />
                </n-form-item>
                
                <n-form-item label="学号" path="student_id" required>
                  <n-input v-model:value="form_data.student_id" placeholder="请输入您的学号" />
                </n-form-item>
                
                <n-form-item label="邮箱" path="email">
                  <n-input v-model:value="form_data.email" placeholder="请输入您的邮箱" />
                </n-form-item>
                
                <n-form-item label="电话" path="phone">
                  <n-input v-model:value="form_data.phone" placeholder="请输入您的联系电话" />
                </n-form-item>
              </div>
              
              <!-- 反馈内容 -->
              <n-form-item label="内容填写" path="content" required>
                <div>
                  <n-input
                    v-model:value="form_data.content"
                    type="textarea"
                    placeholder="请详细描述您的建议或申诉内容，包括具体情形、时间、地点等信息"
                    style="width:100%; resize: none;"
                    @input="checkContentLength"
                  />
                  <div class="word-count" :class="{ 'word-count-error': contentTooLong }">
                    {{ form_data.content.length }}/200字
                  </div>
                </div>
              </n-form-item>
              
              <!-- 联系方式 (匿名提交时显示) -->
              <n-form-item v-if="form_data.is_anonym" label="联系方式" path="contact">
                <n-input
                  v-model:value="form_data.contact"
                  placeholder="请输入您的手机号或邮箱（用于回复）"
                />
              </n-form-item>
              
              <!-- 紧急程度 -->
              <n-form-item label="紧急程度" path="priority" required>
                <n-select
                  v-model:value="form_data.priority"
                  :options="priority_opts"
                  placeholder="请选择紧急程度"
                />
              </n-form-item>
              
              <!-- 附件上传 -->
              <n-form-item label="附件" path="attachments" required>
                <n-upload
                  v-model:file-list="form_data.attachments"
                  multiple
                  directory-dnd
                  :max="5"
                  :max-size="10 * 1024 * 1024"
                >
                  <n-upload-dragger>
                    <div style="padding: 20px 0">
                      <n-space vertical>
                        <n-icon size="48" :depth="3">
                          <Upload :size="24" />
                        </n-icon>
                        <n-text style="font-size: 16px">
                          点击或者拖动文件到该区域来上传
                        </n-text>
                        <n-text depth="3" style="font-size: 14px">
                          支持图片、PDF、Word文档，最大10MB（必填）
                        </n-text>
                      </n-space>
                    </div>
                  </n-upload-dragger>
                </n-upload>
              </n-form-item>
            </n-form>
            
            <!-- 底部提交区域 -->
            <div class="form-actions">
              <n-space justify="end">
                <n-button @click="resetForm">重置</n-button>
                <n-button type="primary" @click="submitForm" :loading="submitting">
                  提交反馈
                </n-button>
              </n-space>
            </div>
          </n-card>
        </n-tab-pane>
        
        <n-tab-pane name="history" tab="历史记录">
          <n-card>
            <n-empty v-if="feed_list.length === 0" description="暂无历史记录" />
            <n-list v-else>
              <n-list-item v-for="item in feed_list" :key="item.id">
                <n-thing
                  :title="item.title"
                  :description="formatDate(item.submit_time)"
                >
                  <template #avatar>
                    <n-tag :type="getStatusType(item.status)" size="small">
                      {{ item.status }}
                    </n-tag>
                  </template>
                  <template #default>
                    <n-ellipsis :line-clamp="2" style="max-width: 100%">
                      {{ item.content }}
                    </n-ellipsis>
                  </template>
                  <template #footer>
                    <n-space justify="end">
                      <n-button text @click="viewItem(item)">
                        <template #icon>
                          <Eye :size="24" />
                        </template>
                        查看详情
                      </n-button>
                    </n-space>
                  </template>
                </n-thing>
              </n-list-item>
            </n-list>
          </n-card>
        </n-tab-pane>
        
        <n-tab-pane name="process" tab="处理流程">
          <n-card>
            <n-steps vertical>
              <n-step title="提交反馈" description="填写反馈表单并提交" status="process">
                <template #icon>
                  <n-icon><FileText :size="24" /></n-icon>
                </template>
              </n-step>
              <n-step title="等待处理" description="管理员接收并审核您的反馈" status="process">
                <template #icon>
                  <n-icon><Clock :size="24" /></n-icon>
                </template>
              </n-step>
              <n-step title="处理中" description="相关部门正在处理您的反馈" status="process">
                <template #icon>
                  <n-icon><Settings :size="24" /></n-icon>
                </template>
              </n-step>
              <n-step title="处理完成" description="您的反馈已处理完毕，请查看回复" status="process">
                <template #icon>
                  <n-icon><CheckCircle :size="24" /></n-icon>
                </template>
              </n-step>
            </n-steps>
            
            <div class="process-tips">
              <n-alert title="处理说明" type="info">
                <template #icon>
                  <InfoCircle :size="24" />
                </template>
                <p>1. 一般反馈将在3个工作日内处理</p>
                <p>2. 紧急反馈将在1个工作日内处理</p>
                <p>3. 非常紧急的反馈将在24小时内处理</p>
                <p>4. 您可以在"历史记录"中查看反馈处理状态</p>
              </n-alert>
            </div>
          </n-card>
        </n-tab-pane>
      </n-tabs>
    </div>
    
    <!-- 详情弹窗 -->
    <n-modal v-model:show="modal" preset="card" title="反馈详情" style="width: 600px; max-width: 100%;">
      <n-descriptions bordered>
        <n-descriptions-item label="反馈类型">
          {{ curr_item?.feed_type }}
        </n-descriptions-item>
        <n-descriptions-item label="提交方式">
          {{ curr_item?.is_anonym ? '匿名提交' : '实名提交' }}
        </n-descriptions-item>
        <n-descriptions-item label="提交时间">
          {{ formatDate(curr_item?.submit_time) }}
        </n-descriptions-item>
        <n-descriptions-item label="状态">
          <n-tag :type="getStatusType(curr_item?.status)">
            {{ curr_item?.status }}
          </n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="紧急程度">
          {{ getUrgencyText(curr_item?.urgency) }}
        </n-descriptions-item>
        <n-descriptions-item label="反馈标题" :span="3">
          {{ curr_item?.title }}
        </n-descriptions-item>
        <n-descriptions-item label="反馈内容" :span="3">
          <div style="white-space: pre-wrap;">{{ curr_item?.content }}</div>
        </n-descriptions-item>
        <n-descriptions-item v-if="curr_item?.reply" label="回复内容" :span="3">
          <div style="white-space: pre-wrap;">{{ curr_item?.reply }}</div>
        </n-descriptions-item>
      </n-descriptions>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useMessage } from 'naive-ui'
import { 
  IconUser as User,
  IconEyeOff as EyeOff,
  IconUpload as Upload,
  IconEye as Eye,
  IconFileText as FileText,
  IconClock as Clock,
  IconSettings as Settings,
  IconCircleCheck as CheckCircle,
  IconInfoCircle as InfoCircle
} from '@tabler/icons-vue'
import type { 
  IPostFeedbackReq, 
  IPostFeedbackResp, 
  IGetFeedbacksResp, 
  IFeedbackItem 
} from '../../../types/api'
import { getFeedbacks, postFeedback } from '@/api'
import axios from 'axios'
import request from '@/utils/request'

// 使用系统中统一配置好的 http 实例（即 request）
const http = request



// 消息提示
const message = useMessage()

// 表单引用
const form_ref = ref<any>(null)

// 标签页状态
const active_tab = ref('submit')

// 提交状态
const submitting = ref(false)

// 表单数据
const form_data = reactive<{
  feed_type: string
  is_anonym: boolean
  name: string
  student_id: string
  email: string
  phone: string
  content: string
  contact: string
  priority: string
  attachments: Array<{ file: File; name: string }>
}>({
  feed_type: '',
  is_anonym: false,
  name: '',
  student_id: '',
  email: '',
  phone: '',
  content: '',
  contact: '',
  priority: 'low',
  attachments: []
})

// 内容字数限制
const contentTooLong = computed(() => form_data.content.length > 200)

// 检查内容长度
const checkContentLength = () => {
  if (form_data.content.length > 200) {
    message.warning('内容不能超过200字')
  }
}

// 处理匿名/实名切换
const handleAnonymChange = (value: boolean) => {
  if (value) {
    // 匿名提交时清空个人信息
    form_data.name = ''
    form_data.student_id = ''
    form_data.email = ''
    form_data.phone = ''
  }
}

// 表单验证规则
const form_rules = {
  feed_type: {
    required: true,
    message: '请选择反馈类型',
    trigger: 'blur'
  },
  content: {
    required: true,
    message: '请输入反馈内容',
    trigger: 'blur',
    validator: (rule: any, value: string) => {
      if (value.length > 200) {
        return new Error('内容不能超过200字')
      }
      return true
    }
  },
  attachments: {
    required: true,
    message: '请上传至少一个附件',
    trigger: 'blur',
    validator: (rule: any, value: any[]) => {
      if (!value || value.length === 0) {
        return new Error('请上传至少一个附件')
      }
      return true
    }
  },
  name: {
    required: true,
    message: '请输入姓名',
    trigger: 'blur'
  },
  student_id: {
    required: true,
    message: '请输入学号',
    trigger: 'blur'
  }
}

// 反馈类型选项 - 与后端API的分类保持一致
const feed_types = [
  { label: '建议', value: 'suggestion' },
  { label: '申诉', value: 'appeal' },
  { label: '问题', value: 'issue' },
  { label: '其他', value: 'other' }
]

// 紧急程度选项
const priority_opts = [
  { label: '一般', value: 'low' },
  { label: '紧急', value: 'medium' }
]

// 历史记录列表
interface FeedItem {
  id: number
  feed_type: string // 前端显示的反馈类型
  title: string
  content: string
  status: string // 前端显示的状态
  submit_time: string
  is_anonym: boolean
  urgency: string
  reply?: string
  // 以下是与API对应的原始字段
  category?: string // API中的分类
  feedbackstatus?: string // API中的状态
  name?: string
  student_id?: string
  email?: string
  phone?: string
  date?: string
  createdAt?: string
  updatedAt?: string
  attachments?: any[]
}

const feed_list = ref<FeedItem[]>([])

// 详情弹窗
const modal = ref(false)
const curr_item = ref<FeedItem | null>(null)

// 获取历史记录
const getFeedList = async (): Promise<void> => {
  try {
    const response = await getFeedbacks({ page: 1, pageSize: 10 })
    if (response && response.data) {
      // 将API返回的数据转换为组件需要的格式
      feed_list.value = response.data.map((item: IFeedbackItem) => ({
        id: item.id,
        feed_type: mapCategoryToFeedType(item.category),
        title: item.content ? item.content.substring(0, 20) + (item.content.length > 20 ? '...' : '') : '无标题',
        content: item.content || '',
        status: mapFeedbackStatus(item.feedbackstatus),
        submit_time: item.createdAt || item.date || '',
        is_anonym: !item.name, // 如果没有名字，则视为匿名
        urgency: 'normal', // 默认普通紧急程度
        reply: '' // API中暂无回复字段
      }))
    }
  } catch (error) {
    console.error('获取反馈列表失败:', error)
    message.error('获取反馈列表失败，请稍后重试')
    feed_list.value = [] // 出错时设置为空数组
  }
}

// 将API的分类映射到前端的反馈类型
const mapCategoryToFeedType = (category?: string): string => {
  if (!category) return '其他'
  const typeMap: Record<string, string> = {
    'Suggestion_建议': '建议',
    'Appeal_申诉': '申诉',
    'Issue_问题': '问题',
    'Other_其他': '其他'
  }
  return typeMap[category] || '其他'
}

// 将API的状态映射到前端的状态
const mapFeedbackStatus = (status?: string): string => {
  if (!status) return '未处理'
  const statusMap: Record<string, string> = {
    'pending_待处理': '未处理',
    'processing_处理中': '处理中',
    'resolved_已处理': '已处理'
  }
  return statusMap[status] || '未处理'
}

// 格式化日期
const formatDate = (dateStr?: string): string => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 获取状态类型
const getStatusType = (status?: string): string => {
  if (!status) return 'default'
  const typeMap: Record<string, string> = {
    '未处理': 'warning',
    '处理中': 'info',
    '已处理': 'success',
    '已拒绝': 'error'
  }
  return typeMap[status] || 'default'
}

// 获取紧急程度文本
const getUrgencyText = (priority?: string): string => {
  if (!priority) return '一般'
  const textMap: Record<string, string> = {
    'low': '一般',
    'medium': '紧急'
  }
  return textMap[priority] || '一般'
}

// 查看详情
const viewItem = (item: FeedItem): void => {
  curr_item.value = item
  modal.value = true
}

// 重置表单
const resetForm = () => {
  if (form_ref.value) {
    form_ref.value.restoreValidation()
  }
  Object.assign(form_data, {
    feed_type: '',
    is_anonym: false,
    name: '',
    student_id: '',
    email: '',
    phone: '',
    content: '',
    contact: '',
    priority: 'low',
    attachments: []
  })
}



// 使用axios提交表单（适用于Strapi v4格式）
const submitForm = async (): Promise<void> => {
  if (!form_ref.value) return
  
  try {
    await form_ref.value.validate()
    submitting.value = true
    
    // 将前端反馈类型映射到API的分类
    const mapFeedTypeToCategory = (feedType: string | null): string => {
      if (!feedType) return 'Other_其他'
      const categoryMap: Record<string, string> = {
        'suggestion': 'Suggestion_建议',
        'appeal': 'Appeal_申诉',
        'issue': 'Issue_问题',
        'other': 'Other_其他'
      }
      return categoryMap[feedType] || 'Other_其他'
    }
    
    // 检查附件是否上传
    if (!form_data.attachments || form_data.attachments.length === 0) {
      message.error('请上传至少一个附件')
      submitting.value = false
      return
    }
    
    // 检查内容长度
    if (form_data.content.length > 200) {
      message.error('内容不能超过200字')
      submitting.value = false
      return
    }
    
    // 检查实名提交时的必填字段
    if (!form_data.is_anonym) {
      if (!form_data.name || !form_data.student_id) {
        message.error('实名提交时姓名和学号为必填项')
        submitting.value = false
        return
      }
    }
    
    // 创建FormData对象（Strapi v4格式）
    const formData = new FormData()
    
    // ✅ 添加JSON数据到FormData
    formData.append('data', JSON.stringify({
      name: form_data.is_anonym ? '' : form_data.name,
      student_id: form_data.is_anonym ? '' : form_data.student_id,
      email: form_data.is_anonym ? (form_data.contact?.includes('@') ? form_data.contact : '') : form_data.email,
      phone: form_data.is_anonym ? (form_data.contact?.includes('@') ? '' : form_data.contact) : form_data.phone,
      date: new Date().toISOString().split('T')[0],
      content: form_data.content,
      category: mapFeedTypeToCategory(form_data.feed_type)
    }))
    
    // 添加文件（注意字段名必须和Strapi中定义的媒体字段一致）
    form_data.attachments?.forEach(fileInfo => {
      if (fileInfo.file instanceof File) {
        formData.append('files.attachments', fileInfo.file) // 
      }
    })
    
    // 调用API提交
    try {
      // 不要设置Content-Type，让axios自动处理
      const response = await axios.post(`${http.defaults.baseURL}/feedbacks`, formData)
      
      submitting.value = false
      if (response && response.data) {
        message.success('反馈提交成功')
        resetForm()
        // 切换到历史记录标签
        active_tab.value = 'history'
        // 刷新历史记录
        getFeedList()
      } else {
        throw new Error('提交响应异常')
      }
    } catch (apiError) {
      console.error('API提交失败:', apiError)
      message.error('提交失败，请稍后重试')
      submitting.value = false
    }
  } catch (error) {
    submitting.value = false
    console.error('表单验证失败或提交出错:', error)
    message.error('提交失败，请检查表单或稍后重试')
  }
}

// 组件挂载时获取历史记录
onMounted(() => {
  getFeedList()
})
</script>

<style scoped>
.feedback-container {
  width: 100%;
  padding: 16px 24px;
  background-color: #f8f9fa;
  min-height: 100vh;
  box-sizing: border-box;
  overflow-x: hidden;
}

/* 页面标题 */
.page_header {
  text-align: left;
  margin-bottom: 20px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.page_header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.page_header p {
  font-size: 14px;
  color: #666;
  margin: 0;
}

.feedback-header {
  margin-bottom: 24px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.form-actions {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.word-count {
  text-align: right;
  color: #999;
  font-size: 12px;
  margin-top: 4px;
}

.word-count-error {
  color: #f5222d;
}

.process-tips {
  margin-top: 24px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}
</style>