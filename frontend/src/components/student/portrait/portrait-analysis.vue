<template>
  <div class="portrait-analysis">
    <!-- 新的顶部设计区域 -->
    <div class="top-dashboard">
      <!-- 个人信息卡片 -->
      <n-card class="personal-info-card" hoverable>
        <template #header>
          <div class="card-header">
            <span class="header-title">个人信息</span>
            <n-icon :size="16" class="expand-icon">
              <IconChevronRight />
            </n-icon>
          </div>
        </template>
        
        <div class="personal-content">
          <div class="avatar-section">
            <n-avatar :size="80" :src="student_avatar" class="main-avatar">
              {{ student_name.charAt(0) }}
            </n-avatar>
          </div>
          <div class="info-section">
            <div class="basic-info">
              <div class="name-row">
                <span class="label">姓名</span>
                <span class="value">{{ student_name }}</span>
              </div>
              <div class="info-row">
                <span class="label">性别</span>
                <span class="value">男</span>
              </div>
              <div class="info-row">
                <span class="label">院系</span>
                <span class="value">信息技术学院</span>
              </div>
            </div>
            <div class="contact-info">
              <div class="contact-row">
                <span class="label">邮件地址</span>
                <span class="value">luomeihui@daed.edu</span>
              </div>
              <div class="contact-row">
                <span class="label">身份人员</span>
                <span class="value">学生</span>
              </div>
            </div>
          </div>
        </div>
      </n-card>

      <!-- 个人综合评价卡片 -->
      <n-card class="comprehensive-evaluation-card" hoverable>
        <template #header>
          <div class="card-header">
            <span class="header-title">个人综合评价</span>
            <div class="evaluation-tip">
              <span class="tip-text">点击查看个人综合评价详细方案</span>
            </div>
            <n-icon :size="16" class="expand-icon">
              <IconChevronRight />
            </n-icon>
          </div>
        </template>
        
        <div class="evaluation-content">
          <div class="radar-chart-container">
            <!-- 雷达图展示区域 -->
            <div class="radar-chart">
              <svg width="200" height="200" viewBox="0 0 200 200">
                <!-- 雷达图背景网格 -->
                <g class="radar-grid">
                  <polygon points="100,20 150,50 150,150 100,180 50,150 50,50" fill="none" stroke="#e0e0e0" stroke-width="1"/>
                  <polygon points="100,35 135,57.5 135,142.5 100,165 65,142.5 65,57.5" fill="none" stroke="#e0e0e0" stroke-width="1"/>
                  <polygon points="100,50 120,65 120,135 100,150 80,135 80,65" fill="none" stroke="#e0e0e0" stroke-width="1"/>
                  <polygon points="100,65 105,72.5 105,127.5 100,135 95,127.5 95,72.5" fill="none" stroke="#e0e0e0" stroke-width="1"/>
                  <!-- 雷达图轴线 -->
                  <line x1="100" y1="100" x2="100" y2="20" stroke="#e0e0e0" stroke-width="1"/>
                  <line x1="100" y1="100" x2="150" y2="50" stroke="#e0e0e0" stroke-width="1"/>
                  <line x1="100" y1="100" x2="150" y2="150" stroke="#e0e0e0" stroke-width="1"/>
                  <line x1="100" y1="100" x2="100" y2="180" stroke="#e0e0e0" stroke-width="1"/>
                  <line x1="100" y1="100" x2="50" y2="150" stroke="#e0e0e0" stroke-width="1"/>
                  <line x1="100" y1="100" x2="50" y2="50" stroke="#e0e0e0" stroke-width="1"/>
                </g>
                <!-- 数据多边形 -->
                <polygon points="100,30 140,60 130,140 100,160 70,130 80,70" fill="rgba(24, 160, 88, 0.3)" stroke="#18a058" stroke-width="2"/>
                <!-- 数据点 -->
                <circle cx="100" cy="30" r="3" fill="#18a058"/>
                <circle cx="140" cy="60" r="3" fill="#18a058"/>
                <circle cx="130" cy="140" r="3" fill="#18a058"/>
                <circle cx="100" cy="160" r="3" fill="#18a058"/>
                <circle cx="70" cy="130" r="3" fill="#18a058"/>
                <circle cx="80" cy="70" r="3" fill="#18a058"/>
              </svg>
            </div>
            <!-- 评价维度标签 -->
            <div class="evaluation-labels">
              <div class="label-item top">竞赛 ({{ achievementData.competition }})</div>
              <div class="label-item top-right">科研 ({{ achievementData.research }})</div>
              <div class="label-item bottom-right">项目 ({{ achievementData.project }})</div>
              <div class="label-item bottom">论文 ({{ achievementData.paper }})</div>
              <div class="label-item bottom-left">专利 ({{ achievementData.patent }})</div>
              <div class="label-item top-left">证书 ({{ achievementData.certificate }})</div>
            </div>
          </div>
          <div class="evaluation-details">
            <div class="detail-item">
              <span class="detail-label">综合评分</span>
              <span class="detail-value">{{ aiAnalysisData.comprehensiveScore || '分析中...' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">排名</span>
              <span class="detail-value">{{ aiAnalysisData.ranking || '分析中...' }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">优势领域</span>
              <span class="detail-value">{{ aiAnalysisData.strengthArea || '分析中...' }}</span>
            </div>
          </div>
        </div>
      </n-card>

      <!-- 学分完成情况卡片 -->
      <n-card class="credit-progress-card" hoverable>
        <template #header>
          <div class="card-header">
            <span class="header-title">学分完成情况</span>
            <n-icon :size="16" class="expand-icon">
              <IconChevronRight />
            </n-icon>
          </div>
        </template>
        
        <div class="credit-content">
          <div class="credit-chart">
            <div class="circular-progress">
              <svg width="120" height="120" viewBox="0 0 120 120">
                <circle cx="60" cy="60" r="50" fill="none" stroke="#f0f0f0" stroke-width="8"/>
                <circle cx="60" cy="60" r="50" fill="none" stroke="#18a058" stroke-width="8" 
                        stroke-dasharray="220" stroke-dashoffset="66" 
                        stroke-linecap="round" transform="rotate(-90 60 60)"/>
                <text x="60" y="55" text-anchor="middle" class="credit-number">47.5</text>
                <text x="60" y="70" text-anchor="middle" class="credit-total">/170</text>
                <text x="60" y="85" text-anchor="middle" class="credit-label">CREDITS</text>
              </svg>
            </div>
          </div>
          <div class="credit-breakdown">
            <div class="breakdown-item">
              <div class="item-color" style="background-color: #18a058;"></div>
              <span class="item-label">已完成</span>
            </div>
            <div class="breakdown-item">
              <div class="item-color" style="background-color: #f0a020;"></div>
              <span class="item-label">进行中</span>
            </div>
            <div class="breakdown-item">
              <div class="item-color" style="background-color: #d03050;"></div>
              <span class="item-label">未开始</span>
            </div>
            <div class="breakdown-item">
              <div class="item-color" style="background-color: #2080f0;"></div>
              <span class="item-label">大类课程</span>
            </div>
            <div class="breakdown-item">
              <div class="item-color" style="background-color: #722ed1;"></div>
              <span class="item-label">专业课程</span>
            </div>
          </div>
        </div>
      </n-card>

      <!-- 专业核心能力结构卡片 -->
      <n-card class="core-ability-card" hoverable>
        <template #header>
          <div class="card-header">
            <span class="header-title">专业核心能力结构</span>
            <n-icon :size="16" class="expand-icon">
              <IconChevronRight />
            </n-icon>
          </div>
        </template>
        
        <div class="ability-content">
          <div class="ability-chart">
            <!-- 菱形能力结构图 -->
            <svg width="200" height="200" viewBox="0 0 200 200">
              <!-- 背景菱形 -->
              <polygon points="100,20 170,100 100,180 30,100" fill="#f8f9fa" stroke="#e0e0e0" stroke-width="1"/>
              <!-- 能力区域 -->
              <polygon points="100,40 150,100 100,160 50,100" fill="rgba(24, 160, 88, 0.2)" stroke="#18a058" stroke-width="2"/>
              <!-- 中心点 -->
              <circle cx="100" cy="100" r="8" fill="#18a058"/>
              <!-- 能力点 -->
              <circle cx="100" cy="40" r="4" fill="#18a058"/>
              <circle cx="150" cy="100" r="4" fill="#18a058"/>
              <circle cx="100" cy="160" r="4" fill="#18a058"/>
              <circle cx="50" cy="100" r="4" fill="#18a058"/>
            </svg>
            <!-- 能力标签 -->
            <div class="ability-labels">
              <div class="ability-label top">会计核心能力运用能力</div>
              <div class="ability-label right">会计理论知识运用能力</div>
              <div class="ability-label bottom">数据整理运用分析能力</div>
              <div class="ability-label left">企业决策的预测分析能力</div>
            </div>
          </div>
          <div class="ability-details">
            <div class="ability-item">
              <span class="ability-name">核心能力</span>
              <div class="ability-bar">
                <div class="bar-fill" style="width: 85%;"></div>
              </div>
              <span class="ability-score">85%</span>
            </div>
            <div class="ability-item">
              <span class="ability-name">理论运用</span>
              <div class="ability-bar">
                <div class="bar-fill" style="width: 78%;"></div>
              </div>
              <span class="ability-score">78%</span>
            </div>
            <div class="ability-item">
              <span class="ability-name">数据分析</span>
              <div class="ability-bar">
                <div class="bar-fill" style="width: 72%;"></div>
              </div>
              <span class="ability-score">72%</span>
            </div>
            <div class="ability-item">
              <span class="ability-name">决策预测</span>
              <div class="ability-bar">
                <div class="bar-fill" style="width: 68%;"></div>
              </div>
              <span class="ability-score">68%</span>
            </div>
          </div>
        </div>
      </n-card>
    </div>

    <!-- 课程成绩分布展示 -->
    <div class="course-performance-section">
      <n-card class="course-performance-card" hoverable>
        <template #header>
          <div class="card-header">
            <span class="header-title">课程成绩分布</span>
            <n-icon :size="16" class="expand-icon">
              <IconChevronRight />
            </n-icon>
          </div>
        </template>
        
        <div class="performance-content">
          <div class="performance-chart">
            <!-- 散点图展示区域 -->
            <svg width="100%" height="300" viewBox="0 0 800 300">
              <!-- 坐标轴 -->
              <line x1="80" y1="250" x2="750" y2="250" stroke="#666" stroke-width="1"/>
              <line x1="80" y1="250" x2="80" y2="50" stroke="#666" stroke-width="1"/>
              
              <!-- Y轴刻度 -->
              <g class="y-axis">
                <line x1="75" y1="250" x2="85" y2="250" stroke="#666"/>
                <text x="70" y="255" text-anchor="end" class="axis-label">60</text>
                <line x1="75" y1="200" x2="85" y2="200" stroke="#666"/>
                <text x="70" y="205" text-anchor="end" class="axis-label">68</text>
                <line x1="75" y1="150" x2="85" y2="150" stroke="#666"/>
                <text x="70" y="155" text-anchor="end" class="axis-label">76</text>
                <line x1="75" y1="100" x2="85" y2="100" stroke="#666"/>
                <text x="70" y="105" text-anchor="end" class="axis-label">84</text>
                <line x1="75" y1="50" x2="85" y2="50" stroke="#666"/>
                <text x="70" y="55" text-anchor="end" class="axis-label">92</text>
                <text x="25" y="150" text-anchor="middle" class="axis-title" transform="rotate(-90 25 150)">100</text>
              </g>
              
              <!-- X轴刻度 -->
              <g class="x-axis">
                <line x1="150" y1="245" x2="150" y2="255" stroke="#666"/>
                <text x="150" y="270" text-anchor="middle" class="axis-label">大一</text>
                <line x1="300" y1="245" x2="300" y2="255" stroke="#666"/>
                <text x="300" y="270" text-anchor="middle" class="axis-label">大二</text>
                <line x1="450" y1="245" x2="450" y2="255" stroke="#666"/>
                <text x="450" y="270" text-anchor="middle" class="axis-label">大三</text>
                <line x1="600" y1="245" x2="600" y2="255" stroke="#666"/>
                <text x="600" y="270" text-anchor="middle" class="axis-label">大四</text>
              </g>
              
              <!-- 散点数据 -->
              <g class="scatter-points">
                <!-- 大一成绩点 -->
                <circle cx="120" cy="120" r="8" fill="#2080f0" opacity="0.7"/>
                <circle cx="140" cy="140" r="6" fill="#2080f0" opacity="0.7"/>
                <circle cx="160" cy="110" r="10" fill="#2080f0" opacity="0.7"/>
                <circle cx="180" cy="130" r="7" fill="#2080f0" opacity="0.7"/>
                
                <!-- 大二成绩点 -->
                <circle cx="250" cy="100" r="9" fill="#f0a020" opacity="0.7"/>
                <circle cx="280" cy="90" r="8" fill="#f0a020" opacity="0.7"/>
                <circle cx="320" cy="110" r="7" fill="#f0a020" opacity="0.7"/>
                <circle cx="340" cy="95" r="10" fill="#f0a020" opacity="0.7"/>
                
                <!-- 大三成绩点 -->
                <circle cx="400" cy="80" r="8" fill="#18a058" opacity="0.7"/>
                <circle cx="430" cy="70" r="9" fill="#18a058" opacity="0.7"/>
                <circle cx="460" cy="85" r="7" fill="#18a058" opacity="0.7"/>
                <circle cx="480" cy="75" r="8" fill="#18a058" opacity="0.7"/>
                
                <!-- 大四成绩点 -->
                <circle cx="550" cy="60" r="10" fill="#722ed1" opacity="0.7"/>
                <circle cx="580" cy="65" r="8" fill="#722ed1" opacity="0.7"/>
                <circle cx="620" cy="55" r="9" fill="#722ed1" opacity="0.7"/>
              </g>
            </svg>
          </div>
          <div class="performance-legend">
            <div class="legend-item">
              <div class="legend-color" style="background-color: #2080f0;"></div>
              <span>大一</span>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #f0a020;"></div>
              <span>大二</span>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #18a058;"></div>
              <span>大三</span>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #722ed1;"></div>
              <span>大四</span>
            </div>
          </div>
        </div>
      </n-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import {
  NCard,
  NIcon,
  NAvatar,
  useMessage
} from 'naive-ui'
import {
  IconUser,
  IconAward,
  IconHeart,
  IconBook,
  IconCode,
  IconMusic,
  IconCamera,
  IconChevronRight
} from '../../../utils/icons'
import {
  getStudentPersona,
  getStudentMe as fetchStudentMe,
  getMyAchievements as fetchAchievements,
  chatWithAI
} from '@/api'

// 接口适配器：旧代码传递了 ID，但新 API 从 Token 获取当前用户画像
const fetchStudentPortraitByStudentId = async (id?: string) => {
  return getStudentPersona()
}

// 未使用的函数 Mock，防止报错
const fetchStudentPortraitById = async (id: string) => { console.warn('未使用'); return null }

// 类型定义
interface SkillData {
  name: string
  level: number
  tags: string[]
  category: string
  description: string
  improvement_suggestions: string[]
}

interface InterestData {
  category: string
  name: string
  score: number
  description: string
  isRecommended: boolean
}

interface RiskAlert {
  id: number
  level: string
  title: string
  description: string
  severity: string
  actions: string[]
  deadline: string
  suggestion: string
  time: string
}

interface LearningSuggestion {
  id: number
  type: string
  title: string
  description: string
  priority: string
  details: string[]
  estimatedTime: string
  difficulty: string
}

interface QAHistory {
  id: number
  question: string
  answer: string
  timestamp: Date
}

// 响应式数据
const student_name = ref<string>('')
const student_avatar = ref<string>('')
const portrait_summary = ref<string>('正在加载学生画像数据...')
const last_update_time = ref<string>('')
const portrait_data = ref<any>(null)
const student_id = ref<string>('')
const message = useMessage()

// 初始化用户信息
const initializeUser = async () => {
  try {
    const userResponse = await fetchStudentMe()
    if (userResponse && userResponse.data) {
      const studentId = userResponse.data.student_id || userResponse.data.id
      if (studentId) {
        student_id.value = studentId.toString()
        student_name.value = userResponse.data.username || userResponse.data.name || '未知用户'
      }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    student_name.value = '未知用户'
    student_id.value = ''
  }
}

// 成果数据
const achievementData = ref({
  competition: 0,
  research: 0,
  project: 0,
  paper: 0,
  patent: 0,
  certificate: 0
})

// AI分析数据
const aiAnalysisData = ref({
  comprehensiveScore: '',  // 综合评分
  ranking: '',            // 排名
  strengthArea: ''        // 优势领域
})

/**
 * 获取AI分析结果
 */
const fetchAIAnalysis = async (): Promise<void> => {
  try {
    if (!student_id.value) {
      await initializeUser()
    }
    const prompt = `[画像分析请求] 请基于我的画像数据返回JSON，包含comprehensiveScore, ranking, strengthArea`
    const resp = await chatWithAI({
      message: prompt,
      session_id: null
    })
    const text = resp.message || ''
    let parsed: any = null
    try {
      parsed = typeof text === 'string' ? JSON.parse(text) : text
    } catch (_) {
      parsed = null
    }
    if (parsed && typeof parsed === 'object') {
      aiAnalysisData.value = {
        comprehensiveScore: parsed.comprehensiveScore?.toString?.() || '',
        ranking: parsed.ranking?.toString?.() || '',
        strengthArea: parsed.strengthArea?.toString?.() || ''
      }
    } else {
      aiAnalysisData.value = {
        comprehensiveScore: '',
        ranking: '',
        strengthArea: (typeof text === 'string' && text) ? text : '分析暂不可用'
      }
    }
  } catch (error) {
    console.error('AI分析失败:', error)
    message.error('AI分析失败，请稍后重试')
  }
}

// 数据定义
const skills_data = ref<SkillData[]>([])
const interests_data = ref<InterestData[]>([])
const risk_alerts = ref<RiskAlert[]>([])
const learning_suggestions = ref<LearningSuggestion[]>([])
const learning_stats = reactive({
  total_hours: 0,
  completed_courses: 0,
  avg_score: 0,
  achievements: 0,
  monthly_progress: 0
})
const recent_qa_history = ref<QAHistory[]>([])

// 组件挂载时加载数据
onMounted(async (): Promise<void> => {
  await loadPortraitData()
  await fetchAIAnalysis()
  await fetchAchievementCounts()
})

/**
 * 加载画像数据
 */
const loadPortraitData = async (): Promise<void> => {
  try {
    await initializeUser()
    const response = await fetchStudentPortraitByStudentId(student_id.value)
    if (response) {
      // 适配新API数据结构到旧UI组件
      // 新API仅返回字符串数组，这里进行简单包装以适配UI
      portrait_data.value = {
        summary: response.summary || '暂无画像摘要',
        updatedAt: new Date().toISOString(),
        skills: (Array.isArray(response.skills) ? response.skills : []).map(s => ({
          name: typeof s === 'string' ? s : '未知技能',
          level: 80, // 默认值
          category: 'tech',
          tags: [],
          description: '',
          improvement_suggestions: []
        })),
        interests: (Array.isArray(response.interests) ? response.interests : []).map(i => ({
          name: typeof i === 'string' ? i : '未知兴趣',
          score: 85,
          category: 'tech',
          description: '',
          isRecommended: false
        })),
        risk_alerts: [],
        qa_history: (Array.isArray(response.recent_activities) ? response.recent_activities : []).map((q, idx) => ({
          id: idx,
          question: q,
          answer: '',
          timestamp: new Date()
        }))
      }
      updateDisplayData()
    }
  } catch (error) {
    console.error('画像数据加载失败:', error)
    message.error('画像数据加载失败，请稍后重试')
  }
}

// 从后端统计成果类型数量
const fetchAchievementCounts = async (): Promise<void> => {
  try {
    const resp = await fetchAchievements()
    // 新 API 直接返回 Achievement[] 数组
    const list = Array.isArray(resp) ? resp : []
    const counts = {
      competition: 0,
      research: 0,
      project: 0,
      paper: 0,
      patent: 0,
      certificate: 0
    }
    for (const item of list) {
      const tRaw = item?.type || ''
      const t = String(tRaw).toLowerCase()
      if (t.includes('竞赛') || t.includes('competition')) counts.competition++
      else if (t.includes('科研') || t.includes('research')) counts.research++
      else if (t.includes('项目') || t.includes('project')) counts.project++
      else if (t.includes('论文') || t.includes('paper')) counts.paper++
      else if (t.includes('专利') || t.includes('patent')) counts.patent++
      else if (t.includes('证书') || t.includes('certificate')) counts.certificate++
    }
    achievementData.value = counts
  } catch (error) {
    console.error('获取成果统计失败:', error)
    // 保持为0并提示错误
    message.error('获取成果统计失败，请稍后重试')
  }
}

/**
 * 更新显示数据
 */
const updateDisplayData = (): void => {
  if (!portrait_data.value) return
  
  const data = portrait_data.value
  portrait_summary.value = data.summary || '暂无画像摘要'
  last_update_time.value = formatTime(new Date(data.updatedAt || data.createdAt))
  
  // 更新技能数据
  if (data.skills && data.skills.length > 0) {
    skills_data.value = data.skills
  }
  
  // 更新兴趣数据
  if (data.interests && data.interests.length > 0) {
    interests_data.value = data.interests
  }
  
  // 更新预警数据
  if (data.risk_alerts && data.risk_alerts.length > 0) {
    risk_alerts.value = data.risk_alerts
  }
  
  // 更新对话历史
  if (data.qa_history && data.qa_history.length > 0) {
    recent_qa_history.value = data.qa_history.slice(-3).reverse()
  }
}

/**
 * 刷新数据
 */
const refreshData = async (): Promise<void> => {
  message.loading('正在刷新数据...', { duration: 1000 })
  await loadPortraitData()
  message.success('数据刷新成功')
}

/**
 * 获取技能颜色
 * @param level 技能等级
 * @returns 颜色值
 */
const getSkillColor = (level: number): string => {
  if (level >= 80) return '#52c41a'
  if (level >= 60) return '#faad14'
  return '#ff4d4f'
}

/**
 * 获取兴趣图标
 * @param category 兴趣类别
 * @returns 图标组件
 */
const getInterestIcon = (category: string) => {
  const iconMap: Record<string, any> = {
    tech: IconCode,
    design: IconCamera,
    music: IconMusic,
    sports: IconHeart, 
    book: IconBook
  }
  return iconMap[category] || IconHeart
}

/**
 * 获取预警标签类型
 * @param level 预警级别
 * @returns 标签类型
 */
const getWarningTagType = (level: string): 'default' | 'info' | 'success' | 'warning' | 'error' | 'primary' => {
  const typeMap: Record<string, 'default' | 'info' | 'success' | 'warning' | 'error' | 'primary'> = {
    high: 'error',
    medium: 'warning',
    low: 'info'
  }
  return typeMap[level] || 'default'
}

/**
 * 获取预警级别文本
 * @param level 预警级别
 * @returns 级别文本
 */
const getWarningLevelText = (level: string): string => {
  const textMap: Record<string, string> = {
    high: '高风险',
    medium: '中风险',
    low: '低风险'
  }
  return textMap[level] || '未知'
}

/**
 * 获取建议图标
 * @param type 建议类型
 * @returns 图标组件
 */
const getSuggestionIcon = (type: string) => {
  const iconMap: Record<string, any> = {
    course: IconBook,
    practice: IconCode,
    skill: IconAward,
    career: IconUser
  }
  return iconMap[type] || IconBook
}

/**
 * 截断文本
 * @param text 原始文本
 * @param maxLength 最大长度
 * @returns 截断后的文本
 */
const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

/**
 * 格式化时间
 * @param timestamp 时间戳
 * @returns 格式化后的时间字符串
 */
const formatTime = (timestamp: Date | string): string => {
  const date = typeof timestamp === 'string' ? new Date(timestamp) : timestamp
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

/**
 * 获取综合技能水平
 * @returns 综合技能水平
 */
const getOverallSkillLevel = (): number => {
  if (skills_data.value.length === 0) return 0
  const total = skills_data.value.reduce((sum, skill) => sum + skill.level, 0)
  return Math.round(total / skills_data.value.length)
}

/**
 * 获取最强技能
 * @returns 最强技能名称
 */
const getTopSkill = (): string => {
  if (skills_data.value.length === 0) return '暂无数据'
  const topSkill = skills_data.value.reduce((prev, current) => 
    prev.level > current.level ? prev : current
  )
  return topSkill.name
}

/**
 * 获取最弱技能
 * @returns 最弱技能名称
 */
const getWeakestSkill = (): string => {
  if (skills_data.value.length === 0) return '暂无数据'
  const weakestSkill = skills_data.value.reduce((prev, current) => 
    prev.level < current.level ? prev : current
  )
  return weakestSkill.name
}

/**
 * 获取技能标签类型
 * @param level 技能等级
 * @returns 标签类型
 */
const getSkillTagType = (level: number): 'default' | 'info' | 'success' | 'warning' | 'error' | 'primary' => {
  if (level >= 80) return 'success'
  if (level >= 60) return 'warning'
  return 'error'
}

/**
 * 探索兴趣
 * @param interest 兴趣数据
 */
const exploreInterest = (interest: InterestData): void => {
  message.info(`正在探索 ${interest.name} 相关内容...`)
}

/**
 * 时间段选择相关
 */
const selectedPeriod = ref<string>('month')
const periodOptions = [
  { label: '本月', value: 'month' },
  { label: '本季度', value: 'quarter' },
  { label: '本年', value: 'year' }
]

/**
 * 更新统计时间段
 * @param period 时间段值
 */
const updateStatsPeriod = (period: string): void => {
  selectedPeriod.value = period
  // 这里可以根据时间段重新获取数据
  message.info(`已切换到${periodOptions.find(p => p.value === period)?.label}统计`)
}

/**
 * 设置学习目标
 */
const setLearningGoal = (): void => {
  message.info('正在设置学习目标...')
}

/**
 * 处理预警
 * @param alert 预警数据
 */
const handleWarning = (alert: RiskAlert): void => {
  message.success(`正在处理预警：${alert.title}`)
}

/**
 * 忽略预警
 * @param alert 预警数据
 */
const dismissWarning = (alert: RiskAlert): void => {
  const index = risk_alerts.value.findIndex(item => item.id === alert.id)
  if (index > -1) {
    risk_alerts.value.splice(index, 1)
    message.info('已忽略该预警')
  }
}

/**
 * 获取预警数量
 * @param level 预警级别
 * @returns 预警数量
 */
const getWarningCount = (level: string): number => {
  return risk_alerts.value.filter(alert => alert.level === level).length
}

/**
 * 生成建议
 */
const generateSuggestions = (): void => {
  message.loading('AI正在生成个性化建议...', { duration: 2000 })
}

/**
 * 采纳建议
 * @param suggestion 学习建议数据
 */
const acceptSuggestion = (suggestion: LearningSuggestion): void => {
  message.success(`已采纳建议：${suggestion.title}`)
}

/**
 * 查看建议详情
 * @param suggestion 学习建议数据
 */
const viewSuggestionDetails = (suggestion: LearningSuggestion): void => {
  message.info(`查看建议详情：${suggestion.title}`)
}

/**
 * 忽略建议
 * @param suggestion 学习建议数据
 */
const dismissSuggestion = (suggestion: LearningSuggestion): void => {
  const index = learning_suggestions.value.findIndex(item => item.id === suggestion.id)
  if (index > -1) {
    learning_suggestions.value.splice(index, 1)
    message.info('已忽略该建议')
  }
}

/**
 * 刷新建议
 */
const refreshSuggestions = (): void => {
  message.loading('正在刷新建议...', { duration: 1000 })
}

/**
 * 导出建议
 */
const exportSuggestions = (): void => {
  message.success('学习计划已导出')
}

/**
 * 获取建议颜色
 * @param type 建议类型
 * @returns 颜色值
 */
const getSuggestionColor = (type: string): string => {
  const colorMap: Record<string, string> = {
    course: '#1890ff',
    practice: '#52c41a',
    skill: '#faad14',
    career: '#722ed1'
  }
  return colorMap[type] || '#1890ff'
}

/**
 * 获取建议标签类型
 * @param priority 优先级
 * @returns 标签类型
 */
const getSuggestionTagType = (priority: string): 'default' | 'info' | 'success' | 'warning' | 'error' | 'primary' => {
  const typeMap: Record<string, 'default' | 'info' | 'success' | 'warning' | 'error' | 'primary'> = {
    high: 'error',
    medium: 'warning',
    low: 'info'
  }
  return typeMap[priority] || 'info'
}

/**
 * 获取建议优先级文本
 * @param priority 优先级
 * @returns 优先级文本
 */
const getSuggestionPriorityText = (priority: string): string => {
  const textMap: Record<string, string> = {
    high: '高优先级',
    medium: '中优先级',
    low: '低优先级'
  }
  return textMap[priority] || '中优先级'
}

// 组件挂载时初始化用户信息
onMounted(async () => {
  await initializeUser()
  // 如果成功获取到student_id，则加载其他数据
  if (student_id.value) {
    await fetchAIAnalysis()
  }
})
</script>

<style scoped>
.portrait-analysis {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 卡片头部样式 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.expand-icon {
  color: #999;
  transition: transform 0.2s ease;
}

.expand-icon:hover {
  transform: translateX(2px);
}





/* 新的顶部仪表板样式 */
.top-dashboard {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 20px;
  margin-bottom: 32px;
  min-height: 480px;
}

/* 个人信息卡片 */
.personal-info-card {
  grid-row: span 1;
  height: 100%;
}

.comprehensive-evaluation-card,
.credit-progress-card,
.core-ability-card {
  height: 100%;
}

.personal-content {
  display: flex;
  gap: 20px;
  height: 100%;
  align-items: flex-start;
}

.avatar-section {
  flex-shrink: 0;
  padding-top: 10px;
}

.main-avatar {
  border: 3px solid #f0f0f0;
}

.info-section {
  flex: 1;
  display: flex;
  gap: 30px;
  min-height: 0;
}

.basic-info, .contact-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.name-row, .info-row, .contact-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.name-row {
  font-weight: 600;
  font-size: 16px;
}

.label {
  color: #666;
  font-size: 14px;
}

.value {
  color: #333;
  font-weight: 500;
}

/* 个人综合评价卡片 */
.comprehensive-evaluation-card {
  position: relative;
}

.evaluation-tip {
  position: absolute;
  top: 8px;
  right: 40px;
  background: #e6f7ff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #1890ff;
}

.evaluation-content {
  display: flex;
  gap: 20px;
  align-items: center;
}

.radar-chart-container {
  position: relative;
  flex-shrink: 0;
}

.radar-chart {
  position: relative;
}

.evaluation-labels {
  position: absolute;
  top: 0;
  left: 0;
  width: 200px;
  height: 200px;
  pointer-events: none;
}

.label-item {
  position: absolute;
  font-size: 12px;
  color: #666;
  text-align: center;
  white-space: nowrap;
}

.label-item.top {
  top: 5px;
  left: 50%;
  transform: translateX(-50%);
}

.label-item.top-right {
  top: 25px;
  right: 10px;
}

.label-item.bottom-right {
  bottom: 25px;
  right: 10px;
}

.label-item.bottom {
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
}

.label-item.bottom-left {
  bottom: 25px;
  left: 10px;
}

.label-item.top-left {
  top: 25px;
  left: 10px;
}

.evaluation-details {
  flex: 1;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail-label {
  color: #666;
  font-size: 14px;
}

.detail-value {
  color: #333;
  font-weight: 600;
  font-size: 16px;
}

/* 学分完成情况卡片 */
.credit-content {
  display: flex;
  gap: 20px;
  align-items: center;
}

.credit-chart {
  flex-shrink: 0;
}

.credit-number {
  font-size: 18px;
  font-weight: 600;
  fill: #333;
}

.credit-total {
  font-size: 12px;
  fill: #666;
}

.credit-label {
  font-size: 10px;
  fill: #999;
  font-weight: 500;
}

.credit-breakdown {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.item-label {
  font-size: 14px;
  color: #666;
}

/* 专业核心能力结构卡片 */
.ability-content {
  display: flex;
  gap: 20px;
  align-items: center;
}

.ability-chart {
  position: relative;
  flex-shrink: 0;
}

.ability-labels {
  position: absolute;
  top: 0;
  left: 0;
  width: 200px;
  height: 200px;
  pointer-events: none;
}

.ability-label {
  position: absolute;
  font-size: 11px;
  color: #666;
  text-align: center;
  max-width: 80px;
  line-height: 1.2;
}

.ability-label.top {
  top: 5px;
  left: 50%;
  transform: translateX(-50%);
}

.ability-label.right {
  top: 50%;
  right: 5px;
  transform: translateY(-50%);
}

.ability-label.bottom {
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
}

.ability-label.left {
  top: 50%;
  left: 5px;
  transform: translateY(-50%);
}

.ability-details {
  flex: 1;
}

.ability-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.ability-name {
  width: 80px;
  font-size: 14px;
  color: #666;
  flex-shrink: 0;
}

.ability-bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #18a058, #52c41a);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.ability-score {
  width: 40px;
  text-align: right;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

/* 课程成绩分布 */
.course-performance-section {
  margin-top: 24px;
  margin-bottom: 24px;
}

.course-performance-card {
  width: 100%;
}

.performance-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.performance-chart {
  width: 100%;
  overflow-x: auto;
}

.axis-label {
  font-size: 12px;
  fill: #666;
}

.axis-title {
  font-size: 14px;
  fill: #333;
  font-weight: 500;
}

.performance-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}



/* 响应式设计 */
@media (max-width: 1200px) {
  .top-dashboard {
    grid-template-columns: 1fr;
  }
  
  .personal-info-card {
    grid-row: span 1;
  }
  
  .personal-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .info-section {
    flex-direction: column;
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .evaluation-content,
  .credit-content,
  .ability-content {
    flex-direction: column;
    text-align: center;
  }
  
  .performance-chart svg {
    width: 100%;
    height: auto;
  }
}





/* 响应式设计 */
@media (max-width: 768px) {
  .portrait-analysis {
    padding: 16px;
  }
}


</style>