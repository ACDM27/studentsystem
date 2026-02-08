<template>
  <div class="talent-market-container">
    <!-- 页面标题区域 -->
    <header class="header">
      <h1>人才市场</h1>
      <p>发现优质企业和职位机会，开启您的职业发展之路</p>
    </header>

    <!-- 统计信息卡片 -->
    <n-grid :cols="4" :x-gap="16" :y-gap="16" class="stats-section">
      <n-grid-item>
        <n-card class="stat-card">
          <n-statistic label="招聘企业" :value="market_stats.total_comp">
            <template #prefix>
              <n-icon>
                <Building :size="24" />
              </n-icon>
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card class="stat-card">
          <n-statistic label="开放职位" :value="market_stats.total_pos">
            <template #prefix>
              <n-icon>
                <Briefcase :size="24" />
              </n-icon>
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card class="stat-card">
          <n-statistic label="本月新增" :value="market_stats.new_pos">
            <template #prefix>
              <n-icon>
                <TrendingUp :size="24" />
              </n-icon>
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card class="stat-card">
          <n-statistic label="匹配推荐" :value="market_stats.match_pos">
            <template #prefix>
              <n-icon>
                <Target :size="24" />
              </n-icon>
            </template>
          </n-statistic>
        </n-card>
      </n-grid-item>
    </n-grid>

    <!-- 筛选器区域 -->
    <n-collapse-transition :show="show_filter">
      <n-card class="filter-section" title="筛选条件">
        <n-grid :cols="4" :x-gap="16" :y-gap="16">
          <n-grid-item>
            <n-form-item label="企业名称">
              <n-input v-model:value="filter_comp" placeholder="搜索企业名称" clearable>
                <template #prefix>
                  <n-icon>
                    <Search :size="16" />
                  </n-icon>
                </template>
              </n-input>
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="行业类型">
              <n-select v-model:value="filter_ind" :options="industry_opts" placeholder="选择行业" clearable />
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="企业规模">
              <n-select v-model:value="filter_size" :options="size_opts" placeholder="选择规模" clearable />
            </n-form-item>
          </n-grid-item>
          <n-grid-item>
            <n-form-item label="工作地点">
              <n-select v-model:value="filter_loc" :options="location_opts" placeholder="选择地点" clearable />
            </n-form-item>
          </n-grid-item>
        </n-grid>
        <n-space justify="end" style="margin-top: 16px;">
          <n-button @click="reset_filter">重置</n-button>
          <n-button type="primary" @click="apply_filter">应用筛选</n-button>
        </n-space>
      </n-card>
    </n-collapse-transition>

    <!-- 企业列表区域 -->
    <div class="company-list-section">
      <n-grid :cols="1" :x-gap="16" :y-gap="16">
        <n-grid-item v-for="company in filtered_comp" :key="company.id">
          <n-card hoverable class="company-card">
            <template #header>
              <div class="company-header">
                <div class="company-info">
                  <n-space align="center">
                    <n-avatar :size="48" :src="company.logo" fallback-src="">
                      {{ company.name.charAt(0) }}
                    </n-avatar>
                    <div class="company-details">
                      <h3 class="company-name">{{ company.name }}</h3>
                      <n-space size="small">
                        <n-tag size="small" type="info">{{ company.industry }}</n-tag>
                        <n-tag size="small">{{ company.size }}</n-tag>
                        <n-tag size="small" type="success">{{ company.location }}</n-tag>
                      </n-space>
                    </div>
                  </n-space>
                </div>
                <div class="company-actions">
                  <n-space>
                    <n-button size="small" @click="view_company(company)">
                      <template #icon>
                        <n-icon>
                          <Eye :size="16" />
                        </n-icon>
                      </template>
                      查看详情
                    </n-button>
                    <n-button size="small" type="primary" @click="contact_company(company)">
                      <template #icon>
                        <n-icon>
                          <Mail :size="16" />
                        </n-icon>
                      </template>
                      联系企业
                    </n-button>
                  </n-space>
                </div>
              </div>
            </template>
            
            <n-space vertical>
              <div class="company-desc">
                <p>{{ company.description }}</p>
              </div>
              
              <n-divider />
              
              <!-- 招聘职位列表 -->
              <div class="positions-section">
                <h4 class="section-title">
                  <n-icon>
                    <Briefcase :size="16" />
                  </n-icon>
                  招聘职位 ({{ company.positions.length }})
                </h4>
                <n-grid :cols="2" :x-gap="12" :y-gap="12">
                  <n-grid-item v-for="position in company.positions" :key="position.id">
                    <n-card size="small" class="position-card" hoverable @click="view_position(position)">
                      <template #header>
                        <div class="position-header">
                          <span class="position-title">{{ position.title }}</span>
                          <span class="position-salary">{{ position.salary }}</span>
                        </div>
                      </template>
                      <n-space vertical size="small">
                        <div class="position-info">
                          <n-space size="small">
                            <n-icon size="14">
                              <MapPin :size="14" />
                            </n-icon>
                            <span>{{ position.location }}</span>
                            <n-divider vertical />
                            <n-icon size="14">
                              <Clock :size="14" />
                            </n-icon>
                            <span>{{ position.exp_req }}</span>
                          </n-space>
                        </div>
                        <div class="position-tags">
                          <n-space size="small">
                            <n-tag v-for="skill in position.skills" :key="skill" size="small">
                              {{ skill }}
                            </n-tag>
                          </n-space>
                        </div>
                        <div class="position-desc">
                          {{ position.description }}
                        </div>
                      </n-space>
                    </n-card>
                  </n-grid-item>
                </n-grid>
              </div>
            </n-space>
            
            <template #footer>
              <n-space justify="space-between" align="center">
                <div class="company-meta">
                  <n-space size="small">
                    <n-icon size="14">
                      <Calendar :size="14" />
                    </n-icon>
                    <span>更新时间: {{ company.update_time }}</span>
                  </n-space>
                </div>
                <div class="company-rating">
                  <n-space align="center" size="small">
                    <span>企业评分:</span>
                    <n-rate :value="company.rating" readonly size="small" />
                    <span>({{ company.rating }})</span>
                  </n-space>
                </div>
              </n-space>
            </template>
          </n-card>
        </n-grid-item>
      </n-grid>

      <!-- 空状态 -->
      <n-empty v-if="filtered_comp.length === 0" description="暂无匹配的企业信息">
        <template #extra>
          <n-button @click="reset_filter">重置筛选条件</n-button>
        </template>
      </n-empty>

      <!-- 分页 -->
      <div class="pagination" v-if="filtered_comp.length > 0">
        <n-pagination 
          v-model:page="current_page" 
          :page-count="total_pages" 
          :page-size="page_size"
          show-size-picker
          :page-sizes="[10, 20, 50]"
          @update:page-size="handle_page_size"
        />
      </div>
    </div>

    <!-- 企业详情弹窗 -->
    <n-modal v-model:show="show_comp_modal" preset="card" title="企业详情" style="width: 800px">
      <template #header-extra>
        <n-space>
          <n-button circle @click="contact_company(selected_comp)">
            <template #icon>
              <n-icon>
                <Mail :size="16" />
              </n-icon>
            </template>
          </n-button>
        </n-space>
      </template>
      
      <div v-if="selected_comp" class="company-detail">
        <n-space vertical size="large">
          <!-- 企业基本信息 -->
          <n-descriptions bordered :column="2">
            <n-descriptions-item label="企业名称">{{ selected_comp.name }}</n-descriptions-item>
            <n-descriptions-item label="所属行业">{{ selected_comp.industry }}</n-descriptions-item>
            <n-descriptions-item label="企业规模">{{ selected_comp.size }}</n-descriptions-item>
            <n-descriptions-item label="成立时间">{{ selected_comp.found_date }}</n-descriptions-item>
            <n-descriptions-item label="注册资本">{{ selected_comp.capital }}</n-descriptions-item>
            <n-descriptions-item label="企业性质">{{ selected_comp.nature }}</n-descriptions-item>
            <n-descriptions-item label="总部地址" :span="2">{{ selected_comp.address }}</n-descriptions-item>
          </n-descriptions>
          
          <!-- 企业介绍 -->
          <div>
            <h4>企业介绍</h4>
            <p>{{ selected_comp.full_desc }}</p>
          </div>
          
          <!-- 联系方式 -->
          <div>
            <h4>联系方式</h4>
            <n-descriptions bordered :column="2">
              <n-descriptions-item label="联系人">{{ selected_comp.contact_name }}</n-descriptions-item>
              <n-descriptions-item label="联系电话">{{ selected_comp.contact_phone }}</n-descriptions-item>
              <n-descriptions-item label="邮箱地址">{{ selected_comp.contact_email }}</n-descriptions-item>
              <n-descriptions-item label="官方网站">
                <n-button text tag="a" :href="selected_comp.website" target="_blank">
                  {{ selected_comp.website }}
                </n-button>
              </n-descriptions-item>
            </n-descriptions>
          </div>
        </n-space>
      </div>
    </n-modal>

    <!-- 职位详情弹窗 -->
    <n-modal v-model:show="show_pos_modal" preset="card" title="职位详情" style="width: 700px">
      <div v-if="selected_pos" class="position-detail">
        <n-space vertical size="large">
          <!-- 职位基本信息 -->
          <n-descriptions bordered :column="2">
            <n-descriptions-item label="职位名称">{{ selected_pos.title }}</n-descriptions-item>
            <n-descriptions-item label="薪资待遇">{{ selected_pos.salary }}</n-descriptions-item>
            <n-descriptions-item label="工作地点">{{ selected_pos.location }}</n-descriptions-item>
            <n-descriptions-item label="经验要求">{{ selected_pos.exp_req }}</n-descriptions-item>
            <n-descriptions-item label="学历要求">{{ selected_pos.edu_req }}</n-descriptions-item>
            <n-descriptions-item label="招聘人数">{{ selected_pos.count }}</n-descriptions-item>
          </n-descriptions>
          
          <!-- 职位描述 -->
          <div>
            <h4>职位描述</h4>
            <p>{{ selected_pos.full_desc }}</p>
          </div>
          
          <!-- 技能要求 -->
          <div>
            <h4>技能要求</h4>
            <n-space>
              <n-tag v-for="skill in selected_pos.skills" :key="skill" type="info">
                {{ skill }}
              </n-tag>
            </n-space>
          </div>
          
          <!-- 福利待遇 -->
          <div>
            <h4>福利待遇</h4>
            <n-space>
              <n-tag v-for="benefit in selected_pos.benefits" :key="benefit" type="success">
                {{ benefit }}
              </n-tag>
            </n-space>
          </div>
        </n-space>
      </div>
      
      <template #footer>
        <n-space justify="end">
          <n-button @click="show_pos_modal = false">关闭</n-button>
          <n-button type="primary" @click="apply_position">投递简历</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 联系企业弹窗 -->
    <n-modal v-model:show="show_contact_modal" preset="card" title="联系企业" style="width: 600px">
      <n-form ref="contact_form" :model="contact_data" :rules="contact_rules">
        <n-form-item label="联系主题" path="subject">
          <n-input v-model:value="contact_data.subject" placeholder="请输入联系主题" />
        </n-form-item>
        <n-form-item label="联系内容" path="content">
          <n-input 
            v-model:value="contact_data.content" 
            type="textarea" 
            :rows="6" 
            placeholder="请详细描述您的需求或问题"
          />
        </n-form-item>
        <n-form-item label="联系方式" path="contact_info">
          <n-input v-model:value="contact_data.contact_info" placeholder="请留下您的联系方式" />
        </n-form-item>
      </n-form>
      
      <template #footer>
        <n-space justify="end">
          <n-button @click="show_contact_modal = false">取消</n-button>
          <n-button type="primary" @click="submit_contact">发送</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  NSpace, NIcon, NButton, NCard, NGrid, NGridItem, NStatistic, 
  NCollapseTransition, NFormItem, NInput, NSelect, NTag, NAvatar,
  NDivider, NRate, NEmpty, NPagination, NModal, NDescriptions,
  NDescriptionsItem, NForm, useMessage
} from 'naive-ui'
import {
  IconBriefcase as Briefcase,
  IconTrendingUp as TrendingUp,
  IconTarget as Target,
  IconSearch as Search,
  IconEye as Eye,
  IconMail as Mail,
  IconMapPin as MapPin,
  IconClock as Clock,
  IconCalendar as Calendar
} from '@tabler/icons-vue'

