import { ref, computed } from 'vue'
import { getActivities, getActivityById } from '@/api'
import type { IActivityItem, IGetActivityByIdParams, IPostActivityReq, IPutActivityReq, IDeleteActivityParams } from '../types/api.d.ts'

// 活动数据类型定义
export interface ActivityItem {
  id: string | number
  name: string
  reg_start: string
  reg_end: string
  max_part: number
  credits: number
  act_type: 'college' | 'campus' | 'assoc' | 'youth'
  act_status: 'ongoing' | 'completed' | 'not_started'
  type_text: string
  college?: string
  assoc?: string
  youth?: string
}

// 全局活动数据状态
const activities = ref<ActivityItem[]>([])
const loading = ref<boolean>(false)
const lastFetchTime = ref<number>(0)

// 缓存时间（5分钟）
const CACHE_DURATION = 5 * 60 * 1000

// 解析活动类型
const parseActivityType = (type: string): { type: 'college' | 'campus' | 'assoc' | 'youth'; typeText: string } => {
  if (type.includes('college')) {
    return { type: 'college', typeText: '学院活动' }
  } else if (type.includes('campus')) {
    return { type: 'campus', typeText: '校园活动' }
  } else if (type.includes('association')) {
    return { type: 'assoc', typeText: '社团活动' }
  } else {
    return { type: 'youth', typeText: '团委活动' }
  }
}

// 将API活动数据转换为前端活动数据格式
const convertToActivityItem = (item: IActivityItem): ActivityItem => {
  const { type, typeText } = parseActivityType(item.activity_type || '')

  return {
    id: item.id,
    name: item.name || '未知活动',
    reg_start: item.registration_start_time || '',
    reg_end: item.registration_end_time || '',
    max_part: item.max_participants || 0,
    credits: item.credits || 0,
    act_type: type,
    act_status: item.activitystatus || 'not_started',
    type_text: typeText,
    college: item.collegename,
    assoc: item.associationname,
    youth: item.youthLeaguename
  }
}

// 将前端活动数据格式转换为API活动数据
const convertToApiActivity = (item: ActivityItem): IPostActivityReq => {
  // 确定活动类型
  let activity_type: 'collegeActivities' | 'campusActivities' | 'associationActivities' | 'youthLeagueCommitteeActivities' = 'campusActivities'

  if (item.act_type === 'college') {
    activity_type = 'collegeActivities'
  } else if (item.act_type === 'assoc') {
    activity_type = 'associationActivities'
  } else if (item.act_type === 'youth') {
    activity_type = 'youthLeagueCommitteeActivities'
  }

  return {
    name: item.name,
    registration_start_time: item.reg_start,
    registration_end_time: item.reg_end,
    max_participants: item.max_part,
    credits: item.credits,
    activity_type,
    activitystatus: item.act_status,
    collegename: item.college,
    associationname: item.assoc,
    youthLeaguename: item.youth
  }
}

