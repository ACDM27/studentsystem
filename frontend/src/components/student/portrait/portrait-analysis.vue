<template>
  <div class="portrait-analysis">
    <div class="top-dashboard">
      <!-- 个人信息卡片 -->
      <n-card class="personal-info-card" hoverable>
        <template #header>
          <div class="card-header">
            <span class="header-title">个人信息</span>
          </div>
        </template>
        <div class="personal-content">
          <div class="avatar-section">
            <n-avatar :size="80" :src="student_avatar" class="main-avatar">
              {{ student_name.charAt(0) }}
            </n-avatar>
          </div>
          <div class="info-section">
            <div class="info-row">
              <span class="label">姓名</span>
              <span class="value">{{ student_name }}</span>
            </div>
            <div class="info-row">
              <span class="label">专业</span>
              <span class="value">{{ student_major || '未设置' }}</span>
            </div>
            <div class="info-row">
              <span class="label">学号</span>
              <span class="value">{{ student_number || '未设置' }}</span>
            </div>
          </div>
        </div>
      </n-card>

      <!-- AI 人物画像卡片 -->
      <n-card class="persona-card" hoverable>
        <template #header>
          <div class="card-header">
            <span class="header-title">AI 人物画像</span>
            <n-button
              size="small"
              :loading="personaLoading"
              class="generate-btn"
              @click="generatePersona"
            >
              {{ personaData ? '重新生成' : '生成画像' }}
            </n-button>
          </div>
        </template>

        <!-- 空状态 -->
        <div v-if="!personaData" class="persona-empty">
          <div class="empty-icon">🎓</div>
          <p>点击"生成画像"按钮，AI将基于您的真实成果数据生成专属人物画像</p>
        </div>

        <!-- 画像内容 -->
        <div v-else class="persona-content">
          <!-- 标签云 -->
          <div class="persona-tags">
            <span
              v-for="(tag, index) in personaData.tags"
              :key="index"
              class="persona-tag"
            >{{ tag }}</span>
          </div>

          <!-- 人物概述 -->
          <div class="persona-summary">
            {{ personaData.summary }}
          </div>

          <!-- 维度分析 -->
          <div class="persona-dimensions" v-if="personaData.dimensions">
            <div
              v-for="(dim, key) in personaData.dimensions"
              :key="key"
              class="dimension-item"
            >
              <span class="dim-label">{{ dim.label }}</span>
              <span class="dim-analysis">{{ dim.analysis || '点击重新生成以获取文字分析' }}</span>
            </div>
          </div>

          <!-- 优势与建议 -->
          <div class="persona-details">
            <div class="detail-col strengths-col">
              <h4 class="detail-title strengths-title">优势</h4>
              <ul class="detail-list">
                <li v-for="(s, i) in personaData.strengths" :key="i">{{ s }}</li>
              </ul>
            </div>
            <div class="detail-col suggestions-col">
              <h4 class="detail-title suggestions-title">建议</h4>
              <ul class="detail-list">
                <li v-for="(s, i) in personaData.suggestions" :key="i">{{ s }}</li>
              </ul>
            </div>
          </div>

          <!-- 生成时间 -->
          <div class="persona-time" v-if="personaData.generated_at">
            生成时间：{{ formatTime(personaData.generated_at) }}
          </div>
        </div>
      </n-card>

      <!-- 成果综合评价（雷达图） -->
      <n-card class="comprehensive-evaluation-card" hoverable>
        <template #header>
          <div class="card-header">
            <span class="header-title">成果综合评价</span>
          </div>
        </template>
        <div class="evaluation-content">
          <div class="radar-chart-container">
            <div class="radar-chart">
              <svg width="220" height="220" viewBox="0 0 220 220">
                <!-- 雷达图背景网格 -->
                <g class="radar-grid">
                  <polygon v-for="level in [0.2, 0.4, 0.6, 0.8, 1.0]" :key="level"
                    :points="gridPoints(level)" fill="none" stroke="#e0e0e0" stroke-width="1"/>
                  <!-- 轴线 -->
                  <line v-for="(_, i) in 6" :key="'axis'+i"
                    x1="110" y1="110"
                    :x2="110 + 80 * Math.cos(Math.PI/2 - i * Math.PI/3)"
                    :y2="110 - 80 * Math.sin(Math.PI/2 - i * Math.PI/3)"
                    stroke="#e0e0e0" stroke-width="1"/>
                </g>
                <!-- 数据多边形 -->
                <polygon :points="radarPoints" fill="rgba(26, 58, 138, 0.25)" stroke="#1a3a8a" stroke-width="2"/>
                <!-- 数据点 -->
                <circle v-for="(pt, i) in radarDataPoints" :key="'pt'+i"
                  :cx="pt.x" :cy="pt.y" r="4" fill="#1a3a8a"/>
              </svg>
            </div>
            <div class="evaluation-labels">
              <div class="label-item top">竞赛 ({{ achievementData.competition }})</div>
              <div class="label-item top-right">科研 ({{ achievementData.research }})</div>
              <div class="label-item bottom-right">项目 ({{ achievementData.project }})</div>
              <div class="label-item bottom">论文 ({{ achievementData.paper }})</div>
              <div class="label-item bottom-left">专利 ({{ achievementData.patent }})</div>
              <div class="label-item top-left">证书 ({{ achievementData.certificate }})</div>
            </div>
          </div>
          <div class="evaluation-stats">
            <div class="stat-item">
              <span class="stat-number">{{ totalAchievements }}</span>
              <span class="stat-label">成果总数</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ achievementTypes }}</span>
              <span class="stat-label">涵盖类型</span>
            </div>
            <div class="stat-item">
              <span class="stat-number">{{ dominantType }}</span>
              <span class="stat-label">主要方向</span>
            </div>
          </div>
        </div>
      </n-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { NCard, NAvatar, NButton, useMessage } from 'naive-ui'
