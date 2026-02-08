<template>
  <div class="job-page-container">
    <!-- 页面标题区域 -->
    <header class="header">
      <h1>就业推荐</h1>
      <p>根据您的专业背景和技能标签，为您推荐最适合的就业机会</p>
    </header>

    <!-- 用户信息卡片 -->
    <n-card class="user-profile" title="个人信息" size="small">
      <n-space vertical>
        <n-descriptions bordered size="small">
          <n-descriptions-item label="姓名">
            {{ user_info.name }}
          </n-descriptions-item>
          <n-descriptions-item label="专业">
            {{ user_info.major }}
          </n-descriptions-item>
          <n-descriptions-item label="年级">
            {{ user_info.grade }}
          </n-descriptions-item>
          <n-descriptions-item label="技能标签">
            <n-space>
              <n-tag v-for="skill in user_info.skills" :key="skill" type="success" size="small">
                {{ skill }}
              </n-tag>
            </n-space>
          </n-descriptions-item>
        </n-descriptions>
        <n-alert type="info" show-icon>
          <template #icon>
            <n-icon>
              <InfoCircle :size="24" />
            </n-icon>
          </template>
          <template #header>
            就业推荐提示
          </template>
          根据您的专业背景和技能标签，我们为您推荐了以下就业机会。点击任意职位了解详情。
        </n-alert>
      </n-space>
    </n-card>

    <!-- 筛选器区域 -->
    <div class="filter-section">
      <n-space align="center" justify="space-between" wrap-item>
        <n-space>
          <n-input v-model:value="filter_key" placeholder="搜索职位关键词" clearable>
            <template #prefix>
              <n-icon>
                <Search :size="24" />
              </n-icon>
            </template>
          </n-input>
          <n-select v-model:value="job_type" :options="job_types" placeholder="职位类型" style="width: 150px" />
          <n-select v-model:value="job_loc" :options="job_locs" placeholder="工作地点" style="width: 150px" />
        </n-space>
        <n-space>
          <n-dropdown trigger="click" :options="sort_options" @select="handle_sort">
            <n-button>
              {{ current_sort.label }}
              <template #icon>
                <n-icon>
                  <CaretDown :size="24" />
                </n-icon>
              </template>
            </n-button>
          </n-dropdown>
        </n-space>
      </n-space>
    </div>

    <!-- 职位列表区域 -->
    <div class="job-list-section">
      <n-grid :cols="1" :x-gap="12" :y-gap="12">
        <n-grid-item v-for="job in filtered_jobs" :key="job.id">
          <n-card hoverable class="job-card" @click="show_detail(job)">
            <template #header>
              <div class="job-header">
                <div class="job-title">
                  <n-space align="center">
                    <span class="title-text">{{ job.title }}</span>
                    <n-tag v-if="job.match_rate >= 90" type="success" size="small">匹配度高</n-tag>
                    <n-tag v-else-if="job.match_rate >= 70" type="info" size="small">匹配度中</n-tag>
                    <n-tag v-else type="warning" size="small">匹配度低</n-tag>
                  </n-space>
                </div>
                <div class="job-salary">{{ job.salary }}</div>
              </div>
            </template>
            <n-space vertical>
              <div class="job-company">
                <n-space align="center">
                  <n-icon>
                    <Building :size="24" />
                  </n-icon>
                  <span>{{ job.company }}</span>
                  <n-divider vertical />
                  <n-icon>
                    <MapPin :size="24" />
                  </n-icon>
                  <span>{{ job.location }}</span>
                  <n-divider vertical />
                  <n-icon>
                    <Briefcase :size="24" />
                  </n-icon>
                  <span>{{ job.type }}</span>
                </n-space>
              </div>
              <div class="job-tags">
                <n-space>
                  <n-tag v-for="tag in job.tags" :key="tag" size="small">{{ tag }}</n-tag>
                </n-space>
              </div>
              <div class="job-desc">{{ job.description }}</div>
              <div class="job-match">
                <n-space vertical size="small">
                  <div class="match-title">匹配度分析</div>
                  <n-progress type="line" :percentage="job.match_rate" :color="match_color(job.match_rate)" />
                  <div class="match-reason">
                    <n-icon>
                      <ThumbUp :size="24" />
                    </n-icon>
                    <span>{{ job.match_reason }}</span>
                  </div>
                </n-space>
              </div>
            </n-space>
            <template #footer>
              <n-space justify="end">
                <n-button text>
                  <template #icon>
                    <n-icon>
                      <Calendar :size="24" />
                    </n-icon>
                  </template>
                  发布时间: {{ job.pub_date }}
                </n-button>
                <n-button text>
                  <template #icon>
                    <n-icon>
                      <Star :size="24" />
                    </n-icon>
                  </template>
                  收藏
                </n-button>
                <n-button text>
                  <template #icon>
                    <n-icon>
                      <Share :size="24" />
                    </n-icon>
                  </template>
                  分享
                </n-button>
              </n-space>
            </template>
          </n-card>
        </n-grid-item>
      </n-grid>

      <!-- 空状态 -->
      <n-empty v-if="filtered_jobs.length === 0" description="暂无匹配的职位推荐">
        <template #extra>
          <n-button @click="reset_filter">重置筛选条件</n-button>
        </template>
      </n-empty>

      <!-- 分页 -->
      <div class="pagination" v-if="filtered_jobs.length > 0">
        <n-pagination v-model:page="page" :page-count="page_count" :page-size="page_size" />
      </div>
    </div>

    <!-- 职位详情弹窗 -->
    <n-modal v-model:show="show_modal" preset="card" title="职位详情" style="width: 700px" :bordered="false">
      <template #header-extra>
        <n-space>
          <n-button circle>
            <template #icon>
              <n-icon>
                <Star :size="24" />
              </n-icon>
            </template>
          </n-button>
          <n-button circle>
            <template #icon>
              <n-icon>
                <Share :size="24" />
              </n-icon>
            </template>
          </n-button>
        </n-space>
      </template>
      <div v-if="current_job">
        <n-space vertical size="large">
        <div class="detail-header">
          <div class="detail-title">
            <h2>{{ current_job.title }}</h2>
            <div class="detail-salary">{{ current_job.salary }}</div>
          </div>
          <div class="detail-company">
            <n-space align="center">
              <n-icon>
                <Building :size="24" />
              </n-icon>
              <span>{{ current_job.company }}</span>
              <n-divider vertical />
              <n-icon>
                <MapPin :size="24" />
              </n-icon>
              <span>{{ current_job.location }}</span>
              <n-divider vertical />
              <n-icon>
                <Briefcase :size="24" />
              </n-icon>
              <span>{{ current_job.type }}</span>
            </n-space>
          </div>
        </div>

        <n-divider />

        <div class="detail-section">
          <h3>
            <n-icon>
              <FileText :size="24" />
            </n-icon>
            职位描述
          </h3>
          <div class="detail-content">{{ current_job.description }}</div>
        </div>

        <div class="detail-section">
          <h3>
            <n-icon>
              <ListCheck :size="24" />
            </n-icon>
            任职要求
          </h3>
          <div class="detail-content">
            <n-list>
              <n-list-item v-for="(req, index) in current_job.requirements" :key="index">
                {{ req }}
              </n-list-item>
            </n-list>
          </div>
        </div>

        <div class="detail-section">
          <h3>
            <n-icon>
              <Award :size="24" />
            </n-icon>
            福利待遇
          </h3>
          <div class="detail-content">
            <n-space>
              <n-tag v-for="benefit in current_job.benefits" :key="benefit" size="medium">
                {{ benefit }}
              </n-tag>
            </n-space>
          </div>
        </div>

        <div class="detail-section">
          <h3>
            <n-icon>
              <ThumbUp :size="24" />
            </n-icon>
            匹配度分析
          </h3>
          <div class="detail-content">
            <n-space vertical>
              <n-progress type="line" :percentage="current_job.match_rate" :color="match_color(current_job.match_rate)" />
              <n-alert type="info">
                {{ current_job.match_reason }}
              </n-alert>
              <n-collapse>
                <n-collapse-item title="技能匹配详情" name="skill_match">
                  <n-space vertical>
                    <div v-for="(match, index) in current_job.skill_matches" :key="index" class="skill-match-item">
                      <div class="skill-name">{{ match.skill }}</div>
                      <n-progress type="line" :percentage="match.match_rate" :color="match_color(match.match_rate)" />
                    </div>
                  </n-space>
                </n-collapse-item>
              </n-collapse>
            </n-space>
          </div>
        </div>
        </n-space>
      </div>
      <template #footer>
        <n-space justify="end">
          <n-button type="primary" @click="apply_job">立即申请</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage } from 'naive-ui'

