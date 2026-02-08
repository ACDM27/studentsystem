<template>
  <div class="portrait-chat">
    <!-- 顶部标题栏 -->
    <div class="chat-header">
      <div class="header-content">
        <div class="header-left">
          <n-icon size="24" class="header-icon">
            <IconMessageCircle />
          </n-icon>
          <div class="header-info">
            <h2 class="header-title">AI学习助手</h2>
            <p class="header-subtitle">个性化学习分析与建议</p>
          </div>
        </div>
        <div class="header-actions">
          <n-button size="small" type="primary" ghost @click="clearHistory">
            <template #icon>
              <n-icon><IconTrash /></n-icon>
            </template>
            清空对话
          </n-button>
          <n-button size="small" type="info" ghost @click="exportChat">
            <template #icon>
              <n-icon><IconDownload /></n-icon>
            </template>
            导出记录
          </n-button>
        </div>
      </div>
    </div>

    <!-- 快捷功能按钮 -->
    <div class="quick-actions">
      <div class="action-group">
        <h4 class="group-title">快速分析</h4>
        <div class="action-buttons">
          <n-button
            size="small"
            type="primary"
            ghost
            @click="sendQuickMessage('请分析我的学习成果数据')"
          >
            <template #icon>
              <n-icon><IconChartBar /></n-icon>
            </template>
            学习成果
          </n-button>
          <n-button
            size="small"
            type="success"
            ghost
            @click="sendQuickMessage('根据我的兴趣为我推荐学习内容')"
          >
            <template #icon>
              <n-icon><IconHeart /></n-icon>
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
              <n-icon><IconTarget /></n-icon>
            </template>
            职业规划
          </n-button>
          <n-button
            size="small"
            type="error"
            ghost
            @click="sendQuickMessage('分析我的学情预警信息')"
          >
            <template #icon>
              <n-icon><IconAlertTriangle /></n-icon>
            </template>
            学情预警
          </n-button>
        </div>
      </div>
    </div>

    <!-- 对话区域 -->
    <div class="chat-container">
      <div class="chat-messages" ref="messagesContainer">
        <!-- 欢迎消息 -->
        <div v-if="chat_messages.length === 0" class="welcome-message">
          <div class="welcome-content">
            <n-icon size="48" class="welcome-icon">
              <IconMessageCircle />
            </n-icon>
            <h3>欢迎使用AI学习助手</h3>
            <p>我可以为您提供个性化的学习分析和建议，包括：</p>
            <ul class="feature-list">
              <li><n-icon size="16"><IconChartBar /></n-icon> 学习成果数据分析</li>
              <li><n-icon size="16"><IconHeart /></n-icon> 个性化兴趣推荐</li>
              <li><n-icon size="16"><IconTarget /></n-icon> 职业规划指导</li>
              <li><n-icon size="16"><IconAlertTriangle /></n-icon> 学情预警提醒</li>
            </ul>
            <p class="welcome-tip">请选择上方的快捷功能或直接输入您的问题开始对话</p>
          </div>
        </div>

        <!-- 对话消息列表 -->
        <div
          v-for="message in chat_messages"
          :key="message.id"
          class="message-item"
          :class="`message-${message.type}`"
        >
          <div class="message-avatar">
            <n-avatar
              v-if="message.type === 'user'"
              size="small"
              :src="user_avatar"
              class="user-avatar"
            >
              {{ user_name.charAt(0) }}
            </n-avatar>
            <n-icon v-else size="24" class="ai-avatar">
              <IconMessageCircle />
            </n-icon>
          </div>
          
          <div class="message-content">
            <div class="message-header">
              <span class="message-sender">
                {{ message.type === 'user' ? user_name : 'AI助手' }}
              </span>
              <span class="message-time">
                {{ formatTime(message.timestamp) }}
              </span>
            </div>
            
            <div class="message-body">
              <div v-if="message.type === 'user'" class="user-message">
                {{ message.content }}
              </div>
              
              <div v-else class="ai-message">
                <!-- AI消息支持富文本显示 -->
                <div v-if="message.loading" class="loading-message">
                  <n-spin size="small" />
                  <span>AI正在思考中...</span>
                </div>
                
                <div v-else class="ai-content">
                  <!-- 如果有结构化数据，特殊显示 -->
                  <div v-if="message.data" class="structured-data">
                    <!-- 学习成果数据 -->
                    <div v-if="message.data.type === 'learning_stats'" class="stats-display">
                      <h4>📊 学习成果分析</h4>
                      <div class="stats-grid">
                        <div class="stat-card">
                          <div class="stat-value">{{ message.data.total_hours }}</div>
                          <div class="stat-label">总学习时长</div>
                        </div>
                        <div class="stat-card">
                          <div class="stat-value">{{ message.data.avg_score }}</div>
                          <div class="stat-label">平均成绩</div>
                        </div>
                        <div class="stat-card">
                          <div class="stat-value">{{ message.data.completed_courses }}</div>
                          <div class="stat-label">完成课程</div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 兴趣推荐 -->
                    <div v-if="message.data.type === 'interest_recommendations'" class="recommendations">
                      <h4>💡 兴趣推荐</h4>
                      <div class="recommendation-list">
                        <div
                          v-for="item in message.data.items"
                          :key="item.id"
                          class="recommendation-item"
                        >
                          <div class="rec-header">
                            <n-icon size="16" :style="{ color: item.color }">
                              <component :is="getRecommendationIcon(item.category)" />
                            </n-icon>
                            <span class="rec-title">{{ item.title }}</span>
                            <n-rate :value="item.match_score" readonly size="small" />
                          </div>
                          <p class="rec-desc">{{ item.description }}</p>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 职业规划 -->
                    <div v-if="message.data.type === 'career_plan'" class="career-plan">
                      <h4>🎯 职业规划建议</h4>
                      <div class="career-timeline">
                        <div
                          v-for="phase in message.data.phases"
                          :key="phase.id"
                          class="timeline-item"
                        >
                          <div class="timeline-marker"></div>
                          <div class="timeline-content">
                            <h5>{{ phase.title }}</h5>
                            <p class="phase-duration">{{ phase.duration }}</p>
                            <ul class="phase-goals">
                              <li v-for="goal in phase.goals" :key="goal">{{ goal }}</li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 学情预警 -->
                    <div v-if="message.data.type === 'learning_alerts'" class="alerts-display">
                      <h4>学情预警分析</h4>
                      <div class="alerts-list">
                        <div
                          v-for="alert in message.data.alerts"
                          :key="alert.id"
                          class="alert-item"
                          :class="`alert-${alert.level}`"
                        >
                          <div class="alert-header">
                            <n-icon size="16">
                              <IconAlertTriangle />
                            </n-icon>
                            <span class="alert-title">{{ alert.title }}</span>
                            <n-tag :type="getAlertTagType(alert.level)" size="small">
                              {{ getAlertLevelText(alert.level) }}
                            </n-tag>
                          </div>
                          <p class="alert-desc">{{ alert.description }}</p>
                          <div class="alert-suggestions">
                            <strong>建议措施：</strong>
                            <ul>
                              <li v-for="suggestion in alert.suggestions" :key="suggestion">
                                {{ suggestion }}
                              </li>
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 普通文本消息 -->
                  <div v-else class="text-content formatted-text">
                    <div v-html="formatMessageContent(message.content)"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 消息操作按钮 -->
            <div v-if="message.type === 'ai' && !message.loading" class="message-actions">
              <n-button size="tiny" text @click="copyMessage(message.content)">
                <template #icon>
                  <n-icon><IconCopy /></n-icon>
                </template>
                复制
              </n-button>
              <n-button size="tiny" text @click="likeMessage(message.id)">
                <template #icon>
                  <n-icon><IconThumbUp /></n-icon>
                </template>
                有用
              </n-button>
              <n-button size="tiny" text @click="regenerateMessage(message.id)">
                <template #icon>
                  <n-icon><IconRefresh /></n-icon>
                </template>
                重新生成
              </n-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input">
        <div class="input-container">
          <n-input
            v-model:value="input_message"
            type="textarea"
            placeholder="请输入您的问题，我会为您提供个性化的学习分析和建议..."
            :autosize="{ minRows: 1, maxRows: 4 }"
            :disabled="is_sending"
            @keydown.enter.prevent="handleEnterKey"
            class="message-input"
          />
          
          <div class="input-actions">
            <n-button
              type="primary"
              :loading="is_sending"
              :disabled="!input_message.trim()"
              @click="sendMessage"
              class="send-button"
            >
              <template #icon>
                <n-icon><IconSend /></n-icon>
              </template>
              发送
            </n-button>
          </div>
        </div>
        
        <!-- 输入提示 -->
        <div class="input-tips">
          <span class="tip-text">💡 提示：按 Ctrl+Enter 快速发送消息</span>
          <span class="char-count">{{ input_message.length }}/500</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onMounted } from 'vue'
