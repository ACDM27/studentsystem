<template>
  <div class="vote-survey-container">
    <!-- 页面标题 -->
    <div class="page_header">
      <h1>问卷与投票</h1>
      <p>参与校园问卷调查，为校园建设发声</p>
    </div>

    <!-- 中部统计区域 -->
    <div class="stats-section">
      <n-grid :cols="4" :x-gap="12">
        <n-gi>
          <n-card class="stat-card total">
            <div class="stat-number">{{ stats.total }}</div>
            <div class="stat-label">总数</div>
          </n-card>
        </n-gi>
        <n-gi>
          <n-card class="stat-card ongoing">
            <div class="stat-number">{{ stats.ongoing }}</div>
            <div class="stat-label">进行中</div>
          </n-card>
        </n-gi>
        <n-gi>
          <n-card class="stat-card ended">
            <div class="stat-number">{{ stats.ended }}</div>
            <div class="stat-label">已结束</div>
          </n-card>
        </n-gi>
        <n-gi>
          <n-card class="stat-card not_started">
            <div class="stat-number">{{ stats.not_started }}</div>
            <div class="stat-label">未开始</div>
          </n-card>
        </n-gi>
      </n-grid>
    </div>

    <!-- 筛选条件 -->
    <div class="filter-section">
      <n-space align="center">
        <n-input
          v-model:value="search_text"
          placeholder="搜索问卷标题或内容"
          clearable
          style="width: 300px"
        >
          <template #prefix>
            <n-icon>
              <IconSearch :size="18" />
            </n-icon>
          </template>
        </n-input>
      </n-space>

      <n-space>
        <n-select
          v-model:value="filter_status"
          placeholder="问卷状态"
          :options="status_opts"
          clearable
          style="width: 120px"
        />
        <n-select
          v-model:value="filter_type"
          placeholder="参与人数"
          :options="participant_opts"
          clearable
          style="width: 120px"
        />
      </n-space>
    </div>

    <!-- 问卷列表 -->
    <div class="survey-list">
      <n-list hoverable clickable>
        <n-list-item v-for="item in filtered_surveys" :key="item.id">
          <n-thing>
            <template #avatar>
              <n-avatar round>
                <template #icon>
                  <IconClipboardCheck v-if="item.type === '问卷'" :size="24" />
                  <IconVote v-else :size="24" />
                </template>
              </n-avatar>
            </template>
            
            <template #header>
              <div class="survey-header">
                <n-space align="center">
                  <span class="survey-title">{{ item.title }}</span>
                  <n-tag size="small" :type="getTagType(item.type)">
                    {{ item.type }}
                  </n-tag>
                </n-space>
              </div>
            </template>
            
            <template #description>
              <div class="survey-meta">
                <n-space>
                  <n-space align="center" class="meta-item">
                    <IconCalendar :size="16" />
                    <span>截止日期: {{ item.deadline }}</span>
                  </n-space>
                  <n-space align="center" class="meta-item">
                    <IconUsers :size="16" />
                    <span>参与人数: {{ item.participants }}</span>
                  </n-space>
                </n-space>
              </div>
            </template>

            <template #footer>
              <div class="survey-actions">
                <n-space>
                  <n-button size="small" @click="viewResults(item.id)">
                    <template #icon>
                      <IconChartBar :size="16" />
                    </template>
                    查看结果
                  </n-button>
                  <n-button size="small" type="primary" @click="participate(item.id)">
                    <template #icon>
                      <IconEdit :size="16" />
                    </template>
                    立即参与
                  </n-button>
                </n-space>
              </div>
            </template>
          </n-thing>
        </n-list-item>
      </n-list>

      <!-- 空状态 -->
      <n-empty v-if="filtered_surveys.length === 0" description="暂无问卷数据" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { 
  IconSearch, 
  IconClipboardCheck,
  IconCalendar, 
  IconUsers, 
  IconChartBar, 
  IconEdit 
} from '@tabler/icons-vue'

