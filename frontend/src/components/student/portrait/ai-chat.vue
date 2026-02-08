<template>
  <div class="ai-chat-container">
    <!-- 顶部标题栏 -->
    <div class="chat-header">
      <div class="header-content">
        <n-icon size="24" class="header-icon">
          <IconMessageCircle />
        </n-icon>
        <h2 class="header-title">AI学习助手</h2>
        <span class="header-subtitle">个性化学习分析与建议</span>
      </div>
    </div>

    <!-- 聊天消息区域 -->
    <div class="chat-messages" ref="msg_container">
      <n-scrollbar style="max-height: 100%;">
        <div class="messages-wrapper">
          <!-- 欢迎消息 -->
          <div v-if="msg_list.length === 0" class="welcome-message">
            <div class="welcome-content">
              <n-icon size="48" class="welcome-icon">
                <IconUser />
              </n-icon>
              <h3>欢迎使用AI学习助手</h3>
              <p>我可以为您提供以下服务：</p>
              <div class="service-tags">
                <n-tag type="info" size="small">学习分析</n-tag>
                <n-tag type="success" size="small">兴趣推荐</n-tag>
                <n-tag type="warning" size="small">职业规划</n-tag>
                <n-tag type="error" size="small">学情预警</n-tag>
              </div>
            </div>
          </div>

          <!-- 消息列表 -->
          <div
            v-for="(message, index) in msg_list"
            :key="index"
            class="message-item"
            :class="{ 'is-user': message.role === 'user', 'is-assistant': message.role === 'assistant' }"
          >
            <div class="message-avatar">
              <n-avatar
                v-if="message.role === 'user'"
                round
                size="small"
                style="background-color: #409eff;"
              >
                {{ user_name.charAt(0) }}
              </n-avatar>
              <n-icon v-else size="24" class="ai-avatar">
                <IconUser />
              </n-icon>
            </div>
            <div class="message-content">
              <div class="message-bubble">
                <div class="message-text" v-html="formatMessage(message.content)"></div>
                <div class="message-time">{{ formatTime(message.timestamp) }}</div>
              </div>
            </div>
          </div>

          <!-- 加载状态 -->
          <div v-if="is_loading" class="message-item is-assistant">
            <div class="message-avatar">
              <n-icon size="24" class="ai-avatar">
                <IconUser />
              </n-icon>
            </div>
            <div class="message-content">
              <div class="message-bubble loading">
                <n-spin size="small" />
                <span class="loading-text">AI正在思考中...</span>
              </div>
            </div>
          </div>
        </div>
      </n-scrollbar>
    </div>

    <!-- 快捷功能按钮 -->
    <div class="quick-actions">
      <n-space>
        <n-button
          size="small"
          type="primary"
          ghost
          @click="sendQuickMessage('请分析我的学习成果数据')"
        >
          <template #icon>
            <n-icon><IconChartBar /></n-icon>
          </template>
          成果分析
        </n-button>
        <n-button
          size="small"
          type="success"
          ghost
          @click="sendQuickMessage('根据我的兴趣推荐相关课程')"
        >
          <template #icon>
            <n-icon><IconAward /></n-icon>
          </template>
          兴趣推荐
        </n-button>
        <n-button
          size="small"
          type="warning"
          ghost
          @click="sendQuickMessage('为我制定职业规划建议')"
        >
          <template #icon>
            <n-icon><IconUser /></n-icon>
          </template>
          职业规划
        </n-button>
        <n-button
          size="small"
          type="error"
          ghost
          @click="sendQuickMessage('检查我的学习预警情况')"
        >
          <template #icon>
            <n-icon><IconHelpCircle /></n-icon>
          </template>
          学情预警
        </n-button>
      </n-space>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input">
      <div class="input-wrapper">
        <n-input
          v-model:value="input_msg"
          type="textarea"
          placeholder="请输入您的问题..."
          :autosize="{ minRows: 1, maxRows: 4 }"
          :disabled="is_loading"
          @keydown.enter.prevent="handleEnterKey"
          class="message-input"
        />
        <n-button
          type="primary"
          :loading="is_loading"
          :disabled="!input_msg.trim()"
          @click="sendMessage"
          class="send-button"
        >
          <template #icon>
            <n-icon><IconMessageCircle /></n-icon>
          </template>
          发送
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onMounted } from 'vue'
import { NIcon, NScrollbar, NAvatar, NTag, NSpin, NSpace, NButton, NInput, useMessage } from 'naive-ui'
import {
  IconMessageCircle,
  IconUser,
  IconChartBar,
  IconAward,
  IconHelpCircle
} from '../../../utils/icons'
import {
  fetchStudentPortraitByStudentId,
  createStudentPortrait,
  addQaHistory,
  chatWithAI,
  fetchStudentMe
} from '../../../server/api/api'

