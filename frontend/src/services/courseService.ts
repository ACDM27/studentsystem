import { ref, computed } from 'vue'
import { getCourses, getCourseById } from '@/api'
import type { ICourseItem } from '../types/api.d.ts'

// 课程数据类型定义
export interface CourseItem {
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

// 本周日历数据类型
export interface WeekScheduleItem {
  name: string
  date: string
  hasClass: boolean
  className?: string
  classTime?: string
}

// 全局课程数据状态
const courses = ref<CourseItem[]>([])
const loading = ref<boolean>(false)
const lastFetchTime = ref<number>(0)

// 缓存时间（5分钟）
const CACHE_DURATION = 5 * 60 * 1000

// 解析课程类型
const parseCourseType = (type: string): { type: 'major' | 'required' | 'elective'; typeText: string } => {
  if (type.includes('必修') || type.includes('CompulsoryCourse')) {
    return { type: 'required', typeText: '必修课' }
  } else if (type.includes('选修') || type.includes('ElectiveCourse')) {
    return { type: 'elective', typeText: '选修课' }
  } else {
    return { type: 'major', typeText: '专业课' }
  }
}

// 解析时间字符串到星期几
const parseTimeToDay = (timeStr: string): number | undefined => {
  if (!timeStr) return undefined

  const dayMap: Record<string, number> = {
    '周一': 1, '星期一': 1, 'Monday': 1, 'Mon': 1,
    '周二': 2, '星期二': 2, 'Tuesday': 2, 'Tue': 2,
    '周三': 3, '星期三': 3, 'Wednesday': 3, 'Wed': 3,
    '周四': 4, '星期四': 4, 'Thursday': 4, 'Thu': 4,
    '周五': 5, '星期五': 5, 'Friday': 5, 'Fri': 5,
    '周六': 6, '星期六': 6, 'Saturday': 6, 'Sat': 6,
    '周日': 7, '星期日': 7, 'Sunday': 7, 'Sun': 7
  }

  for (const [key, value] of Object.entries(dayMap)) {
    if (timeStr.includes(key)) {
      return value
    }
  }

  return undefined
}

// 获取当前周的日期
const getCurrentWeekDates = (): string[] => {
  const today = new Date()
  const currentDay = today.getDay() // 0 = 周日, 1 = 周一, ...
  const monday = new Date(today)

  // 计算本周一的日期
  const diff = currentDay === 0 ? -6 : 1 - currentDay
  monday.setDate(today.getDate() + diff)

  const weekDates: string[] = []
  for (let i = 0; i < 7; i++) {
    const date = new Date(monday)
    date.setDate(monday.getDate() + i)
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    weekDates.push(`${month}-${day}`)
  }

  return weekDates
}

// 获取课程数据
export const useCourseService = () => {
  // 加载课程数据
  const loadCourses = async (forceRefresh = false) => {
    const now = Date.now()

    // 如果有缓存且未过期，直接返回
    if (!forceRefresh && courses.value.length > 0 && (now - lastFetchTime.value) < CACHE_DURATION) {
      return courses.value
    }

    loading.value = true

    try {
      const response = await getCourses()
      let courseData: any[] = []

      // FastAPI响应已由拦截器处理，直接是 {list, total} 格式
      if (response.list && Array.isArray(response.list)) {
        courseData = response.list
      } else if (Array.isArray(response)) {
        courseData = response
      } else {
        console.warn('未知的课程数据格式:', response)
        courseData = []
      }


      // 转换数据格式 - FastAPI后端字段映射
      courses.value = courseData.map((item: any) => {
        const { type, typeText } = parseCourseType(item.category || item.type || '')
        const day = parseTimeToDay(item.schedule || item.classTime || '')

        return {
          id: item.id,
          name: item.course_name || item.name || '未知课程',
          code: item.course_code || item.code || '',
          type,
          typeText,
          teacher: item.teacher_name || item.teacherName || '未知教师',
          time: item.schedule || item.classTime || '时间待定',
          location: item.location || item.classroom || '地点待定',
          studentsCount: item.enrolled_students || item.students || 0,
          description: item.description || item.coursecontent || '暂无课程描述',
          day,
          credit: item.credits || item.credit,
          teacherName: item.teacher_name || item.teacherName,
          teacherId: item.teacher_id || item.teacherId,
          semester: item.semester,
          classTime: item.schedule || item.classTime,
          classroom: item.location || item.classroom,
          students: item.enrolled_students || item.students,
          class_week: item.class_week,
          coursecontent: item.description || item.coursecontent
        }
      })

      lastFetchTime.value = now
      console.log('课程数据加载成功:', courses.value.length, '门课程')

    } catch (error) {
      console.error('加载课程数据失败:', error)
      // 如果API失败，使用默认数据
      courses.value = getDefaultCourses()
    } finally {
      loading.value = false
    }

    return courses.value
  }

  // 获取本周课程安排
  const getWeekSchedule = computed((): WeekScheduleItem[] => {
    const weekDates = getCurrentWeekDates()
    const weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

    return weekdays.map((dayName, index) => {
      const dayNumber = index + 1
      const date = weekDates[index]

      // 查找当天的课程
      const todayCourses = courses.value.filter(course => course.day === dayNumber)

      if (todayCourses.length > 0) {
        // 如果有多门课程，显示第一门
        const firstCourse = todayCourses[0]
        return {
          name: dayName,
          date,
          hasClass: true,
          className: firstCourse.name,
          classTime: firstCourse.time
        }
      } else {
        return {
          name: dayName,
          date,
          hasClass: false
        }
      }
    })
  })

  // 获取课程统计
  const getCourseStats = computed(() => {
    const totalCourses = courses.value.length
    const majorCourses = courses.value.filter(c => c.type === 'major').length
    const requiredCourses = courses.value.filter(c => c.type === 'required').length
    const electiveCourses = courses.value.filter(c => c.type === 'elective').length

    return {
      totalCourses,
      majorCourses,
      requiredCourses,
      electiveCourses
    }
  })

  return {
    courses: computed(() => courses.value),
    loading: computed(() => loading.value),
    weekSchedule: getWeekSchedule,
    courseStats: getCourseStats,
    loadCourses
  }
}

// 默认课程数据（用于API失败时的备用数据）
const getDefaultCourses = (): CourseItem[] => {
  return [
    {
      id: 1,
      name: '数据结构',
      code: 'CS101',
      type: 'required',
      typeText: '必修课',
      teacher: '张教授',
      time: '周一 8:00-9:40',
      location: '教学楼A101',
      studentsCount: 45,
      description: '数据结构与算法基础',
      day: 1
    },
    {
      id: 2,
      name: '软件工程',
      code: 'CS102',
      type: 'major',
      typeText: '专业课',
      teacher: '李教授',
      time: '周三 14:00-15:40',
      location: '教学楼B201',
      studentsCount: 38,
      description: '软件开发生命周期管理',
      day: 3
    },
    {
      id: 3,
      name: '计算机网络',
      code: 'CS103',
      type: 'required',
      typeText: '必修课',
      teacher: '王教授',
      time: '周四 10:00-11:40',
      location: '教学楼C301',
      studentsCount: 42,
      description: '计算机网络原理与协议',
      day: 4
    }
  ]
}