// 导入图标
import {
  IconBriefcase as Briefcase,
  IconBuilding as Building,
  IconMapPin as MapPin,
  IconFileText as FileText,
  IconListCheck as ListCheck,
  IconAward as Award,
  IconThumbUp as ThumbUp,
  IconCalendar as Calendar,
  IconStar as Star,
  IconShare as Share,
  IconSearch as Search,
  IconRefresh as Refresh,
  IconInfoCircle as InfoCircle,
  IconCaretDown as CaretDown
} from '@tabler/icons-vue'

// 创建消息实例
const message = useMessage()

// 用户信息
const user_info = ref({
  name: '刘在行',
  major: '计算机科学与技术',
  grade: '2024届',
  skills: ['Java', 'Python', '前端开发', '数据分析', '机器学习']
})

// 筛选条件
const filter_key = ref('')
const job_type = ref(null)
const job_loc = ref(null)
const page = ref(1)
const page_size = ref(10)
const page_count = ref(5)

// 排序选项
const sort_options = [
  {
    label: '默认排序',
    key: 'default'
  },
  {
    label: '匹配度优先',
    key: 'match'
  },
  {
    label: '最新发布',
    key: 'date'
  },
  {
    label: '薪资最高',
    key: 'salary'
  }
]
const current_sort = ref(sort_options[0])