// 消息接口定义
interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

// 响应式数据
const msg_list = ref<ChatMessage[]>([])
const input_msg = ref('')
const is_loading = ref(false)
const user_name = ref('学生')
const msg_container = ref<HTMLElement>()
const message = useMessage()

// 学生画像数据
const portrait_data = ref<any>(null)
const student_id = ref<string>('')

// 组件挂载时初始化
onMounted(async () => {
  await initializeUser()
  await loadStudentPortrait()
  // 添加欢迎消息
  if (portrait_data.value) {
    addMessage('assistant', `您好！我是您的AI学习助手。基于您的学习画像，我可以为您提供个性化的学习建议和分析。`)
  }
})

// 初始化用户信息
const initializeUser = async () => {
  try {
    console.log('正在获取当前登录用户信息...')
    const userResponse = await fetchStudentMe()
    console.log('获取用户信息响应:', userResponse)
    
    if (userResponse && userResponse.data) {
      // 优先使用student_id字段，如果没有则使用id字段
      const studentId = userResponse.data.student_id || userResponse.data.id
      if (studentId) {
        student_id.value = studentId.toString()
        user_name.value = userResponse.data.username || userResponse.data.name || '学生'
        console.log('设置学生ID:', student_id.value)
        console.log('设置用户名:', user_name.value)
      } else {
        console.error('响应中没有找到student_id或id字段')
        throw new Error('无法获取学生身份信息')
      }
    } else {
      console.error('API响应数据为空')
      throw new Error('无法获取用户信息')
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    // 显示错误提示给用户
    message.error('无法获取学生身份信息，请重新登录')
    student_id.value = ''
    user_name.value = ''
  }
}

// 加载学生画像数据
const loadStudentPortrait = async () => {
  try {
    const response = await fetchStudentPortraitByStudentId(student_id.value)
    if (response.data && response.data.length > 0) {
      portrait_data.value = response.data[0]
    } else {
      // 如果没有画像数据，创建一个新的
      const newPortrait = {
        student: student_id.value,
        summary: '新用户，正在建立学习画像...',
        skills: [],
        interests: [],
        qa_history: [],
        risk_alerts: []
      }
      const createResponse = await createStudentPortrait(newPortrait)
      portrait_data.value = createResponse.data
    }
  } catch (error) {
    console.error('加载学生画像失败:', error)
  }
}

// 添加消息到列表
const addMessage = (role: 'user' | 'assistant', content: string) => {
  msg_list.value.push({
    role,
    content,
    timestamp: new Date()
  })
  nextTick(() => {
    scrollToBottom()
  })
}

// 滚动到底部
const scrollToBottom = () => {
  if (msg_container.value) {
    const scrollElement = msg_container.value.querySelector('.n-scrollbar-content')
    if (scrollElement) {
      scrollElement.scrollTop = scrollElement.scrollHeight
    }
  }
}

// 发送消息
const sendMessage = async () => {
  if (!input_msg.value.trim() || is_loading.value) return

  const user_message = input_msg.value.trim()
  addMessage('user', user_message)
  input_msg.value = ''
  is_loading.value = true

  try {
    console.log('=== 开始发送消息 ===')
    console.log('用户消息:', user_message)
    console.log('学生ID:', student_id.value)
    console.log('画像数据存在:', !!portrait_data.value)
    
    // 调用AI响应生成
    const ai_response = await generateAIResponse(user_message)
    console.log('收到AI响应:', ai_response)
    
    addMessage('assistant', ai_response)

    // 保存对话历史到学生画像
    if (portrait_data.value && portrait_data.value.id) {
      try {
        const qa_data = {
          question: user_message,
          answer: ai_response,
          timestamp: new Date().toISOString(),
          category: detectMessageCategory(user_message)
        }
        console.log('保存对话历史:', qa_data)
        await addQaHistory(portrait_data.value.id, qa_data)
        console.log('对话历史保存成功')
      } catch (error) {
        console.error('保存对话历史失败，但不影响用户体验:', error)
      }
    } else {
      console.warn('画像数据不存在或缺少ID，跳过保存对话历史')
    }
  } catch (error: any) {
    console.error('=== 发送消息失败 ===')
    console.error('错误对象:', error)
    console.error('错误消息:', error.message)
    console.error('错误堆栈:', error.stack)
    
    // 根据错误类型显示不同的提示
    let errorMessage = '抱歉，AI助手服务暂时不可用，请稍后再试。'
    
    if (error.response?.status === 404) {
      errorMessage = '抱歉，AI聊天服务接口未找到。请联系管理员检查后端配置。'
    } else if (error.response?.status === 500) {
      errorMessage = '抱歉，服务器处理请求时出错。请稍后再试或联系管理员。'
    } else if (error.message?.includes('Network Error')) {
      errorMessage = '抱歉，网络连接失败。请检查网络连接后重试。'
    }
    
    addMessage('assistant', errorMessage)
    message.error(errorMessage)
  } finally {
    is_loading.value = false
    console.log('=== 消息发送流程结束 ===')
  }
}

// 快捷发送消息
const sendQuickMessage = (msg: string) => {
  input_msg.value = msg
  sendMessage()
}

// 处理回车键
const handleEnterKey = (event: KeyboardEvent) => {
  if (!event.shiftKey) {
    sendMessage()
  }
}

// 生成AI响应
const generateAIResponse = async (user_message: string): Promise<string> => {
  try {
    // 确保有学生ID
    if (!student_id.value) {
      console.error('学生ID未设置，无法调用AI聊天')
      return '抱歉，无法获取您的身份信息，请刷新页面重试。'
    }

    // 准备上下文数据
    const contextData = portrait_data.value ? {
      summary: portrait_data.value.summary,
      skills: portrait_data.value.skills,
      interests: portrait_data.value.interests
    } : undefined

    // 调用AI聊天API（已包含错误处理和回退逻辑）
    console.log('准备调用AI聊天API，参数:', {
      question: user_message,
      student_id: student_id.value,
      context: contextData ? 'context_provided' : 'no_context'
    })
    
    const response = await chatWithAI({
      question: user_message,
      student_id: student_id.value,
      context: contextData ? JSON.stringify(contextData) : undefined
    })
    
    console.log('AI聊天API完整响应:', JSON.stringify(response, null, 2))
    console.log('响应类型:', typeof response)
    
    // 注意：由于 http 拦截器已经返回了 response.data
    // 所以这里的 response 就是后端返回的数据对象，不需要再访问 .data
    
    // 情况1: response 本身就是字符串（直接返回的消息）
    if (typeof response === 'string') {
      console.log('响应是字符串，直接返回:', response)
      return response
    }
    
    // 情况2: response 是对象，检查是否是错误响应
    if (response && typeof response === 'object') {
      // 检查错误标志
      if ('error' in response && response.error) {
        console.warn('AI返回错误响应:', response)
        const errorMsg = response.response || response.message || '抱歉，AI助手服务暂时不可用。'
        return typeof errorMsg === 'string' ? errorMsg : '抱歉，AI助手服务暂时不可用。'
      }
      
      // 尝试从多个可能的字段提取AI响应
      const aiResponse = response.response || response.message || response.answer || response.reply || response.data
      
      if (aiResponse && typeof aiResponse === 'string') {
        console.log('成功提取AI响应:', aiResponse)
        return aiResponse
      }
      
      // 如果 aiResponse 是对象，尝试进一步提取
      if (aiResponse && typeof aiResponse === 'object') {
        const nestedResponse = aiResponse.response || aiResponse.message || aiResponse.answer || aiResponse.reply
        if (nestedResponse && typeof nestedResponse === 'string') {
          console.log('从嵌套对象提取AI响应:', nestedResponse)
          return nestedResponse
        }
      }
    }
    
    console.error('无法从响应中提取AI回复，响应结构:', response)
    return '抱歉，我暂时无法回答您的问题。请联系管理员检查后端配置。'
  } catch (error: any) {
    console.error('AI聊天调用失败:', error)
    console.error('错误详情:', error.response?.data || error.message)
    console.error('完整错误对象:', JSON.stringify(error, null, 2))
    
    // 根据错误类型返回不同的提示
    if (error.response?.status === 404) {
      return '抱歉，AI聊天服务接口未找到，请联系管理员检查后端配置。'
    } else if (error.response?.status === 500) {
      const errorMsg = error.response?.data?.error?.message || error.response?.data?.message
      console.error('服务器500错误详情:', errorMsg)
      return `抱歉，服务器处理请求时出错：${errorMsg || '请稍后再试'}`
    } else if (error.message?.includes('Network Error')) {
      return '抱歉，网络连接失败，请检查网络连接后重试。'
    }
    
    return '抱歉，AI助手服务暂时不可用，请稍后再试。'
  }
}

// 检测消息类别
const detectMessageCategory = (message: string): MessageCategory => {
  if (message.includes('成果') || message.includes('分析') || message.includes('数据')) {
    return 'achievement'
  }
  if (message.includes('兴趣') || message.includes('推荐') || message.includes('课程')) {
    return 'interest'
  }
  if (message.includes('职业') || message.includes('规划') || message.includes('就业')) {
    return 'career'
  }
  if (message.includes('预警') || message.includes('风险') || message.includes('学情')) {
    return 'warning'
  }
  return 'general'
}

// 消息类别类型定义
type MessageCategory = 'achievement' | 'interest' | 'career' | 'warning' | 'general'

// 已移除固定模板回复，统一通过后端接口返回内容

// 格式化消息内容
const formatMessage = (content: string): string => {
  return content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
}

// 格式化时间
const formatTime = (timestamp: Date): string => {
  const now = new Date()
  const diff = now.getTime() - timestamp.getTime()
  const minutes = Math.floor(diff / 60000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (minutes < 1440) return `${Math.floor(minutes / 60)}小时前`
  return timestamp.toLocaleDateString()
}
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow: hidden;
}

/* 顶部标题栏 */
.chat-header {
  background: white;
  border-bottom: 1px solid #e8e8e8;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  color: #409eff;
}

.header-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.header-subtitle {
  color: #909399;
  font-size: 14px;
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  padding: 16px;
  overflow: hidden;
}

.messages-wrapper {
  padding: 0 8px;
}

/* 欢迎消息 */
.welcome-message {
  text-align: center;
  padding: 40px 20px;
  color: #606266;
}

.welcome-content {
  max-width: 400px;
  margin: 0 auto;
}

.welcome-icon {
  color: #409eff;
  margin-bottom: 16px;
}

.welcome-content h3 {
  margin: 0 0 12px 0;
  color: #303133;
  font-size: 20px;
}

.welcome-content p {
  margin: 0 0 16px 0;
  color: #606266;
}

.service-tags {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 消息项 */
.message-item {
  display: flex;
  margin-bottom: 16px;
  animation: fadeInUp 0.3s ease-out;
}

.message-item.is-user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
  margin: 0 12px;
}

.ai-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message-content {
  flex: 1;
  max-width: 70%;
}

.message-bubble {
  background: white;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.is-user .message-bubble {
  background: #409eff;
  color: white;
}

.message-bubble.loading {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8f9fa;
  color: #606266;
}

.loading-text {
  font-size: 14px;
}

.message-text {
  line-height: 1.6;
  word-wrap: break-word;
}

.message-text :deep(.emoji) {
  font-size: 16px;
  margin-right: 4px;
}

.message-time {
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 4px;
  text-align: right;
}

.is-user .message-time {
  color: rgba(255, 255, 255, 0.8);
}

/* 快捷操作 */
.quick-actions {
  padding: 12px 24px;
  background: white;
  border-top: 1px solid #f0f0f0;
}

/* 输入区域 */
.chat-input {
  background: white;
  border-top: 1px solid #e8e8e8;
  padding: 16px 24px;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.message-input {
  flex: 1;
}

.send-button {
  flex-shrink: 0;
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-header {
    padding: 12px 16px;
  }
  
  .header-title {
    font-size: 16px;
  }
  
  .chat-messages {
    padding: 12px;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .chat-input {
    padding: 12px 16px;
  }
  
  .quick-actions {
    padding: 8px 16px;
  }
  
  .service-tags {
    gap: 6px;
  }
}
</style>