// 消息提示
const message = useMessage()

// 页面状态
const show_filter = ref(false)
const show_comp_modal = ref(false)
const show_pos_modal = ref(false)
const show_contact_modal = ref(false)
const current_page = ref(1)
const page_size = ref(10)

// 筛选条件
const filter_comp = ref('')
const filter_ind = ref('')
const filter_size = ref('')
const filter_loc = ref('')

// 选中的数据
const selected_comp = ref<any>(null)
const selected_pos = ref<any>(null)

// 联系表单
const contact_form = ref()
const contact_data = ref({
  subject: '',
  content: '',
  contact_info: ''
})

const contact_rules = {
  subject: { required: true, message: '请输入联系主题', trigger: 'blur' },
  content: { required: true, message: '请输入联系内容', trigger: 'blur' },
  contact_info: { required: true, message: '请输入联系方式', trigger: 'blur' }
}

// 统计数据
const market_stats = ref({
  total_comp: 156,
  total_pos: 423,
  new_pos: 28,
  match_pos: 15
})

// 筛选选项
const industry_opts = ref([
  { label: '互联网/IT', value: 'it' },
  { label: '金融/银行', value: 'finance' },
  { label: '制造业', value: 'manufacturing' },
  { label: '教育培训', value: 'education' },
  { label: '医疗健康', value: 'healthcare' },
  { label: '房地产', value: 'realestate' },
  { label: '零售/电商', value: 'retail' },
  { label: '其他', value: 'other' }
])