// 统计数据
const stats = ref({
  total: 4,
  ongoing: 2,
  ended: 1,
  not_started: 1
})

// 筛选条件
const search_text = ref('')
const filter_status = ref(null)
const filter_type = ref(null)

// 下拉选项
const status_opts = [
  { label: '进行中', value: 'ongoing' },
  { label: '已结束', value: 'ended' },
  { label: '未开始', value: 'not_started' }
]

const participant_opts = [
  { label: '0-100人', value: 'low' },
  { label: '100-500人', value: 'medium' },
  { label: '500人以上', value: 'high' }
]

// 问卷数据
const surveys = ref([
  {
    id: 1,
    title: '关于大学生素质拓展的调查问卷',
    type: '问卷',
    status: 'ongoing',
    deadline: '2024-08-01',
    participants: '120 / 200',
    description: '调查大学生对素质拓展活动的参与情况和意见建议'
  },
  {
    id: 2,
    title: '"我最喜爱的老师"评选活动',
    type: '投票',
    status: 'ongoing',
    deadline: '2024-06-30',
    participants: '350 / 400',
    description: '评选本学期最受学生欢迎的教师'
  },
  {
    id: 3,
    title: '关于食堂餐饮服务的满意度调查',
    type: '问卷',
    status: 'ended',
    deadline: '2024-07-20',
    participants: '85 / 150',
    description: '了解学生对食堂服务的满意程度和改进建议'
  },
  {
    id: 4,
    title: '毕业季"就业市场"活动意向征集',
    type: '投票',
    status: 'not_started',
    deadline: '2024-06-15',
    participants: '0 / 500',
    description: '征集毕业生对就业市场活动的参与意向'
  }
])

// 筛选后的问卷列表
const filtered_surveys = computed(() => {
  return surveys.value.filter(item => {
    // 标题搜索
    const text_match = search_text.value ? 
      item.title.toLowerCase().includes(search_text.value.toLowerCase()) ||
      item.description.toLowerCase().includes(search_text.value.toLowerCase()) : 
      true
    
    // 状态筛选
    const status_match = filter_status.value ? 
      item.status === filter_status.value : 
      true
    
    // 参与人数筛选
    let participant_match = true
    if (filter_type.value) {
      const count = parseInt(item.participants.split(' / ')[0])
      if (filter_type.value === 'low' && count > 100) participant_match = false
      if (filter_type.value === 'medium' && (count <= 100 || count > 500)) participant_match = false
      if (filter_type.value === 'high' && count <= 500) participant_match = false
    }
    
    return text_match && status_match && participant_match
  })
})

// 获取标签类型
const getTagType = (type: string) => {
  return type === '问卷' ? 'info' : 'warning'
}

// 创建问卷
const handleCreateSurvey = () => {
  // 实际项目中应该跳转到创建页面或打开创建对话框
  console.log('创建新问卷')
}

// 查看结果
const viewResults = (id: number) => {
  console.log('查看问卷结果', id)
  // 实际项目中应该跳转到结果页面
}

// 参与问卷
const participate = (id: number) => {
  console.log('参与问卷', id)
  // 实际项目中应该跳转到问卷填写页面
}
</script>

<style scoped>
.vote-survey-container {
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

.stats-section {
  margin-bottom: 24px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.stat-card {
  text-align: center;
  padding: 16px;
  border-radius: 8px;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.45);
}

.total .stat-number {
  color: #2080f0;
}

.ongoing .stat-number {
  color: #18a058;
}

.ended .stat-number {
  color: #d03050;
}

.not_started .stat-number {
  color: #f0a020;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.survey-list {
  background-color: #fff;
  border-radius: 8px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.survey-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.survey-title {
  font-weight: bold;
  font-size: 16px;
}

.survey-meta {
  margin-top: 8px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.meta-item {
  color: rgba(0, 0, 0, 0.45);
  font-size: 14px;
}

.survey-actions {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}
</style>