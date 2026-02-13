<template>
  <div class="floating-ai-assistant">
    <!-- 折叠按钮 -->
    <Transition name="slide-fade">
      <div
        v-if="!isExpanded"
        class="collapse-btn"
        @click="toggleExpand"
        :title="'AI学习助手'"
      >
        <n-icon size="28" class="assistant-icon">
          <IconMessageCircle />
        </n-icon>
        <span class="assistant-label">AI助手</span>
      </div>
    </Transition>

    <!-- 展开的对话面板 -->
    <Transition name="slide-in">
      <div v-if="isExpanded" class="chat-panel">
        <!-- 头部 -->
        <div class="panel-header">
          <div class="header-left">
            <n-icon size="24" class="header-icon">
              <IconMessageCircle />
            </n-icon>
            <div class="header-info">
              <h3 class="header-title">AI学习助手</h3>
              <p class="header-status">{{ connectionStatus }}</p>
            </div>
          </div>
          <div class="header-actions">
            <n-button
              size="small"
              text
              @click="navigateToFullChat"
              title="查看完整对话"
            >
              <template #icon>
                <n-icon><IconExternalLink /></n-icon>
              </template>
            </n-button>
            <n-button
              size="small"
              text
              @click="toggleExpand"
              title="折叠"
            >
              <template #icon>
                <n-icon><IconX /></n-icon>
              </template>
            </n-button>
          </div>
        </div>

        <!-- 消息区域 -->
        <div class="messages-container" ref="messagesContainer">
          <!-- 欢迎消息 -->
          <div v-if="messageCount === 0" class="welcome-box">
            <n-icon size="40" class="welcome-icon">
              <IconMessageCircle />
            </n-icon>
            <p class="welcome-text">您好！我是AI学习助手</p>
            <p class="welcome-hint">我可以帮您分析学习成果、提供建议</p>
          </div>

          <!-- 消息列表（只显示最近5条） -->
          <div
            v-for="msg in displayMessages"
            :key="msg.id"
            class="message-item"
            :class="`message-${msg.type}`"
          >
            <div class="message-avatar">
              <n-avatar v-if="msg.type === 'user'" size="small" class="user-avatar">
                {{ userName.charAt(0) }}
              </n-avatar>
              <n-icon v-else size="20" class="ai-avatar">
                <IconMessageCircle />
              </n-icon>
            </div>
            <div class="message-bubble">
              <div v-if="msg.loading" class="loading-indicator">
                <n-spin size="small" />
                <span>思考中...</span>
              </div>
              <div v-else class="message-text" v-html="formatMessage(msg.content)"></div>
            </div>
          </div>

          <!-- 历史消息提示 -->
          <div v-if="messageCount > 5" class="more-messages-hint">
            <n-button text size="tiny" @click="navigateToFullChat">
              <template #icon>
                <n-icon><IconExternalLink /></n-icon>
              </template>
              查看完整对话历史（{{ messageCount }} 条消息）
            </n-button>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-area">
          <n-input
            v-model:value="inputMessage"
            type="textarea"
            placeholder="输入您的问题..."
            :autosize="{ minRows: 1, maxRows: 3 }"
            :disabled="isSending"
            @keydown.enter.prevent="handleEnterKey"
            class="message-input"
          />
          <n-button
            type="primary"
            :loading="isSending"
            :disabled="!inputMessage.trim()"
            @click="sendMessage"
            class="send-btn"
          >
            <template #icon>
              <n-icon><IconSend /></n-icon>
            </template>
          </n-button>
        </div>

        <!-- 快捷操作 -->
        <div class="quick-actions">
          <n-button
            size="tiny"
            text
            @click="sendQuickQuestion('请分析我的学习成果')"
          >
            📊 学习成果
          </n-button>
          <n-button
            size="tiny"
            text
            @click="sendQuickQuestion('为我推荐学习内容')"
          >
            💡 学习推荐
          </n-button>
          <n-button
            size="tiny"
            text
            @click="sendQuickQuestion('分析我的学情预警')"
          >
            ⚠️ 学情预警
          </n-button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { NIcon, NButton, NInput, NAvatar, NSpin, useMessage } from 'naive-ui'
import {
  IconMessageCircle,
  IconX,
  IconSend,
  IconExternalLink
} from '@/utils/icons'
import { chatWithAI, getStudentMe } from '@/api'

// Router & Store
const router = useRouter()
const store = useStore()
const message = useMessage()

// Local state (仅UI相关)
const inputMessage = ref('')
const messagesContainer = ref<HTMLElement>()

// 从Store获取状态（使用computed保持响应性）
const isExpanded = computed(() => store.state.aiChat.isExpanded)
const isSending = computed(() => store.state.aiChat.isSending)
const userName = computed(() => store.state.aiChat.userName)
const sessionId = computed(() => store.state.aiChat.sessionId)
const displayMessages = computed(() => store.getters['aiChat/displayMessages'])
const connectionStatus = computed(() => store.getters['aiChat/connectionStatus'])
const messageCount = computed(() => store.getters['aiChat/messageCount'])