import {
  NIcon,
  NButton,
  NAvatar,
  NSpin,
  NInput,
  NRate,
  NTag,
  useMessage,
  useDialog
} from 'naive-ui'
import {
  IconMessageCircle,
  IconTrash,
  IconDownload,
  IconChartBar,
  IconHeart,
  IconTarget,
  IconAlertTriangle,
  IconThumbUp,
  IconRefresh,
  IconBook,
  IconCode,
  IconMusic,
  IconCamera,
} from '../../../utils/icons'
import {
  chatWithAI,
  getStudentMe as fetchStudentMe
} from '@/api'

// 响应式数据
const user_name = ref('刘在行')
const user_avatar = ref('')
const input_message = ref('')
const is_sending = ref(false)
const student_id = ref<string>('')
const messagesContainer = ref<HTMLElement>()
const message = useMessage()
const dialog = useDialog()

// 对话消息列表
interface ChatMessage {
  id: string
  type: 'user' | 'ai'
  content: string
  timestamp: Date
  loading?: boolean
  data?: any
}

const chat_messages = ref<ChatMessage[]>([])

// 组件挂载时初始化
onMounted(async () => {
  await initializeUser()
  loadChatHistory()
})

// 初始化用户信息 - 调用后端
const initializeUser = async () => {
  try {
    const userRes = await fetchStudentMe()
    const sid = userRes?.data?.student_id || userRes?.data?.id
    user_name.value = userRes?.data?.username || userRes?.data?.name || '同学'
    student_id.value = sid ? String(sid) : ''
  } catch (err) {
    console.warn('获取用户信息失败:', err)
    user_name.value = '同学'
    student_id.value = ''
  }
}