// 获取活动数据
export const useActivityService = () => {
  // 加载活动数据
  const loadActivities = async (forceRefresh = false) => {
    const now = Date.now()

    // 如果有缓存且未过期，直接返回
    if (!forceRefresh && activities.value.length > 0 && (now - lastFetchTime.value) < CACHE_DURATION) {
      return activities.value
    }

    loading.value = true

    try {
      const response = await getActivities()
      let activityData: any[] = []

      // FastAPI响应已由拦截器处理，直接是 {list, total} 格式
      if (response.list && Array.isArray(response.list)) {
        activityData = response.list
      } else if (Array.isArray(response)) {
        activityData = response
      } else {
        console.warn('未知的活动数据格式:', response)
        activityData = []
      }
      // 转换数据格式
      activities.value = activityData.map(convertToActivityItem)

      lastFetchTime.value = now
      console.log('活动数据加载成功:', activities.value.length, '个活动')

    } catch (error) {
      console.error('加载活动数据失败:', error)
      // 如果API失败，使用默认数据
      activities.value = getDefaultActivities()
    } finally {
      loading.value = false
    }

    return activities.value
  }

  // 获取单个活动详情
  const getActivity = async (id: string | number) => {
    try {
      const response = await getActivityById(Number(id))

      // FastAPI响应已由拦截器处理，直接是活动对象
      if (response) {
        return convertToActivityItem(response)
      }

      return null
    } catch (error) {
      console.error('获取活动详情失败:', error)
      return null
    }
  }

  // 创建新活动 - TODO: 后端未实现
  const createActivity = async (activityData: ActivityItem) => {
    console.warn('createActivity: 后端 API未实现')
    return null
    // try {
    //   const apiData = convertToApiActivity(activityData)
    //   const response = await postActivity(apiData)

    //   if (response.data) {
    //     // 刷新活动列表
    //     await loadActivities(true)
    //     return convertToActivityItem(response.data)
    //   }

    //   return null
    // } catch (error) {
    //   console.error('创建活动失败:', error)
    //   return null
    // }
  }

  // 更新活动 - TODO: 后端未实现
  const updateActivity = async (id: string | number, activityData: Partial<ActivityItem>) => {
    console.warn('updateActivity: 后端 API未实现')
    return null
    // try {
    //   // 构建更新数据
    //   const updateData: IPutActivityReq = {}

    //   if (activityData.name) updateData.name = activityData.name
    //   if (activityData.reg_start) updateData.registration_start_time = activityData.reg_start
    //   if (activityData.reg_end) updateData.registration_end_time = activityData.reg_end
    //   if (activityData.max_part !== undefined) updateData.max_participants = activityData.max_part
    //   if (activityData.credits !== undefined) updateData.credits = activityData.credits
    //   if (activityData.act_status) updateData.activitystatus = activityData.act_status
    //   if (activityData.college) updateData.collegename = activityData.college
    //   if (activityData.assoc) updateData.associationname = activityData.assoc
    //   if (activityData.youth) updateData.youthLeaguename = activityData.youth

    //   // 更新活动类型
    //   if (activityData.act_type) {
    //     if (activityData.act_type === 'college') {
    //       updateData.activity_type = 'collegeActivities'
    //     } else if (activityData.act_type === 'campus') {
    //       updateData.activity_type = 'campusActivities'
    //     } else if (activityData.act_type === 'assoc') {
    //       updateData.activity_type = 'associationActivities'
    //     } else if (activityData.act_type === 'youth') {
    //       updateData.activity_type = 'youthLeagueCommitteeActivities'
    //     }
    //   }

    //   const response = await putActivity(id, updateData)

    //   if (response.data) {
    //     // 刷新活动列表
    //     await loadActivities(true)
    //     return convertToActivityItem(response.data)
    //   }

    //   return null
    // } catch (error) {
    //   console.error('更新活动失败:', error)
    //   return null
    // }
  }

  // 删除活动 - TODO: 后端未实现
  const removeActivity = async (id: string | number) => {
    console.warn('removeActivity: 后端 API未实现')
    return false
    // try {
    //   const params: IDeleteActivityParams = { id }
    //   const response = await deleteActivity(params)

    //   if (response.data) {
    //     // 刷新活动列表
    //     await loadActivities(true)
    //     return true
    //   }

    //   return false
    // } catch (error) {
    //   console.error('删除活动失败:', error)
    //   return false
    // }
  }

  // 获取活动统计
  const getActivityStats = computed(() => {
    const totalActivities = activities.value.length
    const collegeActivities = activities.value.filter(a => a.act_type === 'college').length
    const campusActivities = activities.value.filter(a => a.act_type === 'campus').length
    const assocActivities = activities.value.filter(a => a.act_type === 'assoc').length
    const youthActivities = activities.value.filter(a => a.act_type === 'youth').length

    const ongoingActivities = activities.value.filter(a => a.act_status === 'ongoing').length
    const completedActivities = activities.value.filter(a => a.act_status === 'completed').length
    const notStartedActivities = activities.value.filter(a => a.act_status === 'not_started').length

    return {
      totalActivities,
      collegeActivities,
      campusActivities,
      assocActivities,
      youthActivities,
      ongoingActivities,
      completedActivities,
      notStartedActivities
    }
  })

  return {
    activities: computed(() => activities.value),
    loading: computed(() => loading.value),
    activityStats: getActivityStats,
    loadActivities,
    getActivity,
    createActivity,
    updateActivity,
    removeActivity
  }
}

// 默认活动数据（用于API失败时的备用数据）
const getDefaultActivities = (): ActivityItem[] => {
  return [
    {
      id: 1,
      name: '校园歌手大赛',
      reg_start: '2023-09-01',
      reg_end: '2023-09-15',
      max_part: 100,
      credits: 2,
      act_type: 'campus',
      act_status: 'ongoing',
      type_text: '校园活动'
    },
    {
      id: 2,
      name: '计算机学院学术讲座',
      reg_start: '2023-09-10',
      reg_end: '2023-09-20',
      max_part: 50,
      credits: 1,
      act_type: 'college',
      act_status: 'not_started',
      type_text: '学院活动',
      college: '计算机学院'
    },
    {
      id: 3,
      name: '摄影协会采风活动',
      reg_start: '2023-08-15',
      reg_end: '2023-08-30',
      max_part: 30,
      credits: 1.5,
      act_type: 'assoc',
      act_status: 'completed',
      type_text: '社团活动',
      assoc: '摄影协会'
    }
  ]
}