// Methods
const toggleExpand = () => {
  store.commit('aiChat/TOGGLE_EXPANDED')
  nextTick(() => {
    scrollToBottom()
  })
}

const sendQuickQuestion = (question: string) => {
  inputMessage.value = question
  sendMessage()
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isSending.value) return

  const userInput = inputMessage.value
  inputMessage.value = ''

  await scrollToBottom()

  try {
    // 使用Store的sendMessage action
    await store.dispatch('aiChat/sendMessage', {
      message: userInput,
      chatWithAI
    })
  } catch (error) {
    console.error('AI对话失败:', error)
    message.error('发送失败')
  } finally {
    await scrollToBottom()
  }
}

const handleEnterKey = (event: KeyboardEvent) => {
  if (event.ctrlKey || event.metaKey) {
    sendMessage()
  }
}

const navigateToFullChat = () => {
  // 跳转到完整的对话页面
  router.push({
    name: 'studentPortraitChat',
    query: {
      session_id: sessionId.value || undefined
    }
  })
}

const scrollToBottom = async () => {
  await nextTick()
  const el = messagesContainer.value
  if (!el) return
  el.scrollTop = el.scrollHeight
}

const formatMessage = (content: string): string => {
  // 简单的格式化
  let formatted = content.replace(/\n/g, '<br>')
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  return formatted
}

// Initialize
onMounted(async () => {
  console.log('[FloatingAiAssistant] Component mounted')
  
  // 从Store加载状态
  await store.dispatch('aiChat/loadFromStorage')
  
  // 获取用户信息
  try {
    const userInfo = await getStudentMe()
    store.commit('aiChat/SET_USER_NAME', userInfo.name || userInfo.username || '同学')
  } catch (err) {
    console.warn('获取用户信息失败:', err)
  }
  
  console.log('[FloatingAiAssistant] Initialization complete')
})
</script>

<style scoped>
.floating-ai-assistant {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 9998;
}

/* 折叠按钮 */
.collapse-btn {
  position: relative;
  right: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 12px;
  border-radius: 12px 0 0 12px;
  cursor: pointer;
  box-shadow: -2px 4px 12px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 60px;
}

.collapse-btn:hover {
  background: linear-gradient(135deg, #7289ea 0%, #8659b5 100%);
  box-shadow: -4px 6px 16px rgba(102, 126, 234, 0.4);
  transform: translateX(-4px);
}

.assistant-icon {
  animation: pulse 2s infinite;
}

.assistant-label {
  font-size: 12px;
  font-weight: 500;
  writing-mode: vertical-rl;
  letter-spacing: 2px;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* 对话面板 */
.chat-panel {
  position: relative;
  right: 0;
  width: 380px;
  height: 600px;
  max-height: 80vh;
  background: white;
  border-radius: 16px 0 0 16px;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 头部 */
.panel-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-radius: 16px 0 0 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  color: white;
}

.header-info {
  display: flex;
  flex-direction: column;
}

.header-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.header-status {
  margin: 0;
  font-size: 12px;
  opacity: 0.9;
}

.header-actions {
  display: flex;
  gap: 4px;
}

.header-actions :deep(.n-button) {
  color: white !important;
}

/* 消息区域 */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f5f7fa;
  scroll-behavior: smooth;
}

.welcome-box {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.welcome-icon {
  color: #667eea;
  margin-bottom: 12px;
}

.welcome-text {
  font-size: 16px;
  font-weight: 500;
  margin: 8px 0;
  color: #333;
}

.welcome-hint {
  font-size: 14px;
  margin: 4px 0;
}

/* 消息项 */
.message-item {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.ai-avatar {
  background: #e8eaec;
  color: #667eea;
  padding: 6px;
  border-radius: 50%;
}

.message-bubble {
  max-width: 75%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
}

.message-user .message-bubble {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px 12px 0 12px;
}

.message-ai .message-bubble {
  background: white;
  color: #333;
  border-radius: 12px 12px 12px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
}

.message-text {
  word-break: break-word;
}

.more-messages-hint {
  text-align: center;
  padding: 8px;
  margin-top: 8px;
}

/* 输入区域 */
.input-area {
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #e8eaec;
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

.message-input {
  flex: 1;
}

.send-btn {
  flex-shrink: 0;
}

/* 快捷操作 */
.quick-actions {
  padding: 8px 16px 12px;
  background: white;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  border-top: 1px solid #f0f0f0;
}

.quick-actions :deep(.n-button) {
  font-size: 12px;
}

/* 过渡动画 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.slide-in-enter-active,
.slide-in-leave-active {
  transition: all 0.3s ease;
}

.slide-in-enter-from,
.slide-in-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-panel {
    width: 100vw;
    height: 100vh;
    max-height: 100vh;
    border-radius: 0;
    right: 0;
    top: 0 !important;
    transform: none !important;
  }

  .panel-header {
    border-radius: 0;
  }
}

/* 滚动条样式 */
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.messages-container::-webkit-scrollbar-thumb {
  background: #d0d0d0;
  border-radius: 3px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: #b0b0b0;
}
</style>