// 加载对话历史
const loadChatHistory = async () => {
  try {
    // 这里可以从API加载历史对话记录
    // const history = await fetchChatHistory(student_id.value)
    // chat_messages.value = history
  } catch (error) {
    console.error('加载对话历史失败:', error)
  }
}

// 发送快捷消息
const sendQuickMessage = (messageText: string) => {
  input_message.value = messageText
  sendMessage()
}

// 发送消息（调用后端AI接口）
const sendMessage = async () => {
  if (!input_message.value.trim() || is_sending.value) return

  const userMessage: ChatMessage = {
    id: generateId(),
    type: 'user',
    content: input_message.value.trim(),
    timestamp: new Date()
  }

  chat_messages.value.push(userMessage)

  const aiMessage: ChatMessage = {
    id: generateId(),
    type: 'ai',
    content: '',
    timestamp: new Date(),
    loading: true
  }
  chat_messages.value.push(aiMessage)

  const userInput = input_message.value
  input_message.value = ''
  is_sending.value = true

  await scrollToBottom()

  try {
    if (!student_id.value) {
      // 尝试重取用户
      await initializeUser()
    }

    const resp = await chatWithAI({
      message: userInput,
      session_id: null
    })

    const messageIndex = chat_messages.value.findIndex(msg => msg.id === aiMessage.id)
    if (messageIndex !== -1) {
      chat_messages.value[messageIndex] = {
        ...aiMessage,
        ...aiMessage,
        // 适配新 API 响应结构 (移除 .data 包装)
        content: (resp as any).message || (resp as any).data?.response || '抱歉，暂时无法获取回复。',
        loading: false,
        data: (resp as any).data?.structured_data || null
      }
    }
  } catch (error) {
    console.error('AI对话失败:', error)
    const messageIndex = chat_messages.value.findIndex(msg => msg.id === aiMessage.id)
    if (messageIndex !== -1) {
      chat_messages.value[messageIndex] = {
        ...aiMessage,
        content: '抱歉，AI助手服务暂时不可用，请稍后再试。',
        loading: false
      }
    }
  } finally {
    is_sending.value = false
    await scrollToBottom()
  }
}

// 处理回车键
const handleEnterKey = (event: KeyboardEvent) => {
  if (event.ctrlKey || event.metaKey) {
    sendMessage()
  }
}