// 职位类型选项
const job_types = [
  {
    label: '全职',
    value: '全职'
  },
  {
    label: '实习',
    value: '实习'
  },
  {
    label: '校招',
    value: '校招'
  }
]

// 工作地点选项
const job_locs = [
  {
    label: '北京',
    value: '北京'
  },
  {
    label: '上海',
    value: '上海'
  },
  {
    label: '广州',
    value: '广州'
  },
  {
    label: '深圳',
    value: '深圳'
  },
  {
    label: '杭州',
    value: '杭州'
  }
]

// 模拟职位数据
const jobs = ref([
  {
    id: 1,
    title: '前端开发工程师',
    company: '科技有限公司',
    location: '北京',
    type: '全职',
    salary: '15k-25k',
    tags: ['React', 'Vue', 'JavaScript'],
    description: '负责公司产品的前端开发工作，包括PC端和移动端的页面实现，与后端工程师协作完成产品功能开发。',
    pub_date: '2023-05-15',
    match_rate: 95,
    match_reason: '您的前端开发技能与该职位高度匹配，且有相关项目经验。',
    requirements: [
      '本科及以上学历，计算机相关专业',
      '熟悉HTML/CSS/JavaScript，熟悉至少一种主流前端框架',
      '了解前端工程化，有良好的代码风格',
      '有良好的沟通能力和团队协作精神'
    ],
    benefits: ['五险一金', '年终奖', '弹性工作', '定期团建', '免费零食'],
    skill_matches: [
      { skill: '前端开发', match_rate: 95 },
      { skill: 'JavaScript', match_rate: 90 },
      { skill: 'Vue', match_rate: 85 }
    ]
  },
  {
    id: 2,
    title: '数据分析师',
    company: '数据智能科技',
    location: '上海',
    type: '全职',
    salary: '18k-30k',
    tags: ['Python', '数据分析', 'SQL'],
    description: '负责公司业务数据的分析和挖掘，提供数据支持和决策建议，参与数据产品的开发。',
    pub_date: '2023-05-10',
    match_rate: 85,
    match_reason: '您的数据分析技能与该职位匹配度较高，建议强化SQL技能。',
    requirements: [
      '统计学、计算机科学或相关专业本科及以上学历',
      '熟练使用Python进行数据分析，熟悉常用的数据分析库',
      '熟悉SQL，有数据库操作经验',
      '有良好的数据敏感度和分析能力'
    ],
    benefits: ['五险一金', '年终奖', '股票期权', '带薪年假', '专业培训'],
    skill_matches: [
      { skill: '数据分析', match_rate: 85 },
      { skill: 'Python', match_rate: 80 },
      { skill: 'SQL', match_rate: 70 }
    ]
  },
  {
    id: 3,
    title: '机器学习工程师',
    company: 'AI创新科技',
    location: '深圳',
    type: '全职',
    salary: '25k-40k',
    tags: ['机器学习', 'Python', '深度学习'],
    description: '负责公司AI产品的算法研发，包括模型设计、训练和优化，参与产品从研发到落地的全过程。',
    pub_date: '2023-05-05',
    match_rate: 75,
    match_reason: '您具备机器学习基础知识，但需要更多实践经验。',
    requirements: [
      '计算机、人工智能或相关专业硕士及以上学历',
      '熟悉常用机器学习算法和深度学习框架',
      '有实际的机器学习项目经验',
      '良好的算法实现能力和问题解决能力'
    ],
    benefits: ['具有竞争力的薪资', '股票期权', '弹性工作', '技术分享', '国际会议'],
    skill_matches: [
      { skill: '机器学习', match_rate: 75 },
      { skill: 'Python', match_rate: 80 },
      { skill: '深度学习', match_rate: 65 }
    ]
  },
  {
    id: 4,
    title: 'Java后端开发工程师',
    company: '云服务科技',
    location: '杭州',
    type: '校招',
    salary: '15k-25k',
    tags: ['Java', 'Spring Boot', '微服务'],
    description: '负责公司核心业务系统的后端开发，包括API设计、功能实现和性能优化。',
    pub_date: '2023-05-12',
    match_rate: 90,
    match_reason: '您的Java技能与该职位高度匹配，且有相关项目经验。',
    requirements: [
      '计算机相关专业本科及以上学历',
      '熟悉Java编程，了解常用的设计模式',
      '熟悉Spring、Spring Boot等框架',
      '了解MySQL等关系型数据库'
    ],
    benefits: ['五险一金', '年终奖', '定期团建', '技术培训', '晋升空间'],
    skill_matches: [
      { skill: 'Java', match_rate: 90 },
      { skill: 'Spring Boot', match_rate: 85 },
      { skill: '数据库', match_rate: 80 }
    ]
  },
  {
    id: 5,
    title: '产品经理（技术方向）',
    company: '互联网科技',
    location: '北京',
    type: '全职',
    salary: '20k-35k',
    tags: ['产品设计', '用户体验', '技术背景'],
    description: '负责公司产品的规划和设计，协调开发团队实现产品功能，跟踪产品上线后的效果并持续优化。',
    pub_date: '2023-05-08',
    match_rate: 65,
    match_reason: '您的技术背景对该职位有帮助，但需要加强产品设计能力。',
    requirements: [
      '本科及以上学历，计算机或相关专业优先',
      '有技术背景，了解软件开发流程',
      '良好的产品思维和用户体验意识',
      '优秀的沟通能力和团队协作能力'
    ],
    benefits: ['五险一金', '年终奖', '弹性工作', '免费三餐', '健身房'],
    skill_matches: [
      { skill: '技术背景', match_rate: 85 },
      { skill: '产品设计', match_rate: 60 },
      { skill: '用户体验', match_rate: 55 }
    ]
  }
])

