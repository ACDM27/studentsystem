<template>
  <div class="dashboard-container">
    <!-- 顶部信息区域 -->
    <div class="dashboard-header">
      <div class="user-info-section">
        <div class="user-avatar">
          <n-avatar size="large" round>
            <n-icon size="30">
              <User />
            </n-icon>
          </n-avatar>
        </div>
        <div class="user-details">
          <div class="user-name-id">
            <h2>
              <span v-if="userLoading" class="loading-text">{{ userInfo.name }}</span>
              <span v-else>{{ userInfo.name }}</span>
            </h2>
            <n-tag v-if="userInfo.student_id" size="small" type="info">{{ userInfo.student_id }}</n-tag>
          </div>
          <div class="user-academic-info">
            <span v-if="userInfo.college">{{ userInfo.college }}</span>
            <span v-if="userInfo.major">{{ userInfo.major }}</span>
            <span v-if="userInfo.grade">{{ userInfo.grade }}级</span>
          </div>
        </div>
        <div class="semester-info">
          <n-tag type="primary" size="large">{{ currentSemester }}</n-tag>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="dashboard-content">
      <div class="content-left">
        <!-- 最新公告 -->
        <n-card title="最新公告" class="announcement-card">
          <template #header-extra>
            <n-button v-if="announcements.length > defaultAnnouncementCount" 
                     text 
                     @click="toggleAnnouncementDisplay">
              {{ showAllAnnouncements ? '收起' : '显示更多' }}
            </n-button>
          </template>
          <n-list>
            <n-list-item v-for="notice in displayedAnnouncements" :key="notice.id">
              <n-thing :title="notice.title">
                <template #description>
                  <div class="notice-meta">
                    <n-tag size="small" :type="notice.type">{{ notice.category }}</n-tag>
                    <span class="notice-date">{{ notice.date }}</span>
                  </div>
                </template>
              </n-thing>
            </n-list-item>
          </n-list>
        </n-card>

        <!-- 最近任务 -->
        <n-card title="最近任务" class="tasks-card">
          <template #header-extra>
            <n-button text @click="navigateToHomework">查看完整任务</n-button>
          </template>
          <n-tabs type="line" animated>
            <n-tab-pane name="homework" tab="待提交作业">
              <n-list>
                <n-list-item v-for="task in homeworkTasks" :key="task.id">
                  <n-thing :title="task.title">
                    <template #description>
                      <div class="task-meta">
                        <div class="task-info">
                          <span class="teacher">指导老师: {{ task.teacher }}</span>
                          <span class="credit">学分: {{ task.credit }}</span>
                          <n-tag :type="get_status_type(task.status)">{{ task.status }}</n-tag>
                        </div>
                        <span class="due-date">截止日期: {{ task.deadline }}</span>
                      </div>
                    </template>
                  </n-thing>
                </n-list-item>
              </n-list>
            </n-tab-pane>
            <n-tab-pane name="project" tab="课程进度">
              <n-list>
                <n-list-item v-for="project in projectTasks" :key="project.id">
                  <n-thing :title="project.title">
                    <template #description>
                      <div class="project-meta">
                        <n-progress type="line" :percentage="project.progress" />
                        <span class="milestone">{{ project.milestone }}</span>
                      </div>
                    </template>
                  </n-thing>
                </n-list-item>
              </n-list>
            </n-tab-pane>
          </n-tabs>
        </n-card>
      </div>

      <div class="content-right">
        <!-- 快速操作 -->
        <n-card title="快速操作" class="quick-actions-card">
          <div class="quick-actions-grid">
            <div v-for="action in quickActions" :key="action.id" class="quick-action-item" @click="handleQuickAction(action.id)">
              <n-icon size="24" :component="action.icon" />
              <span>{{ action.name }}</span>
            </div>
          </div>
        </n-card>

        <!-- 本周日历 -->
        <n-card title="本周日历" class="calendar-card">
          <template #header-extra>
            <n-button text @click="navigateToSchedule">查看完整日历</n-button>
          </template>
          <div class="week-calendar">
            <div v-for="day in weekSchedule" :key="day.date" class="calendar-day" :class="{ 'has-class': day.hasClass }">
              <div class="day-header">
                <span class="day-name">{{ day.name }}</span>
                <span class="day-date">{{ day.date }}</span>
              </div>
              <div class="day-content" v-if="day.hasClass">
                <n-tag size="small" type="success">{{ day.className }}</n-tag>
                <span class="class-time">{{ day.classTime }}</span>
              </div>
            </div>
          </div>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User, 
  Book, 
  FileText, 
  ChartBar, 
  CreditCard, 
  ClipboardCheck
} from '@vicons/tabler'
import { getStudentMe, getStudentProfile } from '@/api'
// import type { IGetAssignmentsResp, IGetNewsResp, IGetStudentsMeResp, IGetStudentsProfileResp } from '@/types/api'
import { useCourseService } from '@/services/courseService'