const size_opts = ref([
  { label: '初创企业(1-50人)', value: 'startup' },
  { label: '中小企业(51-200人)', value: 'small' },
  { label: '中型企业(201-1000人)', value: 'medium' },
  { label: '大型企业(1000+人)', value: 'large' }
])

const location_opts = ref([
  { label: '北京', value: 'beijing' },
  { label: '上海', value: 'shanghai' },
  { label: '广州', value: 'guangzhou' },
  { label: '深圳', value: 'shenzhen' },
  { label: '杭州', value: 'hangzhou' },
  { label: '成都', value: 'chengdu' },
  { label: '武汉', value: 'wuhan' },
  { label: '其他', value: 'other' }
])

// 企业数据
const company_list = ref([
  {
    id: 1,
    name: '腾讯科技',
    logo: '',
    industry: '互联网/IT',
    size: '大型企业(1000+人)',
    location: '深圳',
    description: '腾讯是一家世界领先的互联网科技公司，致力于通过技术丰富人们的数字生活。',
    full_desc: '腾讯成立于1998年，是中国最大的互联网综合服务提供商之一，也是中国服务用户最多的互联网企业之一。腾讯多元化的服务包括：社交和通信服务QQ及微信/WeChat、社交网络平台QQ空间、腾讯游戏旗下QQ游戏平台、门户网站腾讯网、腾讯新闻客户端和网络视频服务腾讯视频等。',
    update_time: '2024-01-15',
    rating: 4.5,
    found_date: '1998年11月',
    capital: '100亿人民币',
    nature: '民营企业',
    address: '广东省深圳市南山区科技园',
    contact_name: '张经理',
    contact_phone: '0755-86013388',
    contact_email: 'hr@tencent.com',
    website: 'https://www.tencent.com',
    positions: [
      {
        id: 101,
        title: '前端开发工程师',
        salary: '15K-30K',
        location: '深圳',
        exp_req: '3-5年',
        edu_req: '本科及以上',
        count: '5人',
        description: '负责Web前端开发，熟悉Vue.js框架',
        full_desc: '岗位职责：1. 负责公司产品的前端开发工作；2. 与UI设计师、后端工程师协作完成产品功能；3. 优化前端性能，提升用户体验；4. 参与技术方案设计和评审。',
        skills: ['Vue.js', 'JavaScript', 'TypeScript', 'CSS3'],
        benefits: ['五险一金', '年终奖', '带薪年假', '股票期权']
      },
      {
        id: 102,
        title: '产品经理',
        salary: '20K-35K',
        location: '深圳',
        exp_req: '3-5年',
        edu_req: '本科及以上',
        count: '2人',
        description: '负责产品规划和需求分析',
        full_desc: '岗位职责：1. 负责产品需求调研和分析；2. 制定产品发展规划和路线图；3. 协调各部门资源推进产品开发；4. 跟踪产品数据，持续优化产品体验。',
        skills: ['产品设计', '需求分析', 'Axure', 'SQL'],
        benefits: ['五险一金', '年终奖', '带薪年假', '培训机会']
      }
    ]
  },
  {
    id: 2,
    name: '阿里巴巴',
    logo: '',
    industry: '互联网/IT',
    size: '大型企业(1000+人)',
    location: '杭州',
    description: '阿里巴巴集团是以电子商务为核心的数字经济体，业务涵盖电商、云计算、数字媒体等。',
    full_desc: '阿里巴巴集团创立于1999年，是一家提供电子商务在线交易平台的公司，服务范围包括B2B贸易、网上零售、购物搜索引擎、第三方支付和云计算服务。集团的使命是让天下没有难做的生意。',
    update_time: '2024-01-14',
    rating: 4.3,
    found_date: '1999年9月',
    capital: '200亿人民币',
    nature: '民营企业',
    address: '浙江省杭州市余杭区文一西路969号',
    contact_name: '李经理',
    contact_phone: '0571-85022088',
    contact_email: 'hr@alibaba.com',
    website: 'https://www.alibaba.com',
    positions: [
      {
        id: 201,
        title: 'Java开发工程师',
        salary: '18K-35K',
        location: '杭州',
        exp_req: '3-5年',
        edu_req: '本科及以上',
        count: '10人',
        description: '负责后端服务开发，熟悉Spring框架',
        full_desc: '岗位职责：1. 负责核心业务系统的设计和开发；2. 参与系统架构设计和技术选型；3. 优化系统性能，保障服务稳定性；4. 参与代码评审和技术分享。',
        skills: ['Java', 'Spring', 'MySQL', 'Redis'],
        benefits: ['五险一金', '年终奖', '股票期权', '免费三餐']
      }
    ]
  }
])

