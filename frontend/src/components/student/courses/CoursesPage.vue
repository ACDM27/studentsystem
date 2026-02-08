<template>
  <div class="courses_page">
    <!-- 页面顶部说明区域 -->
    <n-card class="header_card">
      <div class="header_area">
        <div class="title_info">
          <div class="title_row">
            <Book :size="24" />
            <h2>课程管理</h2>
          </div>
          <p class="desc_text">查看您的学习进度以及课程安排</p>
        </div>
        <div class="action_btns">
          <n-button type="primary" class="assistant_btn">
            <template #icon>
              <HelpCircle :size="24" />
            </template>
            智能助手
          </n-button>
          <n-button 
            quaternary 
            class="refresh_btn" 
            @click="loadCoursesData"
            :loading="loading"
          >
            <template #icon>
              <Refresh :size="24" />
            </template>
            刷新数据
          </n-button>
        </div>
      </div>
    </n-card>

    <!-- 视图切换 -->
    <div class="view-tabs">
      <n-tabs type="line" v-model:value="activeView" animated>
        <n-tab-pane name="list" tab="课程安排">
          <!-- 本周课程统计（淡蓝色容器） -->
          <div class="weekly_stats">
            <div class="stats_header">
              <div class="calendar_info">
                <Calendar :size="24" />
                <span>本周学习安排</span>
              </div>
              <div class="date_info">
                {{ currentDate }} · {{ currentWeekday }}
              </div>
            </div>
            
            <div class="stats_content">
              <div class="stat_item">
                <div class="stat_number">{{ stats.totalCourses }}</div>
                <div class="stat_label">本周课程</div>
              </div>
              <div class="stat_item">
                <div class="stat_number">{{ stats.majorCourses }}</div>
                <div class="stat_label">专业课程</div>
              </div>
              <div class="stat_item">
                <div class="stat_number">{{ stats.requiredCourses }}</div>
                <div class="stat_label">必修课程</div>
              </div>
              <div class="stat_item">
                <div class="stat_number">{{ stats.electiveCourses }}</div>
                <div class="stat_label">选修课程</div>
              </div>
            </div>
          </div>

          <!-- 课程搜索栏 -->
          <div class="search_bar">
            <n-input 
              v-model:value="searchQuery" 
              placeholder="搜索课程名称、代号或教师" 
              class="search_input"
            >
              <template #prefix>
                <Search :size="24" />
              </template>
            </n-input>
            <n-select 
              v-model:value="categoryFilter" 
              :options="categoryOptions" 
              placeholder="全部类别" 
              class="filter_select" 
            />
            <n-button quaternary class="filter_btn">
              <template #icon>
                <Filter :size="24" />
              </template>
              筛选条件
            </n-button>
          </div>

          <!-- 课程列表 -->
          <div class="course_list" v-if="!loading">
            <n-grid :cols="3" :x-gap="16" :y-gap="16">
              <n-grid-item v-for="course in filteredCourses" :key="course.id">
                <n-card class="course_card" hoverable>
                  <div class="course_header">
                    <div class="course_tag" :class="getCourseTypeClass(course.type)">
                      {{ course.typeText }}
                    </div>
                    <div class="course_name">{{ course.name }}</div>
                    <div class="course_code">{{ course.code }}</div>
                  </div>
                  
                  <div class="course_content">
                    <div class="course_info">
                      <div class="info_item">
                        <User :size="24" />
                        <span>授课教师：{{ course.teacher }}</span>
                      </div>
                      <div class="info_item">
                        <Clock :size="24" />
                        <span>上课时间：{{ course.time }}</span>
                      </div>
                      <div class="info_item">
                        <MapPin :size="24" />
                        <span>上课地点：{{ course.location }}</span>
                      </div>
                      <div class="info_item">
                        <Users :size="24" />
                        <span>选课人数：{{ course.studentsCount }}</span>
                      </div>
                    </div>
                    
                    <div class="course_desc">
                      <p>{{ course.description }}</p>
                    </div>
                  </div>
                </n-card>
              </n-grid-item>
            </n-grid>
          </div>
        </n-tab-pane>
        
        <n-tab-pane name="schedule" tab="课程表">
          <!-- 课程表视图 -->
          <div class="schedule_view">
            <div class="schedule_header">
              <div class="calendar_info">
                <Calendar :size="24" />
                <span>{{ currentDate }} · {{ currentWeekday }}</span>
              </div>
            </div>
            
            <div class="timetable">
              <div class="time-column">
                <div class="time-header">时间</div>
                <div class="time-slot" v-for="slot in timeSlots" :key="slot.id">
                  {{ slot.time }}
                </div>
              </div>
              
              <div class="day-column" v-for="day in weekdays" :key="day.id">
                <div class="day-header">{{ day.name }}</div>
                <div class="course-slots">
                  <div 
                    v-for="slot in timeSlots" 
                    :key="`${day.id}-${slot.id}`" 
                    class="course-slot"
                  >
                    <div 
                      v-if="getCourseAtSlot(day.id, slot.id)" 
                      class="course-block"
                      :class="[
                        getCourseAtSlot(day.id, slot.id)?.type ? getCourseTypeClass(getCourseAtSlot(day.id, slot.id)!.type) : '',
                        getSlotSpanClass(day.id, slot.id)
                      ]"
                      :style="getSlotStyle(day.id, slot.id)"
                    >
                      <div class="course-block-name">
                        {{ getCourseAtSlot(day.id, slot.id)?.name }}
                      </div>
                      <div class="course-block-location">
                        {{ getCourseAtSlot(day.id, slot.id)?.location }}
                      </div>
                      <div class="course-block-time" v-if="getCourseAtSlot(day.id, slot.id)?.time">
                        {{ getCourseAtSlot(day.id, slot.id)?.time }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </n-tab-pane>
      </n-tabs>
    </div>
    
    <!-- 加载状态 -->
    <div class="loading_state" v-if="loading">
      <n-spin size="large" />
      <p>数据获取中...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
// 临时 Mock 测试函数
const testCoursesAPI = async () => { console.warn('testCoursesAPI skipped') }
const testCourseAPIConnection = async () => { console.warn('testCourseAPIConnection skipped') }

// 修复导入
import { useCourseService } from '../../../services/courseService'
import { 
  IconBook as Book, 
  IconCalendar as Calendar, 
  IconSearch as Search, 
  IconFilter as Filter, 
  IconUser as User, 
  IconClock as Clock, 
  IconMapPin as MapPin, 
  IconUsers as Users,
  IconHelp as HelpCircle,
  IconRefresh as Refresh
} from '@tabler/icons-vue'

// 类型定义
interface CourseStats {
  totalCourses: number
  majorCourses: number
  requiredCourses: number
  electiveCourses: number
}

interface CourseItem {
  id: string | number
  name: string
  code: string
  type: 'major' | 'required' | 'elective'
  typeText: string
  teacher: string
  time: string
  location: string
  studentsCount: number
  description: string
  day?: number
  slot?: number
  // 后端 API 字段映射
  credit?: number
  teacherName?: string
  teacherId?: number
  semester?: 'Spring' | 'Summer' | 'Fall' | 'Winter'
  classTime?: string
  classroom?: string
  students?: number
  class_week?: string
  coursecontent?: string
}

interface SelectOption {
  label: string
  value: string | null
}

interface WeekDay {
  id: number
  name: string
}

interface TimeSlot {
  id: number
  time: string
}

// 格式化日期: 2023年7月20日
const formatDate = (date: Date): string => {
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`
}

// 获取星期几
const getWeekday = (date: Date): string => {
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  return weekdays[date.getDay()]
}

// 视图切换
const activeView = ref<'list' | 'schedule'>('list')

// 日期和星期
const currentDate = ref<string>(formatDate(new Date()))
const currentWeekday = ref<string>(getWeekday(new Date()))

// 搜索和筛选
const searchQuery = ref<string>('')
const categoryFilter = ref<string | null>(null)
const categoryOptions: SelectOption[] = [
  { label: '全部类别', value: null },
  { label: '专业课', value: 'major' },
  { label: '必修课', value: 'required' },
  { label: '选修课', value: 'elective' }
]

// 消息提示
const message = useMessage()

// 使用课程服务
const { courses, loading, courseStats, loadCourses: loadCoursesFromService } = useCourseService()

// 课程统计数据（使用服务提供的数据）
const stats = courseStats

// 过滤后的课程
const filteredCourses = computed<CourseItem[]>(() => {
  let result = courses.value
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(course => 
      course.name.toLowerCase().includes(query) ||
      course.code.toLowerCase().includes(query) ||
      course.teacher.toLowerCase().includes(query)
    )
  }
  
  // 类别过滤
  if (categoryFilter.value) {
    result = result.filter(course => course.type === categoryFilter.value)
  }
  
  return result
})

// 课程表相关数据 - 增加周六周日
const weekdays: WeekDay[] = [
  { id: 1, name: '周一' },
  { id: 2, name: '周二' },
  { id: 3, name: '周三' },
  { id: 4, name: '周四' },
  { id: 5, name: '周五' },
  { id: 6, name: '周六' },
  { id: 7, name: '周日' }
]

// 更新时间段为11个时间段
const timeSlots: TimeSlot[] = [
  { id: 1, time: '08:30-09:10' },
  { id: 2, time: '09:20-10:00' },
  { id: 3, time: '10:10-10:50' },
  { id: 4, time: '11:00-11:40' },
  { id: 5, time: '11:40-12:20' },
  { id: 6, time: '15:00-15:40' },
  { id: 7, time: '15:50-16:30' },
  { id: 8, time: '16:40-17:20' },
  { id: 9, time: '19:30-20:10' },
  { id: 10, time: '20:10-20:50' },
  { id: 11, time: '20:50-21:30' }
]

// 获取课程类型对应的样式类
const getCourseTypeClass = (type: string): string => {
  const classMap: Record<string, string> = {
    'major': 'tag-major',
    'required': 'tag-required',
    'elective': 'tag-elective'
  }
  return classMap[type] || ''
}




// 解析后端时间字符串到课程表位置的映射函数 - 支持跨时间段
const parseTimeToSlot = (timeStr: string): { day: number; startSlot: number; endSlot: number; slots: number[] } | null => {
  if (!timeStr) return null
  
  // 星期映射
  const dayMap: Record<string, number> = {
    '周一': 1, '星期一': 1, 'Monday': 1, 'Mon': 1,
    '周二': 2, '星期二': 2, 'Tuesday': 2, 'Tue': 2,
    '周三': 3, '星期三': 3, 'Wednesday': 3, 'Wed': 3,
    '周四': 4, '星期四': 4, 'Thursday': 4, 'Thu': 4,
    '周五': 5, '星期五': 5, 'Friday': 5, 'Fri': 5,
    '周六': 6, '星期六': 6, 'Saturday': 6, 'Sat': 6,
    '周日': 7, '星期日': 7, 'Sunday': 7, 'Sun': 7
  }
  
  // 时间段映射 - 根据开始时间判断属于哪个时间段
  const timeSlotMap: Array<{ start: string; end: string; slot: number; startMinutes: number; endMinutes: number }> = [
    { start: '08:30', end: '09:10', slot: 1, startMinutes: 8 * 60 + 30, endMinutes: 9 * 60 + 10 },
    { start: '09:20', end: '10:00', slot: 2, startMinutes: 9 * 60 + 20, endMinutes: 10 * 60 + 0 },
    { start: '10:10', end: '10:50', slot: 3, startMinutes: 10 * 60 + 10, endMinutes: 10 * 60 + 50 },
    { start: '11:00', end: '11:40', slot: 4, startMinutes: 11 * 60 + 0, endMinutes: 11 * 60 + 40 },
    { start: '11:40', end: '12:20', slot: 5, startMinutes: 11 * 60 + 40, endMinutes: 12 * 60 + 20 },
    { start: '15:00', end: '15:40', slot: 6, startMinutes: 15 * 60 + 0, endMinutes: 15 * 60 + 40 },
    { start: '15:50', end: '16:30', slot: 7, startMinutes: 15 * 60 + 50, endMinutes: 16 * 60 + 30 },
    { start: '16:40', end: '17:20', slot: 8, startMinutes: 16 * 60 + 40, endMinutes: 17 * 60 + 20 },
    { start: '19:30', end: '20:10', slot: 9, startMinutes: 19 * 60 + 30, endMinutes: 20 * 60 + 10 },
    { start: '20:10', end: '20:50', slot: 10, startMinutes: 20 * 60 + 10, endMinutes: 20 * 60 + 50 },
    { start: '20:50', end: '21:30', slot: 11, startMinutes: 20 * 60 + 50, endMinutes: 21 * 60 + 30 }
  ]
  
  // 解析星期
  let day = 0
  for (const [dayStr, dayNum] of Object.entries(dayMap)) {
    if (timeStr.includes(dayStr)) {
      day = dayNum
      break
    }
  }
  
  // 解析时间段 - 支持时间范围
  const timeMatch = timeStr.match(/(\d{1,2}):(\d{2})/g)
  if (timeMatch && timeMatch.length >= 1 && day > 0) {
    const startTime = timeMatch[0]
    const endTime = timeMatch.length > 1 ? timeMatch[1] : startTime
    
    // 转换为分钟数
    const [startHour, startMin] = startTime.split(':').map(Number)
    const [endHour, endMin] = endTime.split(':').map(Number)
    const startMinutes = startHour * 60 + startMin
    const endMinutes = endHour * 60 + endMin
    
    console.log(`解析时间: ${timeStr}, 开始: ${startTime}(${startMinutes}分钟), 结束: ${endTime}(${endMinutes}分钟)`)
    
    // 查找跨越的时间段
    const occupiedSlots: number[] = []
    let startSlot = 0
    let endSlot = 0
    
    for (const timeSlotItem of timeSlotMap) {
      // 检查课程时间是否与该时间段有重叠
      const hasOverlap = !(endMinutes <= timeSlotItem.startMinutes || startMinutes >= timeSlotItem.endMinutes)
      
      if (hasOverlap) {
        occupiedSlots.push(timeSlotItem.slot)
        if (startSlot === 0) startSlot = timeSlotItem.slot
        endSlot = timeSlotItem.slot
      }
    }
    
    console.log(`占据的时间段: ${occupiedSlots.join(', ')}`)
    
    if (occupiedSlots.length > 0) {
      return {
        day,
        startSlot,
        endSlot,
        slots: occupiedSlots
      }
    }
  }
  
  return null
}

// 获取指定时间段和星期的课程 - 支持跨时间段课程
const getCourseAtSlot = (dayId: number, slotId: number): CourseItem | null => {
  // 遍历所有课程，查找占据该时间段的课程
  for (const course of courses.value) {
    // 检查课程是否有时间信息
    const timeInfo = course.classTime || course.time || course.class_week
    if (timeInfo) {
      const parsed = parseTimeToSlot(timeInfo)
      if (parsed && parsed.day === dayId && parsed.slots.includes(slotId)) {
        return course
      }
    }
    
    // 如果没有时间信息，使用默认分配逻辑
    if (course.day === dayId && course.slot === slotId) {
      return course
    }
  }
  
  return null
}

// 获取跨时间段课程的CSS类
const getSlotSpanClass = (day: number, slot: number): string => {
  const course = getCourseAtSlot(day, slot)
  if (!course) return ''
  
  const timeInfo = course.classTime || course.time || course.class_week
  if (timeInfo) {
    const parsed = parseTimeToSlot(timeInfo)
    if (parsed && parsed.slots.length > 1) {
      // 跨时间段课程统一使用基础样式，具体显示通过getSlotStyle控制
      return 'multi-slot-course'
    }
  }
  
  return 'single-slot-course'
}

// 获取跨时间段课程的样式
const getSlotStyle = (day: number, slot: number): Record<string, string | number> => {
  const course = getCourseAtSlot(day, slot)
  if (!course) return {}
  
  const timeInfo = course.classTime || course.time || course.class_week
  if (timeInfo) {
    const parsed = parseTimeToSlot(timeInfo)
    if (parsed && parsed.slots.length > 1) {
      const slotIndex = parsed.slots.indexOf(slot)
      
      if (slotIndex === 0) {
        // 第一个时间段：扩展高度覆盖所有相关时间段
        const totalSlots = parsed.slots.length
        const slotHeight = 80 // 每个时间段的高度
        const borderHeight = totalSlots - 1 // 边框高度
        const totalHeight = totalSlots * slotHeight + borderHeight
        
        return {
          height: `${totalHeight}px`,
          zIndex: '10',
          position: 'absolute',
          top: '4px',
          left: '4px',
          right: '4px',
          margin: '0'
        }
      } else {
        // 其他时间段：完全隐藏，让第一个时间段的课程块覆盖
        return {
          visibility: 'hidden'
        }
      }
    }
  }
  
  return {}
}

// 获取课程类型的显示文本
const getTypeText = (type: string): string => {
  const typeMap: Record<string, string> = {
    'major': '专业课',
    'required': '必修课',
    'elective': '选修课'
  }
  return typeMap[type] || '其他'
}

// 获取课程数据 - 使用课程服务
const loadCoursesData = async (): Promise<void> => {
  await loadCoursesFromService()
}

onMounted(() => {
  // 在开发环境下进行 API 连接测试
  if (typeof import.meta !== 'undefined' && import.meta.env && (import.meta.env.DEV || import.meta.env.MODE === 'development')) {
    console.log('🚀 开发模式：开始课程API连接测试...')
    
    // 使用新的API连接测试工具
    testCourseAPIConnection().then(result => {
      console.log('新版课程API连接测试结果:', result)
    })
    
    // 保留原有的测试工具
    testCoursesAPI().then(result => {
      console.log('原版课程API测试结果:', result)
    })
  }
  
  loadCoursesData()
})
</script>

<style scoped>
.courses_page {
  padding: 20px;
}

.header_card {
  margin-bottom: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.header_area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.title_info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.title_row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.title_info h2 {
  margin: 0 0 0 10px;
  font-size: 20px;
}

.desc_text {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.action_btns {
  display: flex;
  gap: 12px;
}

.assistant_btn {
  background-color: #2080f0;
}

.refresh_btn {
  margin-left: 8px;
  border: 1px solid #d9d9d9;
}

.refresh_btn:hover {
  border-color: #2080f0;
  color: #2080f0;
}

.view-tabs {
  margin-bottom: 20px;
}

.weekly_stats {
  background-color: #e6f7ff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.stats_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.calendar_info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
}

.date_info {
  color: #666;
}

.stats_content {
  display: flex;
  justify-content: space-around;
}

.stat_item {
  text-align: center;
}

.stat_number {
  font-size: 24px;
  font-weight: bold;
  color: #1890ff;
}

.stat_label {
  font-size: 14px;
  color: #666;
}

.search_bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  align-items: center;
}

.search_input {
  width: 300px;
}

.filter_select {
  width: 180px;
}

.course_list {
  margin-bottom: 24px;
}

.course_card {
  border-radius: 8px;
  transition: all 0.3s ease;
  height: 100%;
  border: 1px solid #f0f0f0;
}

.course_card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.course_header {
  margin-bottom: 16px;
}

.course_tag {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 8px;
}

.tag-major {
  background-color: #e6f7ff;
  color: #1890ff;
  border: 1px solid #91d5ff;
}

.tag-required {
  background-color: #fff1f0;
  color: #f5222d;
  border: 1px solid #ffa39e;
}

.tag-elective {
  background-color: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.course_name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
  color: #262626;
}

.course_code {
  font-size: 14px;
  color: #8c8c8c;
}

.course_content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.course_info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.info_item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #595959;
}

.course_desc {
  font-size: 14px;
  color: #8c8c8c;
  line-height: 1.6;
}

.loading_state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.loading_state p {
  margin-top: 16px;
  color: #8c8c8c;
}

/* 课程表视图样式 */
.schedule_view {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-top: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.schedule_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 16px;
}

.timetable {
  display: flex;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.time-column {
  width: 120px;
  flex-shrink: 0;
  border-right: 1px solid #f0f0f0;
}

.day-column {
  flex: 1;
  min-width: 140px;
  border-right: 1px solid #f0f0f0;
}

.day-column:last-child {
  border-right: none;
}

.time-header, .day-header {
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  background-color: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  color: #262626;
}

.time-slot {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #f0f0f0;
  font-size: 12px;
  color: #8c8c8c;
  background-color: #fafafa;
  box-sizing: border-box;
}

.time-slot:last-child {
  border-bottom: none;
}

.course-slots {
  display: flex;
  flex-direction: column;
}

.course-slot {
  height: 80px;
  border-bottom: 1px solid #f0f0f0;
  padding: 4px;
  position: relative;
  background-color: #fff;
  box-sizing: border-box;
}

.course-slot:last-child {
  border-bottom: none;
}

.course-block {
  background-color: #e6f7ff;
  border-radius: 4px;
  padding: 8px;
  height: calc(100% - 8px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 1px solid #91d5ff;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  margin: 4px;
  text-align: center;
  font-size: 11px;
  overflow: hidden;
}

.course-block:hover {
  background-color: #bae7ff;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 保留原有的类型样式作为备用，但默认使用淡蓝色 */
.course-block.tag-major {
  background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%);
  border: 1px solid #91d5ff;
  color: #0050b3;
}

.course-block.tag-required {
  background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%);
  border: 1px solid #91d5ff;
  color: #0050b3;
}

.course-block.tag-elective {
  background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%);
  border: 1px solid #91d5ff;
  color: #0050b3;
}

.course-block-name {
  font-weight: 600;
  margin-bottom: 4px;
  font-size: 13px;
}

.course-block-location {
  font-size: 11px;
  opacity: 0.8;
  margin-bottom: 2px;
}

.course-block-time {
  font-size: 9px;
  color: #999;
  font-style: italic;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .course-list :deep(.n-grid) {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 768px) {
  .courses-page {
    padding: 12px;
  }
  
  .header-area {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .search-bar {
    flex-direction: column;
    gap: 12px;
  }
  
  .search-input,
  .filter-select {
    width: 100%;
  }
  
  .course-list :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
  
  .stats-content {
    flex-direction: column;
    gap: 16px;
  }
  
  .timetable {
    overflow-x: auto;
  }
}
</style>