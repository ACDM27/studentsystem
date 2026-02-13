/**
 * AI Chat Store Module
 * 管理AI对话的全局状态，包括会话ID、消息历史、展开状态等
 */

import { Module } from 'vuex'

export interface Message {
    id: string
    type: 'user' | 'ai'
    content: string
    timestamp: Date
    loading?: boolean
}

export interface AiChatState {
    sessionId: string | null
    messages: Message[]
    isExpanded: boolean
    isSending: boolean
    userName: string
}

const STORAGE_KEY_SESSION = 'ai_chat_session_id'
const STORAGE_KEY_MESSAGES = 'ai_chat_messages'
const STORAGE_KEY_EXPANDED = 'ai_chat_expanded'

const aiChatModule: Module<AiChatState, any> = {
    namespaced: true,

    state: (): AiChatState => ({
        sessionId: null,
        messages: [],
        isExpanded: false,
        isSending: false,
        userName: '同学'
    }),

    getters: {
        // 获取显示的消息（最近5条）
        displayMessages: (state) => {
            return state.messages.slice(-5)
        },

        // 连接状态
        connectionStatus: (state) => {
            return state.isSending ? '正在回复...' : '在线'
        },

        // 消息总数
        messageCount: (state) => {
            return state.messages.length
        },

        // 是否有对话历史
        hasHistory: (state) => {
            return state.messages.length > 0
        }
    },

    mutations: {
        // 设置SessionID
        SET_SESSION_ID(state, sessionId: string) {
            console.log('[AI Chat Store] SET_SESSION_ID:', sessionId)
            state.sessionId = sessionId
        },

        // 添加消息
        ADD_MESSAGE(state, message: Message) {
            console.log('[AI Chat Store] ADD_MESSAGE:', message)
            state.messages.push(message)
        },

        // 更新消息
        UPDATE_MESSAGE(state, { id, updates }: { id: string; updates: Partial<Message> }) {
            const index = state.messages.findIndex(msg => msg.id === id)
            if (index !== -1) {
                console.log('[AI Chat Store] UPDATE_MESSAGE:', id, updates)
                state.messages[index] = { ...state.messages[index], ...updates }
            }
        },

        // 设置所有消息
        SET_MESSAGES(state, messages: Message[]) {
            console.log('[AI Chat Store] SET_MESSAGES:', messages.length, 'messages')
            state.messages = messages
        },

        // 清除所有消息
        CLEAR_MESSAGES(state) {
            console.log('[AI Chat Store] CLEAR_MESSAGES')
            state.messages = []
        },

        // 设置展开状态
        SET_EXPANDED(state, isExpanded: boolean) {
            console.log('[AI Chat Store] SET_EXPANDED:', isExpanded)
            state.isExpanded = isExpanded
        },

        // 切换展开状态
        TOGGLE_EXPANDED(state) {
            state.isExpanded = !state.isExpanded
            console.log('[AI Chat Store] TOGGLE_EXPANDED:', state.isExpanded)
        },

        // 设置发送状态
        SET_SENDING(state, isSending: boolean) {
            state.isSending = isSending
        },

        // 设置用户名
        SET_USER_NAME(state, userName: string) {
            console.log('[AI Chat Store] SET_USER_NAME:', userName)
            state.userName = userName
        }
    },

    actions: {
        // 从LocalStorage加载状态
        loadFromStorage({ commit, state }) {
            console.log('[AI Chat Store] Loading from localStorage...')

            try {
                // 加载SessionID
                const savedSessionId = localStorage.getItem(STORAGE_KEY_SESSION)
                if (savedSessionId) {
                    commit('SET_SESSION_ID', savedSessionId)
                }

                // 加载消息
                const savedMessages = localStorage.getItem(STORAGE_KEY_MESSAGES)
                if (savedMessages) {
                    const parsed = JSON.parse(savedMessages)
                    const messages = parsed.map((msg: any) => ({
                        ...msg,
                        timestamp: new Date(msg.timestamp)
                    }))
                    commit('SET_MESSAGES', messages)
                }

                // 加载展开状态（可选）
                const savedExpanded = localStorage.getItem(STORAGE_KEY_EXPANDED)
                if (savedExpanded === 'true') {
                    commit('SET_EXPANDED', true)
                }

                console.log('[AI Chat Store] Loaded state:', {
                    sessionId: state.sessionId,
                    messageCount: state.messages.length
                })
            } catch (error) {
                console.error('[AI Chat Store] 加载状态失败:', error)
            }
        },

        // 保存到LocalStorage
        saveToStorage({ state }) {
            console.log('[AI Chat Store] Saving to localStorage...')

            try {
                // 保存SessionID
                if (state.sessionId) {
                    localStorage.setItem(STORAGE_KEY_SESSION, state.sessionId)
                }

                // 保存消息（排除loading状态）
                const messagesToSave = state.messages
                    .filter(msg => !msg.loading)
                    .map(msg => ({
                        ...msg,
                        timestamp: msg.timestamp.toISOString()
                    }))
                localStorage.setItem(STORAGE_KEY_MESSAGES, JSON.stringify(messagesToSave))

                // 保存展开状态
                localStorage.setItem(STORAGE_KEY_EXPANDED, String(state.isExpanded))

                console.log('[AI Chat Store] Saved:', {
                    sessionId: state.sessionId,
                    messageCount: messagesToSave.length
                })
            } catch (error) {
                console.error('[AI Chat Store] 保存状态失败:', error)
            }
        },

        // 清除存储
        clearStorage({ commit }) {
            console.log('[AI Chat Store] Clearing storage...')

            try {
                localStorage.removeItem(STORAGE_KEY_SESSION)
                localStorage.removeItem(STORAGE_KEY_MESSAGES)
                localStorage.removeItem(STORAGE_KEY_EXPANDED)

                commit('SET_SESSION_ID', null)
                commit('CLEAR_MESSAGES')
                commit('SET_EXPANDED', false)

                console.log('[AI Chat Store] Storage cleared')
            } catch (error) {
                console.error('[AI Chat Store] 清除存储失败:', error)
            }
        },

        // 发送消息
        async sendMessage({ commit, state, dispatch }, { message, chatWithAI }: { message: string; chatWithAI: any }) {
            console.log('[AI Chat Store] Sending message:', message)

            // 生成消息ID
            const generateId = () => Date.now().toString(36) + Math.random().toString(36).substr(2)

            // 添加用户消息
            const userMsg: Message = {
                id: generateId(),
                type: 'user',
                content: message,
                timestamp: new Date()
            }
            commit('ADD_MESSAGE', userMsg)

            // 添加AI消息占位符
            const aiMsgId = generateId()
            const aiMsg: Message = {
                id: aiMsgId,
                type: 'ai',
                content: '',
                timestamp: new Date(),
                loading: true
            }
            commit('ADD_MESSAGE', aiMsg)

            // 设置发送状态
            commit('SET_SENDING', true)

            try {
                // 调用API
                const response = await chatWithAI({
                    message: message,
                    session_id: state.sessionId
                })

                // 更新SessionID
                if (response.session_id) {
                    commit('SET_SESSION_ID', response.session_id)
                }

                // 更新AI消息
                commit('UPDATE_MESSAGE', {
                    id: aiMsgId,
                    updates: {
                        content: response.message || '抱歉，暂时无法获取回复。',
                        loading: false
                    }
                })

                // 保存到LocalStorage
                dispatch('saveToStorage')

                return response
            } catch (error) {
                console.error('[AI Chat Store] 发送消息失败:', error)

                // 更新AI消息为错误状态
                commit('UPDATE_MESSAGE', {
                    id: aiMsgId,
                    updates: {
                        content: '抱歉，AI助手暂时无法回复，请稍后再试。',
                        loading: false
                    }
                })

                throw error
            } finally {
                commit('SET_SENDING', false)
            }
        }
    }
}

export default aiChatModule