// 计算属性
const filtered_comp = computed(() => {
  let result = company_list.value

  if (filter_comp.value) {
    result = result.filter(comp => 
      comp.name.toLowerCase().includes(filter_comp.value.toLowerCase())
    )
  }

  if (filter_ind.value) {
    result = result.filter(comp => comp.industry === industry_opts.value.find(opt => opt.value === filter_ind.value)?.label)
  }

  if (filter_size.value) {
    result = result.filter(comp => comp.size === size_opts.value.find(opt => opt.value === filter_size.value)?.label)
  }

  if (filter_loc.value) {
    result = result.filter(comp => comp.location === location_opts.value.find(opt => opt.value === filter_loc.value)?.label)
  }

  return result
})

const total_pages = computed(() => {
  return Math.ceil(filtered_comp.value.length / page_size.value)
})

// 方法
const refresh_data = () => {
  message.success('数据已刷新')
  // 这里可以调用API刷新数据
}

const reset_filter = () => {
  filter_comp.value = ''
  filter_ind.value = ''
  filter_size.value = ''
  filter_loc.value = ''
  message.info('筛选条件已重置')
}

const apply_filter = () => {
  current_page.value = 1
  message.success('筛选条件已应用')
}

const view_company = (company: any) => {
  selected_comp.value = company
  show_comp_modal.value = true
}