// 清空对话历史
const clearHistory = () => {
  dialog.warning({
    title: '确认清空',
    content: '确定要清空所有对话记录吗？此操作不可恢复。',
    positiveText: '确定',
    negativeText: '取消',
    onPositiveClick: () => {
      chat_messages.value = []
      message.success('对话记录已清空')
    }
  })
}

// 导出对话记录
const exportChat = () => {
  if (chat_messages.value.length === 0) {
    message.warning('暂无对话记录可导出')
    return
  }
  
  const chatData = chat_messages.value.map(msg => ({
    发送者: msg.type === 'user' ? user_name.value : 'AI助手',
    内容: msg.content,
    时间: formatTime(msg.timestamp)
  }))
  
  const dataStr = JSON.stringify(chatData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  
  const link = document.createElement('a')
  link.href = URL.createObjectURL(dataBlob)
  link.download = `学习助手对话记录_${new Date().toISOString().split('T')[0]}.json`
  link.click()
  
  message.success('对话记录导出成功')
}

// 复制消息
const copyMessage = async (content: string) => {
  try {
    await navigator.clipboard.writeText(content)
    message.success('消息已复制到剪贴板')
  } catch (error) {
    message.error('复制失败')
  }
}

// 点赞消息
const likeMessage = (messageId: string) => {
  // 这里可以调用API记录用户反馈
  message.success('感谢您的反馈！')
}

// 重新生成消息
const regenerateMessage = async (messageId: string) => {
  const messageIndex = chat_messages.value.findIndex(msg => msg.id === messageId)
  if (messageIndex === -1) return
  
  // 找到对应的用户消息
  const userMessageIndex = messageIndex - 1
  if (userMessageIndex < 0 || chat_messages.value[userMessageIndex].type !== 'user') return
  
  const userMessage = chat_messages.value[userMessageIndex].content
  
  // 设置加载状态
  chat_messages.value[messageIndex] = {
    ...chat_messages.value[messageIndex],
    loading: true,
    content: ''
  }
  
  try {
    // 确保有学生ID才能重新生成
    if (!student_id.value) {
      throw new Error('学生身份信息缺失，请重新登录')
    }
    
    const response = await chatWithAI({
      message: userMessage,
      session_id: null
    })
    
    chat_messages.value[messageIndex] = {
      ...chat_messages.value[messageIndex],
      ...chat_messages.value[messageIndex],
      content: (response as any).message || '抱歉，我暂时无法回答这个问题。',
      loading: false,
      data: (response as any).data?.structured_data || null
    }
    
  } catch (error) {
    chat_messages.value[messageIndex] = {
      ...chat_messages.value[messageIndex],
      content: '重新生成失败，请稍后再试。',
      loading: false
    }
    message.error('重新生成失败')
  }
}

// 滚动到底部
let scrollRafId: number | null = null
const scrollToBottom = async () => {
  await nextTick()
  const el = messagesContainer.value
  if (!el) return

  if (scrollRafId) {
    cancelAnimationFrame(scrollRafId)
  }
  scrollRafId = requestAnimationFrame(() => {
    el.scrollTop = el.scrollHeight
    scrollRafId = null
  })
}

// 已移除固定模板回复，统一通过后端接口返回内容

// 获取推荐图标
const getRecommendationIcon = (category: string) => {
  const iconMap: Record<string, any> = {
    tech: IconCode,
    design: IconCamera,
    music: IconMusic,
    sports: IconHeart,
    book: IconBook
  }
  return iconMap[category] || IconBook
}

// 获取预警标签类型
const getAlertTagType = (level: string): 'default' | 'info' | 'success' | 'warning' | 'error' | 'primary' => {
  const typeMap: Record<string, 'default' | 'info' | 'success' | 'warning' | 'error' | 'primary'> = {
    high: 'error',
    medium: 'warning',
    low: 'info'
  }
  return typeMap[level] || 'default'
}

// 获取预警级别文本
const getAlertLevelText = (level: string): string => {
  const textMap: Record<string, string> = {
    high: '高风险',
    medium: '中风险',
    low: '低风险'
  }
  return textMap[level] || '未知'
}

// 生成唯一ID
const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substr(2)
}