const router = useRouter()

// 使用课程服务
const { weekSchedule, loadCourses } = useCourseService()

// 用户信息
const userInfo = ref({
  name: '加载中...',
  student_id: '',
  college: '',
  major: '',
  grade: '',
  email: '',
  username: ''
})
const userLoading = ref(false)

// 当前学期
const currentSemester = ref('2023-2024学年第二学期')

// 公告数据
interface Announcement {
  id: number
  title: string
  category: string
  type: string
  date: string
}

const announcements = ref<Announcement[]>([])
// 控制是否展开显示全部公告
const showAllAnnouncements = ref(false)
// 默认显示的公告数量
const defaultAnnouncementCount = 3

// 切换展开/收起公告列表
const toggleAnnouncementDisplay = () => {
  showAllAnnouncements.value = !showAllAnnouncements.value
}

// 计算当前应该显示的公告列表
const displayedAnnouncements = computed(() => {
  if (showAllAnnouncements.value || announcements.value.length <= defaultAnnouncementCount) {
    return announcements.value
  } else {
    return announcements.value.slice(0, defaultAnnouncementCount)
  }
})

// 从API获取新闻数据
const fetchNews = async () => {
  try {
    // TODO: 后端 getNews API 暂未实现，使用默认数据
    announcements.value = [
      { id: 1, title: '关于2024年春季学期期末考试安排的通知', category: '考试通知', type: 'warning', date: '2024-01-10' },
      { id: 2, title: '寒假实习岗位信息发布', category: '就业通知', type: 'info', date: '2024-01-08' },
      { id: 3, title: '计算机学院创新创业大赛启动', category: '竞赛通知', type: 'success', date: '2024-01-05' }
    ]
  } catch (error) {
    console.error('获取新闻数据失败:', error)
    announcements.value = [
      { id: 1, title: '关于2024年春季学期期末考试安排的通知', category: '考试通知', type: 'warning', date: '2024-01-10' }
    ]
  }
}

// 设置默认公告数据的辅助函数
const setDefaultAnnouncements = () => {
  announcements.value = [
    { id: 1, title: '关于2024年春季学期期末考试安排的通知', category: '考试通知', type: 'warning', date: '2024-01-10' },
    { id: 2, title: '寒假实习岗位信息发布', category: '就业通知', type: 'info', date: '2024-01-08' },
    { id: 3, title: '计算机学院创新创业大赛启动', category: '竞赛通知', type: 'success', date: '2024-01-05' }
  ]
}

// 作业任务
interface HomeworkTask {
  id: number
  title: string
  teacher: string
  credit: number
  status: string
  deadline: string
  publish_date: string
}

const homeworkTasks = ref<HomeworkTask[]>([])