// 定义职位数据接口
interface JobData {
  id: number
  title: string
  company: string
  location: string
  type: string
  salary: string
  tags: string[]
  description: string
  pub_date: string
  match_rate: number
  match_reason: string
  requirements: string[]
  benefits: string[]
  skill_matches: {
    skill: string
    match_rate: number
  }[]
}

// 职位详情弹窗
const show_modal = ref(false)
const current_job = ref<JobData | null>(null)

// 根据筛选条件过滤职位
const filtered_jobs = computed(() => {
  let result = jobs.value

  // 关键词筛选
  if (filter_key.value) {
    const keyword = filter_key.value.toLowerCase()
    result = result.filter(job => {
      return (
        job.title.toLowerCase().includes(keyword) ||
        job.company.toLowerCase().includes(keyword) ||
        job.description.toLowerCase().includes(keyword) ||
        job.tags.some(tag => tag.toLowerCase().includes(keyword))
      )
    })
  }

  // 职位类型筛选
  if (job_type.value) {
    result = result.filter(job => job.type === job_type.value)
  }

  // 工作地点筛选
  if (job_loc.value) {
    result = result.filter(job => job.location === job_loc.value)
  }

  // 排序
  if (current_sort.value.key === 'match') {
    result = result.sort((a, b) => b.match_rate - a.match_rate)
  } else if (current_sort.value.key === 'date') {
    result = result.sort((a, b) => new Date(b.pub_date).getTime() - new Date(a.pub_date).getTime())
  } else if (current_sort.value.key === 'salary') {
    result = result.sort((a, b) => {
      const a_salary = parseInt(a.salary.split('-')[1])
      const b_salary = parseInt(b.salary.split('-')[1])
      return b_salary - a_salary
    })
  }

  return result
})