// 格式化时间
const formatTime = (timestamp: Date): string => {
  const now = new Date()
  const diff = now.getTime() - timestamp.getTime()
  
  if (diff < 60000) { // 1分钟内
    return '刚刚'
  } else if (diff < 3600000) { // 1小时内
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) { // 24小时内
    return `${Math.floor(diff / 3600000)}小时前`
  } else {
    return timestamp.toLocaleString('zh-CN', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
}

// 格式化消息内容
const formatMessageContent = (content: string): string => {
  // 处理换行符
  let formatted = content.replace(/\n/g, '<br>')
  
  // 处理粗体文本 **text**
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  
  // 处理标题 **数字. 标题**
  formatted = formatted.replace(/\*\*(\d+\.)\s*(.*?)\*\*/g, '<h4 class="section-title">$1 $2</h4>')
  
  // 处理列表项 - text
  formatted = formatted.replace(/^-\s+(.*)$/gm, '<li class="list-item">$1</li>')
  
  // 包装连续的列表项
  formatted = formatted.replace(/((<li class="list-item">.*?<\/li>\s*)+)/g, '<ul class="formatted-list">$1</ul>')
  
  // 处理缩进内容（以两个空格开头）
  formatted = formatted.replace(/^\s\s-\s+(.*)$/gm, '<li class="sub-list-item">$1</li>')
  
  // 包装子列表
  formatted = formatted.replace(/((<li class="sub-list-item">.*?<\/li>\s*)+)/g, '<ul class="sub-formatted-list">$1</ul>')
  
  return formatted
}
</script>

<style scoped>
.portrait-chat {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f5f7fa;
}

/* 顶部标题栏 */
.chat-header {
  background: white;
  border-bottom: 1px solid #e8eaec;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px;
  border-radius: 8px;
}

.header-info {
  display: flex;
  flex-direction: column;
}

.header-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.header-subtitle {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.header-actions {
  display: flex;
  gap: 8px;
}

/* 快捷功能按钮 */
.quick-actions {
  background: white;
  border-bottom: 1px solid #e8eaec;
  padding: 16px 24px;
}

.action-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.group-title {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* 对话容器 */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 消息区域 */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  scroll-behavior: smooth;
}

/* 欢迎消息 */
.welcome-message {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  min-height: 400px;
}

.welcome-content {
  text-align: center;
  max-width: 500px;
  padding: 40px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.welcome-icon {
  color: #667eea;
  margin-bottom: 16px;
}

.welcome-content h3 {
  margin: 0 0 16px;
  font-size: 24px;
  color: #333;
}

.welcome-content p {
  margin: 0 0 16px;
  color: #666;
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 16px 0;
  text-align: left;
}

.feature-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
  color: #555;
}

.welcome-tip {
  font-size: 14px;
  color: #999;
  font-style: italic;
}

/* 消息项 */
.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  align-items: flex-start;
}

.message-item.message-user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.user-avatar {
  background: #667eea;
}

.ai-avatar {
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  color: white;
  padding: 8px;
  border-radius: 50%;
}

.message-content {
  flex: 1;
  max-width: 70%;
}

.message-user .message-content {
  text-align: right;
  max-width: fit-content;
  min-width: 120px;
  margin-left: auto;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.message-user .message-header {
  justify-content: flex-end;
}

.message-sender {
  font-size: 12px;
  font-weight: 500;
  color: #666;
}

.message-time {
  font-size: 12px;
  color: #999;
}

.message-body {
  margin-bottom: 8px;
}

/* 用户消息 */
.user-message {
  background: #667eea;
  color: white;
  padding: 12px 16px;
  border-radius: 16px 16px 4px 16px;
  word-wrap: break-word;
  line-height: 1.5;
  display: inline-block;
  max-width: 100%;
  width: fit-content;
  min-width: 60px;
}

/* AI消息 */
.ai-message {
  background: white;
  border: 1px solid #e8eaec;
  border-radius: 16px 16px 16px 4px;
  overflow: hidden;
}

.loading-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px;
  color: #666;
}

.ai-content {
  padding: 16px;
}

.text-content {
  color: #333;
  line-height: 1.6;
  word-wrap: break-word;
}

/* 结构化数据显示 */
.structured-data {
  margin-bottom: 12px;
}

.structured-data h4 {
  margin: 0 0 16px;
  font-size: 16px;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 8px;
}

/* 学习统计显示 */
.stats-display .stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.stat-card {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

/* 推荐列表 */
.recommendation-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommendation-item {
  background: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
  border-left: 4px solid #52c41a;
  margin-bottom: 12px;
}

.rec-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.rec-title {
  font-weight: 500;
  color: #333;
  flex: 1;
}

.rec-desc {
  margin: 0;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

/* 职业规划时间线 */
.career-timeline {
  position: relative;
  padding-left: 24px;
}

.timeline-item {
  position: relative;
  margin-bottom: 24px;
}

.timeline-marker {
  position: absolute;
  left: -28px;
  top: 4px;
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
}

.timeline-marker::before {
  content: '';
  position: absolute;
  left: 3px;
  top: 8px;
  width: 2px;
  height: 40px;
  background: #e8eaec;
}

.timeline-item:last-child .timeline-marker::before {
  display: none;
}

.timeline-content h5 {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.phase-duration {
  margin: 0 0 8px;
  font-size: 12px;
  color: #666;
}

.phase-goals {
  margin: 0;
  padding-left: 16px;
  color: #555;
}

.phase-goals li {
  margin-bottom: 4px;
  font-size: 14px;
  line-height: 1.4;
}

/* 预警显示 */
.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  padding: 12px;
  border-radius: 8px;
  border-left: 4px solid #faad14;
  background: #fffbf0;
  margin-bottom: 12px;
}

.alert-item.alert-high {
  border-left-color: #ff4d4f;
  background: #fff2f0;
}

.alert-item.alert-medium {
  border-left-color: #faad14;
  background: #fffbf0;
}

.alert-item.alert-low {
  border-left-color: #1890ff;
  background: #f6ffed;
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.alert-title {
  font-weight: 500;
  color: #333;
  flex: 1;
}

.alert-desc {
  margin: 0 0 12px;
  color: #666;
  line-height: 1.4;
}

.alert-suggestions {
  color: #555;
}

.alert-suggestions strong {
  color: #333;
}

.alert-suggestions ul {
  margin: 4px 0 0;
  padding-left: 16px;
}

.alert-suggestions li {
  margin-bottom: 4px;
  line-height: 1.4;
}

/* 消息操作 */
.message-actions {
  display: flex;
  gap: 8px;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.message-item:hover .message-actions {
  opacity: 1;
}

.message-user .message-actions {
  justify-content: flex-end;
}

/* 输入区域 */
.chat-input {
  background: white;
  border-top: 1px solid #e8eaec;
  padding: 16px 24px;
}

.input-container {
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

.input-tips {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.tip-text {
  display: flex;
  align-items: center;
  gap: 4px;
}

.char-count {
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .portrait-chat {
    height: 100vh;
  }
  
  .chat-header {
    padding: 12px 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .quick-actions {
    padding: 12px 16px;
  }
  
  .action-buttons {
    gap: 6px;
  }
  
  .chat-messages {
    padding: 16px;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .message-user .message-content {
    max-width: fit-content;
    min-width: 100px;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .chat-input {
    padding: 12px 16px;
  }
  
  .input-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .input-tips {
    flex-direction: column;
    gap: 4px;
    align-items: flex-start;
  }
}

/* 滚动条样式 */
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 动画效果 */
.message-item {
  animation: fadeInUp 0.3s ease-out;
}

/* 格式化文本样式 */
.formatted-text {
  line-height: 1.6;
}

.formatted-text .section-title {
  margin: 16px 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  border-left: 4px solid #667eea;
  padding-left: 12px;
}

.formatted-text .formatted-list {
  margin: 12px 0;
  padding-left: 0;
  list-style: none;
}

.formatted-text .list-item {
  margin: 8px 0;
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 6px;
  border-left: 3px solid #667eea;
  position: relative;
}

.formatted-text .list-item::before {
  content: '•';
  color: #667eea;
  font-weight: bold;
  position: absolute;
  left: -8px;
  top: 8px;
}

.formatted-text .sub-formatted-list {
  margin: 8px 0 8px 16px;
  padding-left: 0;
  list-style: none;
}

.formatted-text .sub-list-item {
  margin: 4px 0;
  padding: 6px 10px;
  background: #f0f2f5;
  border-radius: 4px;
  border-left: 2px solid #a0a8b8;
  font-size: 14px;
}

.formatted-text .sub-list-item::before {
  content: '◦';
  color: #a0a8b8;
  font-weight: bold;
  margin-right: 6px;
}

.formatted-text strong {
  color: #333;
  font-weight: 600;
}

.formatted-text br {
  line-height: 1.8;
}

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

/* 加载动画 */
.loading-message {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
</style>