import {
  getStudentPersona,
  generateStudentPersona,
  getStudentMe as fetchStudentMe,
  getMyAchievements as fetchAchievements
} from '@/api'

const message = useMessage()

// Student info
const student_name = ref('')
const student_avatar = ref('')
const student_major = ref('')
const student_number = ref('')

// Achievement data
const achievementData = ref({
  competition: 0, research: 0, project: 0,
  paper: 0, patent: 0, certificate: 0
})

// Persona
const personaData = ref<any>(null)
const personaLoading = ref(false)

// --- Init ---
const initializeUser = async () => {
  try {
    const resp = await fetchStudentMe()
    // 响应拦截器已解包，resp 即为 data 对象
    if (resp) {
      const data = resp as any
      student_name.value = data.name || data.username || '未知用户'
      student_avatar.value = data.avatar_url || ''
      student_major.value = data.major || ''
      student_number.value = data.student_id || ''
    }
  } catch (e) {
    console.error('获取用户信息失败:', e)
  }
}

// --- Achievement counts ---
const fetchAchievementCounts = async () => {
  try {
    const resp = await fetchAchievements() as any
    const list = Array.isArray(resp) ? resp : (resp?.data ? resp.data : [])
    const counts = { competition: 0, research: 0, project: 0, paper: 0, patent: 0, certificate: 0 }
    for (const item of list) {
      const t = String(item?.type || '').toLowerCase()
      if (t.includes('竞赛') || t.includes('competition')) counts.competition++
      else if (t.includes('科研') || t.includes('research')) counts.research++
      else if (t.includes('项目') || t.includes('project')) counts.project++
      else if (t.includes('论文') || t.includes('paper')) counts.paper++
      else if (t.includes('专利') || t.includes('patent')) counts.patent++
      else if (t.includes('证书') || t.includes('certificate')) counts.certificate++
    }
    achievementData.value = counts
  } catch (e) {
    console.error('获取成果统计失败:', e)
  }
}

// --- Persona ---
const loadPersona = async () => {
  try {
    const resp = await getStudentPersona() as any
    if (resp) {
      personaData.value = resp.persona ?? null
    }
  } catch (e) {
    console.error('加载画像失败:', e)
  }
}

const generatePersona = async () => {
  personaLoading.value = true
  try {
    const resp = await generateStudentPersona() as any
    if (resp?.persona) {
      personaData.value = resp.persona
      message.success('画像生成成功')
    }
  } catch (e) {
    console.error('生成画像失败:', e)
    message.error('生成画像失败，请稍后重试')
  } finally {
    personaLoading.value = false
  }
}

// --- Radar chart ---
const radarValues = computed(() => {
  const d = achievementData.value
  return [d.competition, d.research, d.project, d.paper, d.patent, d.certificate]
})

const maxVal = computed(() => {
  const m = Math.max(...radarValues.value)
  return m > 0 ? m : 1
})

function polarToXY(ratio: number, index: number): { x: number; y: number } {
  const cx = 110, cy = 110, r = 80
  const angle = Math.PI / 2 - index * Math.PI / 3
  return {
    x: cx + r * ratio * Math.cos(angle),
    y: cy - r * ratio * Math.sin(angle)
  }
}

function gridPoints(level: number): string {
  return Array.from({ length: 6 }, (_, i) => {
    const pt = polarToXY(level, i)
    return `${pt.x},${pt.y}`
  }).join(' ')
}

const radarDataPoints = computed(() => {
  return radarValues.value.map((v, i) => polarToXY(v / maxVal.value, i))
})

const radarPoints = computed(() => {
  return radarDataPoints.value.map(pt => `${pt.x},${pt.y}`).join(' ')
})

// --- Stats ---
const totalAchievements = computed(() => {
  return radarValues.value.reduce((a, b) => a + b, 0)
})

const achievementTypes = computed(() => {
  return radarValues.value.filter(v => v > 0).length
})

const dominantType = computed(() => {
  const labels = ['竞赛', '科研', '项目', '论文', '专利', '证书']
  const vals = radarValues.value
  const maxIdx = vals.indexOf(Math.max(...vals))
  return vals[maxIdx] > 0 ? labels[maxIdx] : '暂无'
})