// 根据匹配度返回颜色
function match_color(rate: number) {
  if (rate >= 90) return '#18a058'
  if (rate >= 70) return '#2080f0'
  return '#f0a020'
}

// 显示职位详情
function show_detail(job: JobData) {
  current_job.value = job
  show_modal.value = true
}

// 申请职位
function apply_job() {
  message.success('申请成功，请等待企业联系')
  show_modal.value = false
}

// 处理排序选择
function handle_sort(key: string) {
  current_sort.value = sort_options.find(option => option.key === key) || sort_options[0]
}

// 刷新数据
function refresh_data() {
  message.success('已更新推荐列表')
  // 这里可以调用API获取最新数据
}

// 重置筛选条件
function reset_filter() {
  filter_key.value = ''
  job_type.value = null
  job_loc.value = null
  current_sort.value = sort_options[0]
}

// 组件挂载时获取数据
onMounted(() => {
  // 这里可以调用API获取初始数据
  message.success('就业推荐数据加载完成')
})
</script>

<style scoped>
.job-page-container {
  padding: 16px;
  font-family: "Microsoft YaHei", sans-serif;
}

.header {
  margin-bottom: 16px;
}

.header h1 {
  font-weight: 700;
  font-size: 24px;
  margin: 0;
}

.header p {
  color: #666;
  font-size: 14px;
  margin: 4px 0 0 0;
}

.user-profile {
  margin-bottom: 24px;
}

.filter-section {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.job-list-section {
  margin-bottom: 24px;
}

.job-card {
  transition: all 0.3s ease;
}

.job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.job-title {
  display: flex;
  align-items: center;
}

.title-text {
  font-size: 18px;
  font-weight: 500;
  margin-right: 8px;
}

.job-salary {
  font-size: 18px;
  font-weight: 500;
  color: #f60;
}

.job-company {
  margin: 8px 0;
  color: #606266;
}

.job-tags {
  margin: 8px 0;
}

.job-desc {
  margin: 12px 0;
  color: #606266;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.job-match {
  margin-top: 12px;
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.match-title {
  font-weight: 500;
  margin-bottom: 8px;
}

.match-reason {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
}

.pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

/* 详情弹窗样式 */
.detail-header {
  margin-bottom: 16px;
}

.detail-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.detail-title h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.detail-salary {
  font-size: 20px;
  font-weight: 500;
  color: #f60;
}

.detail-company {
  color: #606266;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 16px;
  font-weight: 500;
}

.detail-content {
  color: #606266;
  line-height: 1.6;
}

.skill-match-item {
  margin-bottom: 12px;
}

.skill-name {
  margin-bottom: 4px;
  font-weight: 500;
}
</style>