// 根据时间判断作业状态
const calc_assign_status = (publish_date: string, deadline: string): string => {
  const now = new Date()
  const publish = new Date(publish_date)
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

// 从API获取作业任务数据
const fetchAssignments = async () => {
  try {
    // TODO: 后端 getAssignments API 暂未实现，使用默认数据
    homeworkTasks.value = [
      {
        id: 1,
        title: '数据结构课程作业',
        teacher: '张教授',
        credit: 2,
        status: '待提交',
        deadline: '2024-01-20',
        publish_date: '2024-01-01'
      }
    ]
  } catch (error) {
    console.error('获取作业任务失败:', error)
    homeworkTasks.value = []
  }
}

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    userLoading.value = true
    console.log('Dashboard: 开始获取用户信息...')
    
    // 检查是否有token
    const token = localStorage.getItem('token')
    console.log('Dashboard: 当前token:', token ? '存在' : '不存在')
    
    // 获取基本用户信息
    console.log('Dashboard: 调用getStudentMe API...')
    const userResponse = await getStudentMe()
    console.log('Dashboard: getStudentMe响应:', userResponse)
    
    if (userResponse) {
      userInfo.value.username = userResponse.username || ''
      userInfo.value.email = userResponse.email || ''
      // 优先使用后端返回的 name 字段（档案姓名）
      userInfo.value.name = userResponse.name || userResponse.username || '用户'
      
      console.log('Dashboard: 设置基本用户信息:', {
        username: userInfo.value.username,
        email: userInfo.value.email,
        name: userInfo.value.name
      })
    } else {
      console.warn('Dashboard: getStudentMe返回空响应')
    }
    
    // 尝试获取详细档案信息
    try {
      console.log('Dashboard: 调用getStudentProfile API...')
      const profileResponse = await getStudentProfile()
      console.log('Dashboard: getStudentProfile响应:', profileResponse)
      
      // 修正：后端返回的是 basic_info 字段
      if (profileResponse && profileResponse.basic_info) {
        // 如果档案中有姓名，优先使用档案中的姓名
        if (profileResponse.basic_info.name) {
          userInfo.value.name = profileResponse.basic_info.name
          console.log('Dashboard: 使用档案姓名:', userInfo.value.name)
        }
        if (profileResponse.basic_info.student_id) {
          userInfo.value.student_id = profileResponse.basic_info.student_id
          console.log('Dashboard: 设置学号:', userInfo.value.student_id)
        }
        if (profileResponse.basic_info.college) {
          userInfo.value.college = profileResponse.basic_info.college
          console.log('Dashboard: 设置学院:', userInfo.value.college)
        }
        if (profileResponse.basic_info.major) {
          userInfo.value.major = profileResponse.basic_info.major
          console.log('Dashboard: 设置专业:', userInfo.value.major)
        }
        if (profileResponse.basic_info.grade) {
          userInfo.value.grade = profileResponse.basic_info.grade
          console.log('Dashboard: 设置年级:', userInfo.value.grade)
        }
      } else {
        console.warn('Dashboard: getStudentsProfile返回空档案信息')
      }
    } catch (profileError) {
      console.warn('Dashboard: 获取用户档案信息失败:', profileError)
    }
    
    console.log('Dashboard: 用户信息获取完成，最终用户信息:', userInfo.value)
    
  } catch (error: any) {
    console.error('Dashboard: 获取用户信息失败:', error)
    console.error('Dashboard: 错误详情:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data
    })
    
    // 如果是401错误，说明需要登录
    if (error.response?.status === 401) {
      console.warn('Dashboard: 用户未登录，显示默认信息')
      userInfo.value.name = '未登录用户'
    } else {
      userInfo.value.name = '用户'
    }
  } finally {
    userLoading.value = false
  }
}

// 在组件挂载时获取作业任务数据和新闻数据
onMounted(() => {
  fetchUserInfo()
  fetchAssignments()
  fetchNews()
  loadCourses() // 加载课程数据
})

// 项目任务
const projectTasks = ref([
  { id: 1, title: '毕业设计项目', progress: 45, milestone: '需求分析阶段' },
  { id: 2, title: '创新创业项目', progress: 80, milestone: '开发测试阶段' }
])