// --- Utils ---
const formatTime = (timestamp: string) => {
  try {
    return new Date(timestamp).toLocaleString('zh-CN', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit'
    })
  } catch {
    return timestamp
  }
}

// --- Mount ---
onMounted(async () => {
  await initializeUser()
  await Promise.all([fetchAchievementCounts(), loadPersona()])
})
</script>

<style scoped>
.portrait-analysis {
  padding: 24px;
  background: #f5f7fa;
  min-height: 100vh;
}

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

/* ===== Grid Layout ===== */
.top-dashboard {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
}

.personal-info-card {
  grid-column: 1;
  grid-row: 1;
}

.persona-card {
  grid-column: 2;
  grid-row: 1 / 3;
}

.comprehensive-evaluation-card {
  grid-column: 1;
  grid-row: 2;
}

/* ===== Personal Info ===== */
.personal-content {
  display: flex;
  gap: 24px;
  align-items: center;
}

.avatar-section {
  flex-shrink: 0;
}

.main-avatar {
  border: 3px solid #f0f0f0;
}

.info-section {
  flex: 1;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-row:last-child {
  border-bottom: none;
}

.label {
  color: #666;
  font-size: 14px;
}

.value {
  color: #333;
  font-weight: 500;
}

/* ===== AI Persona Card ===== */
.generate-btn {
  background: linear-gradient(135deg, #1a3a8a 0%, #0d2b6b 100%);
  border: none;
  color: white;
}

.generate-btn:hover:not(:disabled) {
  box-shadow: 0 2px 8px rgba(13, 43, 107, 0.4);
}

.generate-btn:disabled {
  background: #ccc;
  color: #999;
}

.persona-empty {
  text-align: center;
  padding: 48px 24px;
  color: #999;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.persona-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Tags */
.persona-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.persona-tag {
  display: inline-block;
  padding: 4px 14px;
  background: rgba(26, 58, 138, 0.08);
  color: #1a3a8a;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid rgba(26, 58, 138, 0.15);
}

/* Summary */
.persona-summary {
  color: #444;
  font-size: 14px;
  line-height: 1.8;
  padding: 12px 16px;
  background: #f8f9fc;
  border-radius: 8px;
  border-left: 3px solid #1a3a8a;
}

/* Dimensions */
.persona-dimensions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dimension-item {
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 8px 12px;
  background: #f8f9fc;
  border-radius: 6px;
}

.dim-label {
  width: 80px;
  font-size: 13px;
  color: #1a3a8a;
  font-weight: 600;
  flex-shrink: 0;
}

.dim-analysis {
  flex: 1;
  font-size: 13px;
  color: #555;
  line-height: 1.6;
}

/* Strengths & Suggestions */
.persona-details {
  display: flex;
  gap: 16px;
}

.detail-col {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
}

.strengths-col {
  background: rgba(24, 160, 88, 0.06);
}

.suggestions-col {
  background: rgba(26, 58, 138, 0.06);
}

.detail-title {
  font-size: 13px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.strengths-title {
  color: #18a058;
}

.suggestions-title {
  color: #1a3a8a;
}

.detail-list {
  margin: 0;
  padding-left: 18px;
  font-size: 13px;
  color: #555;
  line-height: 1.8;
}

.persona-time {
  font-size: 12px;
  color: #aaa;
  text-align: right;
}

/* ===== Radar Chart ===== */
.evaluation-content {
  display: flex;
  gap: 24px;
  align-items: center;
}

.radar-chart-container {
  position: relative;
  flex-shrink: 0;
  width: 220px;
  height: 220px;
}

.radar-chart {
  position: relative;
}

.evaluation-labels {
  position: absolute;
  top: 0;
  left: 0;
  width: 220px;
  height: 220px;
  pointer-events: none;
}

.label-item {
  position: absolute;
  font-size: 12px;
  color: #666;
  text-align: center;
  white-space: nowrap;
}

.label-item.top { top: 2px; left: 50%; transform: translateX(-50%); }
.label-item.top-right { top: 30px; right: -10px; }
.label-item.bottom-right { bottom: 30px; right: -10px; }
.label-item.bottom { bottom: 2px; left: 50%; transform: translateX(-50%); }
.label-item.bottom-left { bottom: 30px; left: -10px; }
.label-item.top-left { top: 30px; left: -10px; }

.evaluation-stats {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  background: #f8f9fc;
  border-radius: 8px;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #1a3a8a;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

/* ===== Responsive ===== */
@media (max-width: 1200px) {
  .top-dashboard {
    grid-template-columns: 1fr;
  }
  .persona-card {
    grid-column: 1;
    grid-row: auto;
  }
  .comprehensive-evaluation-card {
    grid-column: 1;
    grid-row: auto;
  }
}

@media (max-width: 768px) {
  .portrait-analysis {
    padding: 16px;
  }
  .personal-content {
    flex-direction: column;
    text-align: center;
  }
  .evaluation-content {
    flex-direction: column;
  }
  .persona-details {
    flex-direction: column;
  }
}
</style>
