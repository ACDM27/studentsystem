<template>
    <div class="courses-page">
      <!-- 顶部功能区 -->
      <div class="header-section">
        <div class="title-section">
          <h2>作业管理</h2>
          <p class="subtitle">查看和管理您的所有课程作业</p>
        </div>
        <div class="action-buttons">
          <n-button class="action-btn" type="primary" ghost @click="viewSubmissionHistory">
            <template #icon>
              <n-icon><IconHistory :size="24" /></n-icon>
            </template>
            提交记录
          </n-button>
          <n-button class="action-btn" type="primary" ghost>
            <template #icon>
              <n-icon><IconBulb :size="24" /></n-icon>
            </template>
            智能助手
          </n-button>
          <n-button class="action-btn" type="primary" ghost>
            <template #icon>
              <n-icon><IconBell :size="24" /></n-icon>
            </template>
            提醒设置
          </n-button>
        </div>
      </div>
  
      <!-- 导航标签页 -->
      <n-tabs type="line" animated>
        <n-tab-pane name="list" tab="作业列表">
          <!-- 搜索和筛选区域 -->
          <div class="search-filter-section">
            <n-input-group ref="searchInputGroup">
              <n-input placeholder="搜索作业标题、课程或教师" clearable>
                <template #prefix>
                  <n-icon><IconSearch :size="24" /></n-icon>
                </template>
              </n-input>
            </n-input-group>
            <div class="filters">
              <n-select placeholder="课程" clearable />
              <n-select placeholder="状态" clearable />
              <n-select placeholder="优先级" clearable />
              <n-button type="default" ghost>清除筛选</n-button>
            </div>
          </div>
  
          <!-- 作业卡片列表 -->
          <div class="assignments-grid">
            <n-card v-for="assignment in assignments" :key="assignment.id" class="assignment-card">
              <template #header>
                <div class="card-header">
                  <h3>{{ assignment.courseName }}</h3>
                  <n-tag :type="getStatusType(assignment.status)">{{ assignment.status }}</n-tag>
                </div>
              </template>
              <div class="card-content">
                <div class="info-row">
                  <span class="label">指导老师：</span>
                  <span>{{ assignment.teacher }}</span>
                </div>
                <div class="info-row requirements-row">
                  <span class="label">作业要求：</span>
                  <p>{{ assignment.requirements }}</p>
                </div>
                <div class="info-row time-info">
                  <div class="time-item">
                    <span class="label">发布时间：</span>
                    <span>{{ formatDate(assignment.publishDate) }}</span>
                  </div>
                  <div class="time-item">
                    <span class="label">截止时间：</span>
                    <span>{{ assignment.deadline }}</span>
                  </div>
                </div>
                <div class="info-row time-info">
                  <div class="time-item">
                    <span class="label">可提交次数：</span>
                    <span>{{ assignment.maxSubmissions }}</span>
                  </div>
                  <div class="time-item">
                    <!-- 保留空白区域以保持布局一致性 -->
                  </div>
                </div>
              </div>
              <template #footer>
                <div class="card-footer">
                  <div class="attachments">
                    <n-button text>
                      <template #icon>
                        <n-icon><IconFileDownload :size="24" /></n-icon>
                      </template>
                      下载附件
                    </n-button>
                  </div>
                  <div class="action-buttons">
                    <n-button type="info" ghost @click="viewAssignmentDetail(assignment)">查看详情</n-button>
                    <n-button 
                      :type="assignment.status === '已截止' ? 'default' : 'primary'" 
                      :disabled="assignment.status === '已截止'"
                      @click="submitAssignment(assignment)"
                    >
                      {{ assignment.status === '已截止' ? '已截止' : '提交作业' }}
                    </n-button>
                  </div>
                </div>
              </template>
            </n-card>
          </div>
        </n-tab-pane>
        <n-tab-pane name="calendar" tab="日历视图" />
        <n-tab-pane name="analysis" tab="数据分析" />
        <n-tab-pane name="history" tab="提交记录" />
      </n-tabs>
    </div>
    
    <!-- 作业详情组件 -->
    <assignment-detail
      v-model:show="detailModalVisible"
      :assignment="currentAssignment"
      @refresh="fetchAssignments"
    />
  </template>
  
  <script setup lang="ts">
import { ref, onMounted } from 'vue'
import { IconBulb, IconBell, IconSearch, IconFileDownload, IconHistory } from '@tabler/icons-vue'
import { getAssignments } from '../../../apis'
import type { IGetAssignmentsResp } from '../../../types/api'
import { NInputGroup, useMessage } from 'naive-ui'
import AssignmentDetail from './assignment-detail.vue'

// 定义组件内部使用的作业数据结构
interface Assignment {
  id: number
  courseName: string
  teacher: string
  requirements: string
  publishDate: string
  deadline: string
  maxSubmissions: string
  status: string
}

// 声明响应式的作业数据
const assignments = ref<Assignment[]>([])

