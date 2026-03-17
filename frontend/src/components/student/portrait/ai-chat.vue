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
      <div class="header-actions">
        <n-space>
          <n-button quaternary size="small" @click="startNewChat">
            <template #icon>
              <n-icon><IconPlus /></n-icon>
            </template>
            开启新对话
          </n-button>
          <n-button quaternary circle @click="show_history = true">
            <template #icon>
              <n-icon size="20"><IconHistory /></n-icon>
            </template>
          </n-button>
        </n-space>
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
<!-- 历史对话查询弹窗 (Claude Code 风格) -->
    <n-modal
      v-model:show="show_history"
      preset="card"
      style="width: 600px; max-width: 90vw;"
      title="对话历史"
      :bordered="false"
      size="huge"
    >
      <div class="history-search">
        <n-input
          v-model:value="search_keyword"
          placeholder="搜索消息内容..."
          clearable
        >
          <template #prefix>
            <n-icon><IconSearch /></n-icon>
          </template>
        </n-input>
      </div>
      
      <div class="history-list-wrapper">
        <n-scrollbar style="max-height: 400px;">
          <n-list hoverable clickable>
            <n-empty v-if="filtered_history.length === 0" description="暂无匹配的历史记录" />
            <n-list-item
              v-for="msg in filtered_history"
              :key="msg.id"
              class="history-item"
            >
              <div class="history-item-content">
                <div class="history-item-header">
                  <span class="history-item-time">{{ formatSimpleDate(msg.timestamp) }}</span>
                </div>
                <div class="history-item-text">{{ msg.content }}</div>
              </div>
            </n-list-item>
          </n-list>
        </n-scrollbar>
      </div>
      
      <div class="history-footer">
        <n-button secondary type="error" size="small" @click="clearHistory">
          <template #icon>
            <n-icon><IconTrash /></n-icon>
          </template>
          清除当前历史
        </n-button>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { NIcon, NScrollbar, NAvatar, NTag, NSpin, NSpace, NButton, NInput, useMessage, NModal, NList, NListItem, NEmpty } from 'naive-ui'
import {
  IconMessageCircle,
  IconUser,
  IconChartBar,
  IconAward,
  IconHelpCircle,
  IconHistory,
  IconSearch,
  IconTrash,
  IconPlus
} from '../../../utils/icons'
import {
  chatWithAI,
  getStudentMe as fetchStudentMe
} from '@/api'

// 消息接口定义
interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

// 响应式数据
const store = useStore()
const message = useMessage()

// 映射 Vuex 状态
const msg_list = computed(() => {
  // 过滤逻辑：保留用户消息，以及内容不为空或正在加载中的 AI 消息
  return store.state.aiChat.messages
    .filter((msg: any) => {
      if (msg.type === 'user') return true
      return msg.loading || (msg.content && msg.content.trim() !== '')
    })
    .map((msg: any) => ({
      role: msg.type === 'user' ? 'user' : 'assistant',
      content: msg.content,
      timestamp: msg.timestamp,
      loading: msg.loading
    }))
})
const session_id = computed(() => store.state.aiChat.sessionId)
const is_loading = computed(() => store.state.aiChat.isSending)

const input_msg = ref('')
const user_name = ref('学生')
const msg_container = ref<HTMLElement>()

// 历史记录查询弹窗
const show_history = ref(false)
const search_keyword = ref('')
const filtered_history = computed(() => {
  // 仅显示用户的问题
  const userMessages = store.state.aiChat.messages.filter((msg: any) => msg.type === 'user')
  if (!search_keyword.value.trim()) return userMessages
  return userMessages.filter((msg: any) => 
    msg.content.includes(search_keyword.value)
  )
})

// 学生数据
const student_id = ref<string>('')
// 已整合到 computed session_id

// 组件挂载时初始化
onMounted(async () => {
  // 加载本地存储的对话
  await store.dispatch('aiChat/loadFromStorage')
  await initializeUser()
  nextTick(() => {
    scrollToBottom()
  })
})

// 初始化用户信息
const initializeUser = async () => {
  try {
    // 响应拦截器已解包，返回值即为 data 对象
    const data = await fetchStudentMe() as any
    if (data) {
      const studentId = data.student_id || data.id
      if (studentId) {
        student_id.value = studentId.toString()
        user_name.value = data.name || data.username || '学生'
      } else {
        throw new Error('无法获取学生身份信息')
      }
    } else {
      throw new Error('无法获取用户信息')
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    message.error('无法获取学生身份信息，请重新登录')
    student_id.value = ''
    user_name.value = ''
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
  input_msg.value = ''

  try {
    await store.dispatch('aiChat/sendMessage', {
      message: user_message,
      chatWithAI
    })
    nextTick(() => {
      scrollToBottom()
    })
  } catch (error: any) {
    console.error('发送消息失败:', error)
    const errorMessage = error.response?.status === 404 
      ? '抱歉，AI聊天服务接口未找到。' 
      : '抱歉，发送消息时出错，请重试。'
    message.error(errorMessage)
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

// 开启新对话
const startNewChat = () => {
  store.dispatch('aiChat/resetSession')
  message.success('已开启新会话')
}

// 清除历史
const clearHistory = () => {
  store.dispatch('aiChat/clearStorage')
  show_history.value = false
  message.success('历史记录已清除')
}

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

// 格式化历史记录日期 (年-月-日)
const formatSimpleDate = (timestamp: Date): string => {
  const d = new Date(timestamp)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
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
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  max-width: 85%;
}

.message-bubble {
  background: white;
  border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  width: fit-content;
  max-width: 100%;
}

.is-user .message-bubble {
  background: #409eff;
  color: white;
  margin-left: auto;
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

/* 历史查询样式 */
.history-search {
  margin-bottom: 16px;
}

.history-list-wrapper {
  margin: 16px 0;
}

.history-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.history-item-time {
  font-size: 12px;
  color: #909399;
}

.history-item-text {
  font-size: 14px;
  color: #606266;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.history-footer {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
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