// 快速操作
const quickActions = ref([
  { id: 'homework', name: '作业提交', icon: ClipboardCheck },
  { id: 'schedule', name: '课表查询', icon: Book },
  { id: 'exam', name: '考试安排', icon: FileText },
  { id: 'grade', name: '成绩查询', icon: ChartBar },
  { id: 'library', name: '图书借阅', icon: Book },
  { id: 'card', name: '一卡通', icon: CreditCard }
])

// 处理快速操作点击
const handleQuickAction = (actionId: string) => {
  switch (actionId) {
    case 'homework':
      router.push('/student/homework')
      break
    case 'schedule':
      router.push('/student/course-schedule')
      break
    // ... 其他操作处理
  }
}

// 跳转到课程安排页面
const navigateToSchedule = () => {
  router.push('/student/course-schedule')
}

// 跳转到作业管理页面
const navigateToHomework = () => {
  router.push('/student/homework')
}

// 获取状态对应的标签类型
const get_status_type = (status: string) => {
  const statusMap: Record<string, string> = {
    '已完成': 'success',
    '待提交': 'warning',
    '未开始': 'default',
    '已截止': 'error'
  }
  return statusMap[status] || 'default'
}
</script>

<style scoped>
.dashboard-container {
  padding: 0;
  height: 100%;
  width: 100%;
  overflow-y: auto;
  box-sizing: border-box;
}

.dashboard-header {
  margin-bottom: 16px;
  padding: 16px;
}

.user-info-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.user-details {
  flex-grow: 1;
  margin-left: 20px;
}

.user-name-id {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.user-name-id h2 {
  margin: 0;
  font-size: 20px;
  color: #1a1a1a;
}

.user-academic-info {
  display: flex;
  gap: 16px;
  color: #666;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
  height: calc(100vh - 120px);
  padding: 0 16px;
}

.content-left,
.content-right {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.content-left {
  overflow-y: auto;
}

.content-right {
  overflow-y: auto;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.quick-action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quick-action-item:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
}

.week-calendar {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  padding: 6px 4px;
  border-radius: 4px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  min-height: 60px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.calendar-day.has-class {
  background: #e8f4fd;
  border-color: #91d5ff;
}

.day-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 4px;
}

.day-name {
  font-weight: 500;
  color: #333;
  font-size: 11px;
}

.day-date {
  font-size: 10px;
  color: #666;
  margin-top: 2px;
}

.day-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.day-content .n-tag {
  font-size: 10px;
  padding: 1px 4px;
  line-height: 1.2;
}

.class-time {
  font-size: 9px;
  color: #666;
  text-align: center;
}

.notice-meta,
.project-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
}

.task-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}

.task-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.teacher, .credit {
  color: #666;
  font-size: 14px;
}

.due-date {
  color: #1890ff;
  font-size: 14px;
  font-weight: 500;
}

.task-meta :deep(.n-progress),
.project-meta :deep(.n-progress) {
  width: 60%;
}

.due-date,
.milestone {
  flex-shrink: 0;
  white-space: nowrap;
  color: #666;
  font-size: 13px;
}

/* 卡片样式优化 */
.announcement-card,
.tasks-card,
.quick-actions-card,
.calendar-card {
  height: fit-content;
}

.tasks-card {
  flex: 1;
}

.calendar-card {
  margin-top: 16px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .dashboard-content {
    grid-template-columns: 1fr;
    height: auto;
  }

  .content-left,
  .content-right {
    height: auto;
    overflow-y: visible;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .user-info-section {
    flex-direction: column;
    text-align: center;
  }

  .user-details {
    margin: 16px 0;
  }

  .user-academic-info {
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(1, 1fr);
  }

  .week-calendar {
    grid-template-columns: repeat(4, 1fr);
  }

  .calendar-day {
    min-height: 50px;
  }
}

.loading-text {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
</style>