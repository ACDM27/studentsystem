<template>
  <div class="college-activity">
    <!-- 活动类型切换 -->
    <n-tabs type="line" v-model:value="active_tab">
      <n-tab-pane name="college" tab="学院活动">
        <!-- 顶部标题和功能按钮 -->
        <div class="page-header">
          <div class="title-section">
            <h1 class="page-title">学院活动</h1>
          </div>
          <div class="action-buttons">
            <n-button @click="show_records = true" size="medium">
              <template #icon>
                <n-icon><Book :size="18" /></n-icon>
              </template>
              我的活动记录
            </n-button>
            <n-button v-if="is_admin" type="primary" @click="show_publish = true" size="medium">
              <template #icon>
                <n-icon><Add :size="18" /></n-icon>
              </template>
              发布活动
            </n-button>
          </div>
        </div>

        <!-- 统计卡片 - 实时统计 -->
        <div class="stats-cards">
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.total_count }}</div>
              <div class="stat-label">任务总数</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.ongoing_count }}</div>
              <div class="stat-label">进行中</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.completed_count }}</div>
              <div class="stat-label">已结束</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.not_started_count }}</div>
              <div class="stat-label">未开始</div>
            </div>
          </n-card>
        </div>

        <!-- 筛选与搜索 -->
        <div class="filter-section">
          <div class="filter-left">
            <n-icon><Filter :size="18" /></n-icon>
            <span>筛选与搜索</span>
          </div>
          <div class="filter-right">
            <n-input placeholder="请输入今天标题或关键字" v-model:value="search_key" style="width: 300px;">
              <template #prefix>
                <n-icon><Search :size="18" /></n-icon>
              </template>
            </n-input>
            <n-select v-model:value="filter_type" placeholder="全部类型" style="width: 120px;" :options="type_opts" />
            <n-select v-model:value="filter_stat" placeholder="全部状态" style="width: 120px;" :options="status_opts" />
          </div>
        </div>

        <!-- 活动列表 -->
        <div class="activity-list">
          <div v-for="activity in filtered_acts" :key="activity.id" class="activity-item">
            <div class="activity-content">
              <div class="activity-main">
                <div class="activity-title-section">
                  <h3 class="activity-title">{{ activity.name }}</h3>
                  <div class="activity-tags">
                    <n-tag size="small" :type="get_stat_type(activity.status)">{{ activity.status }}</n-tag>
                  </div>
                </div>
                <div class="activity-info-grid">
                  <div class="info-item">
                    <span class="info-label">报名时间：</span>
                    <span class="info-value">{{ activity.start_time }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">截止时间：</span>
                    <span class="info-value">{{ activity.end_time }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">参与人数：</span>
                    <span class="info-value">{{ activity.current_num }}/{{ activity.max_num }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">获取学分：</span>
                    <span class="info-value">{{ activity.credits }} 分</span>
                  </div>
                  <div v-if="active_tab === 'college'" class="info-item">
                    <span class="info-label">组织单位：</span>
                    <span class="info-value">{{ activity.organizer }}</span>
                  </div>
                </div>
              </div>
              <div class="activity-actions">
                <n-button @click="view_detail(activity.id)" size="medium">查看详情</n-button>
                <n-button
                  type="primary"
                  @click="join_act(activity.id)"
                  :disabled="!can_join(activity)"
                  size="medium"
                >
                  报名参加
                </n-button>
              </div>
            </div>
          </div>
        </div>
      </n-tab-pane>

      <n-tab-pane name="campus" tab="校园活动">
        <!-- 顶部标题和功能按钮 -->
        <div class="page-header">
          <div class="title-section">
            <h1 class="page-title">校园活动</h1>
          </div>
          <div class="action-buttons">
            <n-button @click="show_records = true" size="medium">
              <template #icon>
                <n-icon><Book :size="18" /></n-icon>
              </template>
              我的活动记录
            </n-button>
            <n-button v-if="is_admin" type="primary" @click="show_publish = true" size="medium">
              <template #icon>
                <n-icon><Add :size="18" /></n-icon>
              </template>
              发布活动
            </n-button>
          </div>
        </div>

        <!-- 统计卡片 - 实时统计 -->
        <div class="stats-cards">
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.total_count }}</div>
              <div class="stat-label">任务总数</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.ongoing_count }}</div>
              <div class="stat-label">进行中</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.completed_count }}</div>
              <div class="stat-label">已结束</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.not_started_count }}</div>
              <div class="stat-label">未开始</div>
            </div>
          </n-card>
        </div>

        <!-- 筛选与搜索 -->
        <div class="filter-section">
          <div class="filter-left">
            <n-icon><Filter :size="18" /></n-icon>
            <span>筛选与搜索</span>
          </div>
          <div class="filter-right">
            <n-input placeholder="请输入今天标题或关键字" v-model:value="search_key" style="width: 300px;">
              <template #prefix>
                <n-icon><Search :size="18" /></n-icon>
              </template>
            </n-input>
            <n-select v-model:value="filter_type" placeholder="全部类型" style="width: 120px;" :options="type_opts" />
            <n-select v-model:value="filter_stat" placeholder="全部状态" style="width: 120px;" :options="status_opts" />
          </div>
        </div>

        <!-- 活动列表 -->
        <div class="activity-list">
          <div v-for="activity in filtered_acts" :key="activity.id" class="activity-item">
            <div class="activity-content">
              <div class="activity-main">
                <div class="activity-title-section">
                  <h3 class="activity-title">{{ activity.name }}</h3>
                  <div class="activity-tags">
                    <n-tag size="small" :type="get_stat_type(activity.status)">{{ activity.status }}</n-tag>
                  </div>
                </div>
                <div class="activity-info-grid">
                  <div class="info-item">
                    <span class="info-label">报名时间：</span>
                    <span class="info-value">{{ activity.start_time }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">截止时间：</span>
                    <span class="info-value">{{ activity.end_time }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">参与人数：</span>
                    <span class="info-value">{{ activity.current_num }}/{{ activity.max_num }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">获取学分：</span>
                    <span class="info-value">{{ activity.credits }} 分</span>
                  </div>
                </div>
              </div>
              <div class="activity-actions">
                <n-button @click="view_detail(activity.id)" size="medium">查看详情</n-button>
                <n-button
                  type="primary"
                  @click="join_act(activity.id)"
                  :disabled="!can_join(activity)"
                  size="medium"
                >
                  报名参加
                </n-button>
              </div>
            </div>
          </div>
        </div>
      </n-tab-pane>

      <n-tab-pane name="association" tab="协会活动">
        <!-- 顶部标题和功能按钮 -->
        <div class="page-header">
          <div class="title-section">
            <h1 class="page-title">协会活动</h1>
          </div>
          <div class="action-buttons">
            <n-button @click="show_records = true" size="medium">
              <template #icon>
                <n-icon><Book /></n-icon>
              </template>
              我的活动记录
            </n-button>
            <n-button v-if="is_admin" type="primary" @click="show_publish = true" size="medium">
              <template #icon>
                <n-icon><Add /></n-icon>
              </template>
              发布活动
            </n-button>
          </div>
        </div>

        <!-- 统计卡片 - 实时统计 -->
        <div class="stats-cards">
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.total_count }}</div>
              <div class="stat-label">任务总数</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.ongoing_count }}</div>
              <div class="stat-label">进行中</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.completed_count }}</div>
              <div class="stat-label">已结束</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.not_started_count }}</div>
              <div class="stat-label">未开始</div>
            </div>
          </n-card>
        </div>

        <!-- 筛选与搜索 -->
        <div class="filter-section">
          <div class="filter-left">
            <n-icon><Filter :size="18" /></n-icon>
            <span>筛选与搜索</span>
          </div>
          <div class="filter-right">
            <n-input placeholder="请输入今天标题或关键字" v-model:value="search_key" style="width: 300px;">
              <template #prefix>
                <n-icon><Search :size="18" /></n-icon>
              </template>
            </n-input>
            <n-select v-model:value="filter_type" placeholder="全部类型" style="width: 120px;" :options="type_opts" />
            <n-select v-model:value="filter_stat" placeholder="全部状态" style="width: 120px;" :options="status_opts" />
          </div>
        </div>

        <!-- 活动列表 -->
        <div class="activity-list">
          <div v-for="activity in filtered_acts" :key="activity.id" class="activity-item">
            <div class="activity-content">
              <div class="activity-main">
                <div class="activity-title-section">
                  <h3 class="activity-title">{{ activity.name }}</h3>
                  <div class="activity-tags">
                    <n-tag size="small" :type="get_stat_type(activity.status)">{{ activity.status }}</n-tag>
                  </div>
                </div>
                <div class="activity-info-grid">
                  <div class="info-item">
                    <span class="info-label">报名时间：</span>
                    <span class="info-value">{{ activity.start_time }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">截止时间：</span>
                    <span class="info-value">{{ activity.end_time }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">参与人数：</span>
                    <span class="info-value">{{ activity.current_num }}/{{ activity.max_num }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">获取学分：</span>
                    <span class="info-value">{{ activity.credits }} 分</span>
                  </div>
                  <div v-if="active_tab === 'association'" class="info-item">
                    <span class="info-label">协会名称：</span>
                    <span class="info-value">{{ activity.association }}</span>
                  </div>
                </div>
              </div>
              <div class="activity-actions">
                <n-button @click="view_detail(activity.id)" size="medium">查看详情</n-button>
                <n-button
                  type="primary"
                  @click="join_act(activity.id)"
                  :disabled="!can_join(activity)"
                  size="medium"
                >
                  报名参加
                </n-button>
              </div>
            </div>
          </div>
        </div>
      </n-tab-pane>

      <n-tab-pane name="committee" tab="校团委活动">
        <!-- 顶部标题和功能按钮 -->
        <div class="page-header">
          <div class="title-section">
            <h1 class="page-title">校团委活动</h1>
          </div>
          <div class="action-buttons">
            <n-button @click="show_records = true" size="medium">
              <template #icon>
                <n-icon><Book /></n-icon>
              </template>
              我的活动记录
            </n-button>
            <n-button v-if="is_admin" type="primary" @click="show_publish = true" size="medium">
              <template #icon>
                <n-icon><Add /></n-icon>
              </template>
              发布活动
            </n-button>
          </div>
        </div>

        <!-- 统计卡片 - 实时统计 -->
        <div class="stats-cards">
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.total_count }}</div>
              <div class="stat-label">任务总数</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.ongoing_count }}</div>
              <div class="stat-label">进行中</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.completed_count }}</div>
              <div class="stat-label">已结束</div>
            </div>
          </n-card>
          <n-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ stats.not_started_count }}</div>
              <div class="stat-label">未开始</div>
            </div>
          </n-card>
        </div>

        <!-- 筛选与搜索 -->
        <div class="filter-section">
          <div class="filter-left">
            <n-icon><Filter :size="18" /></n-icon>
            <span>筛选与搜索</span>
          </div>
          <div class="filter-right">
            <n-input placeholder="请输入今天标题或关键字" v-model:value="search_key" style="width: 300px;">
              <template #prefix>
                <n-icon><Search :size="18" /></n-icon>
              </template>
            </n-input>
            <n-select v-model:value="filter_type" placeholder="全部类型" style="width: 120px;" :options="type_opts" />
            <n-select v-model:value="filter_stat" placeholder="全部状态" style="width: 120px;" :options="status_opts" />
          </div>
        </div>

        <!-- 活动列表 -->
        <div class="activity-list">
          <div v-for="activity in filtered_acts" :key="activity.id" class="activity-item">
            <div class="activity-content">
              <div class="activity-main">
                <div class="activity-title-section">
                  <h3 class="activity-title">{{ activity.name }}</h3>
                  <div class="activity-tags">
                    <n-tag size="small" :type="get_stat_type(activity.status)">{{ activity.status }}</n-tag>
                  </div>
                </div>
                <div class="activity-info-grid">
                  <div class="info-item">
                    <span class="info-label">报名时间：</span>
                    <span class="info-value">{{ activity.start_time }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">截止时间：</span>
                    <span class="info-value">{{ activity.end_time }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">参与人数：</span>
                    <span class="info-value">{{ activity.current_num }}/{{ activity.max_num }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">获取学分：</span>
                    <span class="info-value">{{ activity.credits }} 分</span>
                  </div>
                  <div v-if="active_tab === 'committee'" class="info-item">
                    <span class="info-label">委员会：</span>
                    <span class="info-value">{{ activity.committee_name }}</span>
                  </div>
                </div>
              </div>
              <div class="activity-actions">
                <n-button @click="view_detail(activity.id)" size="medium">查看详情</n-button>
                <n-button
                  type="primary"
                  @click="join_act(activity.id)"
                  :disabled="!can_join(activity)"
                  size="medium"
                >
                  报名参加
                </n-button>
              </div>
            </div>
          </div>
        </div>
      </n-tab-pane>
    </n-tabs>

    <!-- 活动详情弹窗 -->
    <n-modal v-model:show="show_detail">
      <n-card title="活动详情" style="width: 600px">
        <template #header-extra>
          <n-button circle @click="show_detail = false">
            <template #icon>
              <n-icon><Close :size="18" /></n-icon>
            </template>
          </n-button>
        </template>
        <div v-if="current_act">
          <h2>{{ current_act.name }}</h2>
          <div class="detail-content">
            <p>活动时间：{{ current_act.activity_time }}</p>
            <p>活动地点：{{ current_act.location }}</p>
            <p>活动描述：{{ current_act.description }}</p>
            <p>主办单位：{{ current_act.organizer }}</p>
            <p>联系方式：{{ current_act.contact }}</p>
          </div>
        </div>
      </n-card>
    </n-modal>

    <!-- 发布活动弹窗 -->
    <n-modal v-model:show="show_publish">
      <n-card title="发布活动" style="width: 600px">
        <n-form
          ref="formRef"
          :model="act_form"
          :rules="rules"
        >
          <n-form-item label="活动名称" path="name">
            <n-input v-model:value="act_form.name" />
          </n-form-item>
          <n-form-item label="活动类型" path="type">
            <n-select v-model:value="act_form.type" :options="act_types" />
          </n-form-item>
          <n-form-item label="报名时间" path="reg_time">
            <n-date-picker
              v-model:value="act_form.reg_time"
              type="datetimerange"
              clearable
            />
          </n-form-item>
          <n-form-item label="活动时间" path="activity_time">
            <n-date-picker
              v-model:value="act_form.activity_time"
              type="datetime"
              clearable
            />
          </n-form-item>
          <n-form-item label="活动地点" path="location">
            <n-input v-model:value="act_form.location" />
          </n-form-item>
          <n-form-item label="参与人数" path="max_num">
            <n-input-number v-model:value="act_form.max_num" />
          </n-form-item>
          <n-form-item label="活动学分" path="credits">
            <n-input-number v-model:value="act_form.credits" />
          </n-form-item>
          <n-form-item label="活动描述" path="description">
            <n-input
              v-model:value="act_form.description"
              type="textarea"
              :rows="3"
            />
          </n-form-item>
        </n-form>
        <template #footer>
          <n-space justify="end">
            <n-button @click="show_publish = false">取消</n-button>
            <n-button type="primary" @click="publish_act">发布</n-button>
          </n-space>
        </template>
      </n-card>
    </n-modal>

    <!-- 我的活动记录抽屉 -->
    <n-drawer v-model:show="show_records" width="500">
      <n-drawer-content title="我的活动记录">
        <n-empty v-if="my_records.length === 0" description="暂无活动记录">
          <template #extra>
            <n-button size="small" @click="show_records = false">
              返回
            </n-button>
          </template>
        </n-empty>
        <n-list v-else>
          <n-list-item v-for="record in my_records" :key="record.id">
            <n-thing :title="record.activity_name">
              <template #description>
                <n-space vertical size="small">
                  <div>
                    <n-tag size="small" :type="record.status === '已参加' ? 'success' : 'warning'" style="margin-right: 8px">
                      {{ record.status }}
                    </n-tag>
                    <n-tag size="small" type="info">{{ activity_type_mapping[record.activity_type] || record.activity_type }}</n-tag>
                  </div>
                  <p style="margin: 0; color: #666;">参加时间：{{ record.join_time }}</p>
                  <p style="margin: 0; color: #666;">获得学分：{{ record.credits }} 分</p>
                </n-space>
              </template>
            </n-thing>
          </n-list-item>
        </n-list>
        <template #footer>
          <n-button block @click="fetch_records">
            刷新记录
          </n-button>
        </template>
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Add, Book, Filter, Search, Close } from '@vicons/ionicons5'
import { useMessage, type FormRules } from 'naive-ui'
import axios from 'axios'
import request from '@/utils/request'

// 使用系统统一的请求实例
const apiClient = request


// 类型定义
interface Activity {
  id: number
  name: string
  status: string
  category: string
  activity_type: string
  start_time: string
  end_time: string
  registration_start_time: string
  registration_end_time: string
  activity_time: string
  location: string
  current_num: number
  max_num: number
  credits: number
  description: string
  organizer?: string
  association?: string
  committee_name?: string
  contact: string
}

interface ActivityRecord {
  id: number
  activity_name: string
  join_time: string
  status: string
  credits: number
  activity_type: string
}

interface ActivityForm {
  name: string
  type: string
  reg_time: number[] | null
  activity_time: number | null
  location: string
  max_num: number
  credits: number
  description: string
}

interface SelectOption {
  label: string
  value: string
}

// 路由和消息
const route = useRoute()
const message = useMessage()

// 状态变量
const active_tab = ref('college')
const activities = ref<Activity[]>([])
const show_detail = ref(false)
const show_publish = ref(false)
const show_records = ref(false)
const current_act = ref<Activity | null>(null)
const is_admin = ref(false)
const my_records = ref<ActivityRecord[]>([])

// 搜索和筛选
const search_key = ref('')
const filter_type = ref('')
const filter_stat = ref('')

// 筛选选项
const type_opts: SelectOption[] = [
  { label: '全部类型', value: '' },
  { label: '学术讲座', value: 'lecture' },
  { label: '竞赛活动', value: 'competition' },
  { label: '文艺活动', value: 'cultural' },
  { label: '志愿服务', value: 'volunteer' }
]

const status_opts: SelectOption[] = [
  { label: '全部状态', value: '' },
  { label: '报名中', value: '报名中' },
  { label: '进行中', value: '进行中' },
  { label: '已结束', value: '已结束' }
]

// 统计数据对象 - 实时计算活动统计信息
const stats = computed(() => {
  const all_activities = activities.value
  return {
    total_count: all_activities.length,
    ongoing_count: all_activities.filter(a => a.status === '进行中').length,
    completed_count: all_activities.filter(a => a.status === '已结束').length,
    not_started_count: all_activities.filter(a => a.status === '未开始').length
  }
})

// 计算属性：过滤后的活动列表
const filtered_acts = computed(() => {
  let filtered = activities.value

  // 关键字搜索
  if (search_key.value) {
    filtered = filtered.filter(activity =>
      activity.name.toLowerCase().includes(search_key.value.toLowerCase()) ||
      activity.description.toLowerCase().includes(search_key.value.toLowerCase())
    )
  }

  // 类型筛选
  if (filter_type.value) {
    filtered = filtered.filter(activity => activity.category === filter_type.value)
  }
  
  // 状态筛选
  if (filter_stat.value) {
    filtered = filtered.filter(activity => activity.status === filter_stat.value)
  }

  return filtered
})

// 表单相关
const act_form = ref<ActivityForm>({
  name: '',
  type: '',
  reg_time: null,
  activity_time: null,
  location: '',
  max_num: 0,
  credits: 0,
  description: ''
})

const act_types: SelectOption[] = [
  { label: '学院活动', value: 'college' },
  { label: '校园活动', value: 'campus' },
  { label: '协会活动', value: 'association' },
  { label: '校团委活动', value: 'committee' }
]

const rules: FormRules = {
  name: { required: true, message: '请输入活动名称', trigger: 'blur' },
  type: { required: true, message: '请选择活动类型', trigger: 'change' },
  reg_time: { required: true, message: '请选择报名时间', trigger: 'change' },
  activity_time: { required: true, message: '请选择活动时间', trigger: 'change' },
  location: { required: true, message: '请输入活动地点', trigger: 'blur' },
  max_num: {
    required: true,
    type: 'number',
    message: '请输入参与人数',
    trigger: 'change',
    validator: (rule: any, value: number) => {
      if (!value || value <= 0) {
        return new Error('参与人数必须大于0')
      }
      if (value > 1000) {
        return new Error('参与人数不能超过1000')
      }
      return true
    }
  },
  credits: {
    required: true,
    type: 'number',
    message: '请输入活动学分',
    trigger: 'change',
    validator: (rule: any, value: number) => {
      if (!value || value <= 0) {
        return new Error('活动学分必须大于0')
      }
      if (value > 10) {
        return new Error('活动学分不能超过10分')
      }
      return true
    }
  },
  description: { required: true, message: '请输入活动描述', trigger: 'blur' }
}

// 方法
const activity_type_mapping: Record<string, string> = {
  'collegeActivities': '学院活动',
  'campusActivities': '校园活动',
  'associationActivities': '协会活动',
  'youthLeagueCommitteeActivities': '校团委活动'
}

// 根据时间判断活动状态
const getActivityStatus = (registration_start_time: string, registration_end_time: string, activity_time: string): string => {
  const now = new Date();
  const regStartTime = registration_start_time ? new Date(registration_start_time) : null;
  const regEndTime = registration_end_time ? new Date(registration_end_time) : null;
  const activityTime = activity_time ? new Date(activity_time) : null;
  
  // 如果没有设置时间，返回默认状态
  if (!regStartTime || !regEndTime) {
    return '未开始';
  }
  
  // 判断活动状态
  if (now < regStartTime) {
    return '未开始';
  } else if (now >= regStartTime && now <= regEndTime) {
    return '报名中';
  } else if (activityTime && now <= activityTime) {
    return '进行中';
  } else {
    return '已结束';
  }
}

const get_stat_type = (status: string): string => {
  const status_map: Record<string, string> = {
    '报名中': 'success',
    '已结束': 'error',
    '进行中': 'warning',
    '未开始': 'info'
  }
  return status_map[status] || 'default'
}

const can_join = (activity: Activity): boolean => {
  return activity.status === '报名中' &&
    activity.current_num < activity.max_num
}

const view_detail = async (id: number): Promise<void> => {
  try {
    // 调用API获取活动详情
    const item: any = await apiClient.get(`/api/v1/activities/${id}`)
    
    if (item) {
      // 将API返回的数据转换为组件使用的格式

      current_act.value = {
        id: item.id,
        name: item.name,
        status: getActivityStatus(item.registration_start_time, item.registration_end_time, item.activity_time),
        category: item.activity_type === 'collegeActivities' ? 'academic' :
                  item.activity_type === 'campusActivities' ? 'cultural' :
                  item.activity_type === 'associationActivities' ? 'cultural' : 'volunteer',
        activity_type: item.activity_type || '',
        start_time: item.registration_start_time ? new Date(item.registration_start_time).toLocaleDateString() : '',
        end_time: item.registration_end_time ? new Date(item.registration_end_time).toLocaleDateString() : '',
        registration_start_time: item.registration_start_time || '',
        registration_end_time: item.registration_end_time || '',
        activity_time: item.activity_time || '',
        location: item.location || '',
        current_num: item.current_participants || 0,
        max_num: item.max_participants,
        credits: item.credits,
        description: item.description || '',
        organizer: item.collegename || '',
        association: item.associationname || '',
        committee_name: item.youthLeaguename || '',
        contact: item.contact || ''
      }
      show_detail.value = true
    } else {
      message.error('获取活动详情失败：数据格式错误')
    }
  } catch (error) {
    message.error('获取活动详情失败')
    console.error('获取活动详情失败:', error)
  }
}

const join_act = async (id: number): Promise<void> => {
  try {
    // 调用API进行活动报名
    await apiClient.post(`/api/v1/activities/${id}/join`)

    message.success('报名成功')
    // 刷新活动列表
    fetch_acts()
  } catch (error) {
    message.error('报名失败')
    console.error('报名失败:', error)
  }
}

const publish_act = async (): Promise<void> => {
  try {
    // 将表单数据转换为API需要的格式
    const activityData = {
      name: act_form.value.name,
      registration_start_time: act_form.value.reg_time ? new Date(act_form.value.reg_time[0]).toISOString() : '',
      registration_end_time: act_form.value.reg_time ? new Date(act_form.value.reg_time[1]).toISOString() : '',
      max_participants: act_form.value.max_num,
      credits: act_form.value.credits,
      activity_type: act_form.value.type === 'college' ? 'collegeActivities' :
                    act_form.value.type === 'campus' ? 'campusActivities' :
                    act_form.value.type === 'association' ? 'associationActivities' : 'youthLeagueCommitteeActivities',
      activitystatus: 'not_started',
      location: act_form.value.location,
      description: act_form.value.description
    }
    
    // 调用API发布活动
    await apiClient.post('/api/v1/activities', activityData)

    message.success('发布成功')
    show_publish.value = false
    // 刷新活动列表
    fetch_acts()
  } catch (error) {
    message.error('发布失败')
    console.error('发布失败:', error)
  }
}


const fetch_acts = async (): Promise<void> => {
  try {
    // 根据当前选中的标签页构建查询参数
    let params = {}
    
    // 根据标签页设置不同的查询参数
    switch (active_tab.value) {
      case 'college':
        params = { 'filters[activity_type][$eq]': 'collegeActivities' }
        break
      case 'campus':
        params = { 'filters[activity_type][$eq]': 'campusActivities' }
        break
      case 'association':
        params = { 'filters[activity_type][$eq]': 'associationActivities' }
        break
      case 'committee':
        params = { 'filters[activity_type][$eq]': 'youthLeagueCommitteeActivities' }
        break
      default:
        break
    }
    
    // 发送GET请求获取活动数据
    const response: any = await apiClient.get('/api/v1/activities', { params })
    
    // 处理响应数据
    if (response && response.list) {
      // 将API返回的数据转换为组件使用的格式
      activities.value = response.list.map((item: any) => ({


        id: item.id,
        name: item.name,
        status: getActivityStatus(item.registration_start_time, item.registration_end_time, item.activity_time),
        category: item.activity_type === 'collegeActivities' ? 'academic' :
                  item.activity_type === 'campusActivities' ? 'cultural' :
                  item.activity_type === 'associationActivities' ? 'cultural' : 'volunteer',
        activity_type: item.activity_type,
        start_time: item.registration_start_time ? new Date(item.registration_start_time).toLocaleDateString() : '',
        end_time: item.registration_end_time ? new Date(item.registration_end_time).toLocaleDateString() : '',
        activity_time: item.activity_time || '',
        location: item.location || '',
        current_num: item.current_participants || 0,
        max_num: item.max_participants,
        credits: item.credits,
        description: item.description || '',
        organizer: item.collegename || '',
        association: item.associationname || '',
        committee_name: item.youthLeaguename || '',
        contact: item.contact || ''
      }))
    } else {
      activities.value = []
    }
  } catch (error) {
    message.error('获取活动列表失败')
    console.error('获取活动失败:', error)
    activities.value = []
  }
}

const fetch_records = async (): Promise<void> => {
  try {
    const response: any = await apiClient.get('/api/v1/activities')
    
    // 处理响应数据
    if (response && response.list) {
      // 将API返回的数据转换为组件使用的格式
      my_records.value = response.list.map((item: any) => ({


        id: item.id,
        activity_name: item.activity_name || item.name,
        join_time: item.join_time ? new Date(item.join_time).toLocaleDateString() : '',
        status: item.status === 'registered' ? '已报名' : 
                item.status === 'participated' ? '已参加' : '已取消',
        credits: item.credits,
        activity_type: item.activity_type
      }))
    } else {
      my_records.value = []
    }
  } catch (error) {
    message.error('获取活动记录失败')
    console.error('获取活动记录失败:', error)
    
    // 如果API尚未实现，使用模拟数据（仅用于开发阶段）
    my_records.value = [
      {
        id: 1,
        activity_name: '计算机学院编程大赛',
        join_time: '2024-01-16 10:30',
        status: '已报名',
        credits: 2,
        activity_type: '学院活动'
      },
      {
        id: 2,
        activity_name: '学院学术讲座：人工智能前沿',
        join_time: '2024-01-12 14:20',
        status: '已参加',
        credits: 1,
        activity_type: '学院活动'
      }
    ]
  }
}

// 监听活动类型切换
watch(active_tab, () => {
  fetch_acts()
})

// 定期更新活动状态（每分钟检查一次）
let statusUpdateInterval: number | null = null;

onMounted(() => {
  // 设置定时器，每分钟更新一次活动状态
  statusUpdateInterval = window.setInterval(() => {
    // 更新活动列表中的状态
    if (activities.value.length > 0) {
      activities.value = activities.value.map(activity => ({
        ...activity,
        status: getActivityStatus(activity.registration_start_time, activity.registration_end_time, activity.activity_time)
      }))
    }
    
    // 更新当前查看的活动状态
    if (current_act.value) {
      current_act.value = {
        ...current_act.value,
        status: getActivityStatus(current_act.value.registration_start_time, current_act.value.registration_end_time, current_act.value.activity_time)
      }
    }
  }, 60000) // 60000毫秒 = 1分钟
})

onUnmounted(() => {
  // 组件卸载时清除定时器
  if (statusUpdateInterval !== null) {
    clearInterval(statusUpdateInterval)
  }
})

// 根据菜单key切换到对应的标签页
const switch_tab = (menu_key: string): void => {
  const menu_map: Record<string, string> = {
    'college_act': 'college',
    'campus_act': 'campus', 
    'assoc_act': 'association',
    'youth_act': 'committee'
  }
  
  if (menu_map[menu_key]) {
    active_tab.value = menu_map[menu_key]
  }
}

// 监听路由变化，根据来源菜单切换标签页
watch(() => route.query.from, (new_from) => {
  if (new_from) {
    switch_tab(new_from as string)
  }
}, { immediate: true })

// 组件挂载时获取数据
onMounted(() => {
  // 检查路由参数，如果有来源菜单则切换到对应标签页
  if (route.query.from) {
    switch_tab(route.query.from as string)
  }
  
  fetch_acts()
  fetch_records()
})
</script>

<style scoped>
.college-activity {
  padding: 24px;
  background: #f8f9fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding: 20px 0;
}

.title-section {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.action-buttons {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 12px;
  border: 1px solid #e8e8e8;
  background: #fff;
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.stat-content {
  text-align: center;
  padding: 20px;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #1890ff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

/* 筛选搜索区域 */
.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: #fff;
  border-radius: 12px;
  margin-bottom: 24px;
  border: 1px solid #e8e8e8;
}

.filter-left {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.filter-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 活动列表 */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;
}

.activity-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.activity-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
}

.activity-main {
  flex: 1;
  margin-right: 24px;
}

.activity-title-section {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.activity-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
  margin-right: 12px;
}

.activity-tags {
  display: flex;
  gap: 8px;
}

.activity-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px 24px;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-label {
  font-size: 14px;
  color: #666;
  margin-right: 8px;
  min-width: 80px;
}

.info-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.activity-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 120px;
}

/* 标签页样式优化 */
:deep(.n-tabs .n-tab-pane) {
  padding-top: 0;
}

:deep(.n-tabs .n-tabs-nav) {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 8px;
  margin-bottom: 24px;
  border: 1px solid #e8e8e8;
}

:deep(.n-tabs .n-tabs-tab) {
  border-radius: 8px;
  font-weight: 500;
}

/* 按钮样式优化 */
:deep(.n-button) {
  border-radius: 8px;
  font-weight: 500;
}

/* 卡片内容样式 */
:deep(.n-card) {
  border-radius: 12px;
}

:deep(.n-card .n-card__content) {
  padding: 20px;
  overflow: hidden;
  box-sizing: border-box;
}

/* 抽屉样式优化 */
:deep(.n-drawer .n-drawer-content) {
  background: #fafafa;
}

:deep(.n-drawer .n-drawer-header) {
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
}

/* 详情弹窗样式 */
.detail-content {
  margin-top: 20px;
  line-height: 1.8;
}

.detail-content p {
  margin: 12px 0;
  color: #555;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .activity-info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .college-activity {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .filter-section {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .filter-right {
    width: 100%;
    flex-wrap: wrap;
  }
  
  .activity-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .activity-main {
    margin-right: 0;
  }
  
  .activity-actions {
    flex-direction: row;
    width: 100%;
    justify-content: flex-end;
  }
  
  .activity-info-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .activity-actions {
    flex-direction: column;
  }
}
</style>