// 根据时间判断作业状态
const calculateAssignmentStatus = (publishDate: string, deadline: string): string => {
  const now = new Date()
  const publish = new Date(publishDate)
  const due = new Date(deadline)
  
  // 如果当前时间小于发布时间，显示"未开始"
  if (now < publish) {
    return '未开始'
  }
  
  // 如果当前时间超过截止时间，显示"已截止"
  if (now > due) {
    return '已截止'
  }
  
  // 如果在发布时间和截止时间之间，显示"待提交"
  return '待提交'
}
    
  // 从API获取作业数据
const fetchAssignments = async () => {
  try {
    const response = await getAssignments()
    if (response && response.data) {
      // 将API返回的数据映射到assignments数组
      assignments.value = response.data.map(item => {
        const publishDate = item.createdAt || '2024-01-01'
        const deadline = item.deadline || '2024-12-31'
        
        return {
          id: item.id,
          courseName: item.title,
          teacher: item.teachers_name || '未指定',
          requirements: item.assignmentcontent || item.description || '暂无要求',
          publishDate: publishDate,
          deadline: deadline,
          maxSubmissions: '不限次数',
          status: calculateAssignmentStatus(publishDate, deadline) // 使用新的状态计算逻辑
        }
      }) as Assignment[]
    }
  } catch (error) {
    console.error('获取作业数据失败:', error)
  }
}
  
  // 搜索输入组的引用
const searchInputGroup = ref(null)

// 作业详情弹窗
const detailModalVisible = ref(false)
const currentAssignment = ref<Assignment | null>(null)
const message = useMessage()

// 查看作业详情
const viewAssignmentDetail = (assignment: Assignment) => {
  currentAssignment.value = assignment
  detailModalVisible.value = true
}

// 提交作业
const submitAssignment = (assignment: Assignment) => {
  // 检查作业状态
  if (assignment.status === '已截止') {
    message.warning('该作业已截止，无法提交')
    return
  }
  
  currentAssignment.value = assignment
  detailModalVisible.value = true
}

// 查看提交记录
const viewSubmissionHistory = () => {
  message.info('提交记录功能开发中...')
}

// 组件挂载时获取作业数据
onMounted(() => {
  fetchAssignments()
  
  // 确保DOM元素存在后再访问
  if (searchInputGroup.value) {
    // 安全访问DOM元素
    console.log('搜索输入组已加载')
  }
})
  
  // 根据API状态获取显示状态
const getAssignmentStatus = (apiStatus?: string): string => {
  const statusMap: Record<string, string> = {
    'notSubmitted_未提交': '未开始',
    'submitted_已提交': '进行中',
    'graded_已批改': '已完成'
  }
  return statusMap[apiStatus || ''] || '未开始'
}

// 获取状态对应的标签类型
const getStatusType = (status: string) => {
  const statusMap: Record<string, string> = {
    '已完成': 'success',
    '待提交': 'warning',
    '未开始': 'default',
    '已截止': 'error'
  }
  return statusMap[status] || 'default'
}

// 格式化日期为XXXX年XX月XX日
const formatDate = (dateString: string): string => {
  if (!dateString || dateString === '未设置') return '未设置'
  
  try {
    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    
    return `${year}年${month.toString().padStart(2, '0')}月${day.toString().padStart(2, '0')}日`
  } catch (error) {
    console.error('日期格式化错误:', error)
    return dateString
  }
}
  </script>
  
  <style scoped>
  .courses-page {
    padding: 24px;
  }
  
  .header-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
    margin-bottom: 24px;
  }
  
  .title-section {
    h2 {
      margin: 0;
      font-size: 20px;
      color: #1a1a1a;
      font-weight: 500;
    }
  
    .subtitle {
      margin: 8px 0 0;
      color: #666;
      font-size: 14px;
    }
  }
  
  .action-buttons {
    display: flex;
    gap: 12px;
  
    .action-btn {
      display: flex;
      align-items: center;
      gap: 4px;
      color: #1890ff;
      border-color: #1890ff;
    }
  }
  
  .search-filter-section {
    margin: 24px 0;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .filters {
    display: flex;
    gap: 12px;
  }
  
  .assignments-grid {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-top: 24px;
  }
  
  .assignment-card {
    margin-bottom: 8px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 12px;
      border-bottom: 1px solid #f0f0f0;
  
      h3 {
        margin: 0;
        font-size: 18px;
        font-weight: 500;
        color: #1a1a1a;
      }
    }
  
    .card-content {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      padding: 16px 0;
      
      .requirements-row {
        grid-column: 1 / -1;
        margin-bottom: 8px;
        
        p {
          flex: 1;
        }
      }
    }
  
    .info-row {
      display: flex;
      gap: 8px;
      align-items: flex-start;
  
      &.time-info {
        display: flex;
        justify-content: space-between;
  
        > div.time-item {
          display: flex;
          gap: 8px;
          width: 45%; /* 确保每个时间项占据固定宽度 */
        }
      }
  
      .label {
        color: #666;
        white-space: nowrap;
        font-weight: 500;
      }
  
      p {
        margin: 0;
        line-height: 1.6;
      }
    }
  
    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid #f0f0f0;
  
      .action-buttons {
        display: flex;
        gap: 12px;
      }
    }
  }
  </style>