const view_position = (position: any) => {
  selected_pos.value = position
  show_pos_modal.value = true
}

const contact_company = (company: any) => {
  selected_comp.value = company
  contact_data.value = {
    subject: `关于${company.name}的合作咨询`,
    content: '',
    contact_info: ''
  }
  show_contact_modal.value = true
}

const submit_contact = async () => {
  try {
    await contact_form.value?.validate()
    // 这里调用API提交联系信息
    message.success('联系信息已发送，企业将尽快与您联系')
    show_contact_modal.value = false
  } catch (error) {
    message.error('请完善联系信息')
  }
}

const apply_position = () => {
  message.success('简历投递成功，请等待企业回复')
  show_pos_modal.value = false
}

const handle_page_size = (size: number) => {
  page_size.value = size
  current_page.value = 1
}

// 生命周期
onMounted(() => {
  // 初始化数据
})
</script>

<style scoped>
.talent-market-container {
  padding: 16px;
  font-family: "Microsoft YaHei", sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
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

.stats-section {
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;
}

.filter-section {
  margin-bottom: 24px;
}

.company-list-section {
  margin-bottom: 24px;
}

.company-card {
  transition: all 0.3s ease;
}

.company-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.company-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.company-details {
  margin-left: 12px;
}

.company-name {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.company-desc {
  color: #666;
  line-height: 1.6;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.position-card {
  transition: all 0.2s ease;
  cursor: pointer;
}

.position-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.position-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.position-title {
  font-weight: 600;
  color: #333;
}

.position-salary {
  color: #f56c6c;
  font-weight: 600;
}

.position-info {
  color: #666;
  font-size: 14px;
}

.position-desc {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.company-meta {
  color: #999;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.company-detail h4,
.position-detail h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.company-detail p,
.position-detail p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}
</style>