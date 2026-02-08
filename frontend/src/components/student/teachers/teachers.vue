<template>
  <div class="teachers_page">
    <!-- 页面顶部说明区域 -->
    <n-card class="header_card">
      <div class="header_area">
        <div class="title_info">
          <div class="title_row">
            <Users :size="24" />
            <h2>教师信息查询</h2>
          </div>
          <p class="desc_text">查找您需要的教师信息和联系信息</p>
        </div>
        <div class="action_btns">
          <n-button type="primary" @click="view_favorites" class="favorite_btn">
            <template #icon>
              <Star :size="24" />
            </template>
            我的收藏
          </n-button>
        </div>
      </div>
    </n-card>

    <!-- 搜索和筛选区域 -->
    <div class="filter_area">
      <n-input v-model:value="search_key" placeholder="搜索教师姓名/工号" class="search_input">
        <template #prefix>
          <Search :size="24" />
        </template>
      </n-input>
      <n-select v-model:value="college_filter" placeholder="按学院筛选" :options="college_options" class="filter_select" />
      <n-select v-model:value="title_filter" placeholder="按职称筛选" :options="title_options" class="filter_select" />
      <n-select v-model:value="direction_filter" placeholder="按研究方向筛选" :options="direction_options" class="filter_select" />
      <n-button quaternary @click="reset_filters" class="reset_btn">
        <template #icon>
          <Refresh :size="24" />
        </template>
        清除筛选
      </n-button>
    </div>

    <!-- 教师卡片展示区域 -->
    <div class="teacher_cards">
      <n-spin :show="loading">
        <n-empty v-if="filtered_teachers.length === 0" description="暂无教师数据" />
        <n-grid :cols="3" :x-gap="16" :y-gap="16" v-else>
          <n-grid-item v-for="teacher in filtered_teachers" :key="teacher.id">
            <n-card class="teacher_card" hoverable>
              <template #header>
                <div class="card_header">
                  <div class="teacher_avatar">
                    <n-avatar
                      round
                      :size="64"
                      :src="getAvatarUrl(teacher)"
                      fallback-src="/avatar.jpg"
                    />
                  </div>
                  <div class="teacher_basic_info">
                    <div class="teacher_name">{{ teacher.name }}</div>
                    <div class="teacher_title">{{ get_title_cn(teacher.title) }}</div>
                    <div class="teacher_college">{{ teacher.college }}</div>
                  </div>
                  <div class="favorite_icon">
                    <n-button text @click="toggle_favorite(teacher.id)">
                      <template #icon>
                        <component :is="is_favorite(teacher.id) ? StarFilled : Star" :size="24" />
                      </template>
                    </n-button>
                  </div>
                </div>
              </template>

              <div class="teacher_info">
                <div class="info_item">
                  <Compass :size="24" />
                  <span class="info_label">研究方向：</span>
                  <span>{{ teacher.research_direction || '暂无信息' }}</span>
                </div>
                <div class="info_item">
                  <Users :size="24" />
                  <span class="info_label">招收学生：</span>
                  <span>{{ teacher.student_type || '暂无信息' }}</span>
                </div>
                <div class="info_item">
                  <Star :size="24" />
                  <span class="info_label">教师评分：</span>
                  <n-rate readonly :value="teacher.rating || 0" :count="5" />
                  <span class="rating_value">{{ (teacher.rating || 0).toFixed(1) }}</span>
                </div>
                <div class="info_item">
                  <Book :size="24" />
                  <span class="info_label">当前授课：</span>
                  <span>{{ teacher.current_courses || '暂无信息' }}</span>
                </div>
                <div class="info_item">
                  <MapPin :size="24" />
                  <span class="info_label">办公地点：</span>
                  <span>{{ teacher.office_location || '暂无信息' }}</span>
                </div>
                <div class="info_item">
                  <Clock :size="24" />
                  <span class="info_label">办公时间：</span>
                  <span>{{ teacher.office_hours || '暂无信息' }}</span>
                </div>
              </div>

              <template #footer>
                <div class="card_footer">
                  <div class="footer_left">
                    <n-button text @click="view_teacher_detail(teacher.id)">
                      <template #icon>
                        <Eye :size="24" />
                      </template>
                      查看详情
                    </n-button>
                  </div>
                  <div class="footer_right">
                    <n-button text @click="contact_teacher(teacher.id)">
                      <template #icon>
                        <Mail :size="24" />
                      </template>
                      联系教师
                    </n-button>
                  </div>
                </div>
              </template>
            </n-card>
          </n-grid-item>
        </n-grid>
      </n-spin>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import type { Component } from 'vue'
import { 
  IconUsers as Users, 
  IconSearch as Search, 
  IconStar as Star,
  IconStarFilled as StarFilled,
  IconEye as Eye, 
  IconMail as Mail,
  IconRefresh as Refresh,
  IconCompass as Compass,
  IconBook as Book,
  IconMapPin as MapPin,
  IconClock as Clock
} from '@tabler/icons-vue'
import { getTeachers } from '@/api'
// TODO: teacher-api-test 工具函数暂未实现
// import { testTeacherAPI, checkAPIConfig } from '../../../utils/teacher-api-test'

// 定义教师数据类型
interface TeacherItem {
  id: string
  name: string
  title: string
  college: string
  research_direction: string
  student_type: string
  rating: number
  current_courses: string
  office_location: string
  office_hours: string
  avatar?: any
  [key: string]: any
}

// 定义API响应类型
interface ApiResponse {
  data: TeacherItem[]
  [key: string]: any
}

// 定义选择器选项类型
interface SelectOption {
  label: string
  value: string
}

const router = useRouter()
const message = useMessage()

// 职称映射表 - 将英文职称转换为中文
const title_map: Record<string, string> = {
  'Lecturer': '讲师',
  'Professor': '教授',
  'associate professor': '副教授',
  'assistant professor': '助理教授',
  'associate': '副教授',
  'assistant': '助教'
}

// 获取中文职称
const get_title_cn = (title: string): string => {
  if (!title) return '暂无职称'
  return title_map[title] || title
}

// 获取后端URL用于拼接头像路径
const backendUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const getAvatarUrl = (teacher: TeacherItem): string => {
  // 如果教师对象不存在或没有avatar属性，返回默认头像
  if (!teacher || !teacher.avatar) {
    return backendUrl + '/uploads/avatar_88e8d14b8c.jpg';
  }
  
  const avatarObj = teacher.avatar as any;

  // 处理字符串类型的头像URL
  if (typeof avatarObj === 'string') {
    // 如果是完整URL则直接返回，否则拼接后端URL
    return avatarObj.startsWith('http') ? avatarObj : backendUrl + avatarObj;
  }

  // 处理新的Strapi媒体对象格式
  if (avatarObj.id && avatarObj.hash) {
    // 直接使用hash作为文件名
    return `${backendUrl}/uploads/${avatarObj.hash}${avatarObj.ext}`;
  }
  
  // 处理标准Strapi媒体对象类型的头像
  const data = avatarObj?.data;
  if (data && data.attributes && data.attributes.url) {
    return backendUrl + data.attributes.url;
  }
  
  // 如果无法获取有效的头像URL，返回默认头像
  return backendUrl + '/uploads/avatar_88e8d14b8c.jpg';
}



// 加载状态
const loading = ref<boolean>(false)

// 教师数据
const teachers = ref<TeacherItem[]>([])

// 收藏的教师ID列表
const favorite_ids = ref<string[]>([])

// 筛选条件
const search_key = ref<string>('')
const college_filter = ref<string | null>(null)
const title_filter = ref<string | null>(null)
const direction_filter = ref<string | null>(null)

// 筛选选项
const college_options: SelectOption[] = [
  { label: '计算机学院', value: 'computer' },
  { label: '数学学院', value: 'math' },
  { label: '物理学院', value: 'physics' },
  { label: '化学学院', value: 'chemistry' },
  { label: '生物学院', value: 'biology' }
]

const title_options: SelectOption[] = [
  { label: '教授', value: 'professor' },
  { label: '副教授', value: 'associate' },
  { label: '讲师', value: 'lecturer' },
  { label: '助教', value: 'assistant' }
]

const direction_options: SelectOption[] = [
  { label: '人工智能', value: 'ai' },
  { label: '数据科学', value: 'data' },
  { label: '软件工程', value: 'software' },
  { label: '网络安全', value: 'security' },
  { label: '云计算', value: 'cloud' }
]

// 此处已删除重复的isDevelopment函数定义

// fallback教师数据（仅开发环境使用）
const fallbackTeachers: TeacherItem[] = [
  {
    id: '1',
    name: '李明',
    title: '教授',
    college: '计算机科学与技术学院',
    research_direction: '人工智能、机器学习',
    student_type: '本科生、研究生',
    rating: 4.5,
    current_courses: '人工智能导论、机器学习',
    office_location: '计算机楼A区501',
    office_hours: '周一、周三 14:00-16:00',
    avatar: '/teacher-avatars/teacher1.jpg'
  },
  {
    id: '2',
    name: '王雪琴',
    title: '副教授',
    college: '计算机学院',
    research_direction: '数据科学、云计算',
    student_type: '本科生、研究生',
    rating: 4.6,
    current_courses: '分布式系统、云计算技术',
    office_location: '计算机楼B205',
    office_hours: '周一、周三 10:00-12:00'
  },
  {
    id: '3',
    name: '张建国',
    title: '讲师',
    college: '计算机学院',
    research_direction: '软件工程、信息安全',
    student_type: '本科生',
    rating: 4.5,
    current_courses: '软件工程、密码学基础',
    office_location: '中教楼C102',
    office_hours: '周五 15:00-17:00'
  }
]

// 获取教师数据
const fetchTeacherData = async (): Promise<void> => {
  loading.value = true
  try {
    console.log('正在获取教师列表数据...')
    const response = await getTeachers()  // 修正：使用 getTeachers 而不是 fetchTeachers
    console.log('教师数据响应:', response)
    
    // 响应直接是数组类型 (TeachersResponse = Teacher[])
    let teacherData: any[] = []
    
    if (Array.isArray(response)) {
      teacherData = response
    } else if ((response as any).data) { // 兼容旧接口结构
      const startpiData = (response as any).data
      if (Array.isArray(startpiData)) {
        teacherData = startpiData
      } else if (startpiData.data && Array.isArray(startpiData.data)) {
        teacherData = startpiData.data
      }
    }

    if (teacherData.length > 0) {
      
      // 确保数据格式一致，正确映射后端字段
      teachers.value = teacherData.map((item: any) => {
        console.log('处理单个教师数据:', item)
        console.log('研究方向字段:', {
          research_direction: item.research_direction,
          researchcontent: item.researchcontent,
          researchContent: item.researchContent,
          research_directions: item.research_directions
        })
        console.log('当前授课字段:', {
          current_courses: item.current_courses,
          classname: item.classname,
          className: item.className
        })
        return {
          id: item.id?.toString() || '',
          name: item.name || '',
          title: item.title || '',
          college: item.department || item.college || '',
          research_direction: item.research_direction || item.researchcontent || item.researchContent || item.research_directions || '',
          student_type: item.studentCount ? item.studentCount.toString() : item.student_type || '',
          rating: Number(item.rating) || 0,
          current_courses: item.current_courses || item.classname || item.className || '',
          office_location: item.officeLocation || item.office_location || '',
          office_hours: item.officeHours || item.office_hours || '',
          avatar: item.attributes?.avatar || item.avatar || ''
        }
      })
      
      console.log('处理后的教师数据:', teachers.value)
      
      // 如果后端返回空数据且在开发环境，使用fallback数据
      if (teachers.value.length === 0 && isDevelopment()) {
        console.log('开发环境：后端无数据，使用fallback数据')
        teachers.value = fallbackTeachers
      }
    } else {
      console.warn('响应中没有找到有效的教师数据')
      // 仅在开发环境使用fallback数据
      if (isDevelopment()) {
        console.log('开发环境：API响应无效，使用fallback数据')
        teachers.value = fallbackTeachers
      } else {
        teachers.value = []
        message.warning('暂无教师数据')
      }
    }
  } catch (error) {
    console.error('获取教师数据失败:', error)
    
    // 仅在开发环境使用fallback数据
    if (isDevelopment()) {
      console.log('开发环境：API请求失败，使用fallback数据')
      teachers.value = fallbackTeachers
      message.warning('API请求失败，当前显示测试数据')
    } else {
      teachers.value = []
      message.error('获取教师数据失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

// 筛选后的教师列表
const filtered_teachers = computed((): TeacherItem[] => {
  return teachers.value.filter((teacher: TeacherItem) => {
    // 关键词筛选（姓名或工号）
    if (search_key.value && !teacher.name?.includes(search_key.value) && !teacher.id?.includes(search_key.value)) {
      return false
    }
    
    // 学院筛选
    if (college_filter.value) {
      const collegeMap: Record<string, string> = {
        'computer': '计算机学院',
        'math': '数学学院',
        'physics': '物理学院',
        'chemistry': '化学学院',
        'biology': '生物学院'
      }
      if (teacher.college !== collegeMap[college_filter.value]) {
        return false
      }
    }
    
    // 职称筛选
    if (title_filter.value) {
      const titleMap: Record<string, string> = {
        'professor': '教授',
        'associate': '副教授',
        'lecturer': '讲师',
        'assistant': '助教'
      }
      if (teacher.title !== titleMap[title_filter.value]) {
        return false
      }
    }
    
    // 研究方向筛选
    if (direction_filter.value) {
      const directionMap: Record<string, string> = {
        'ai': '人工智能',
        'data': '数据科学',
        'software': '软件工程',
        'security': '网络安全',
        'cloud': '云计算'
      }
      if (!teacher.research_direction?.includes(directionMap[direction_filter.value])) {
        return false
      }
    }
    
    return true
  })
})

// 重置筛选条件
const reset_filters = (): void => {
  search_key.value = ''
  college_filter.value = null
  title_filter.value = null
  direction_filter.value = null
  message.success('已重置所有筛选条件')
}

// 查看教师详情
const view_teacher_detail = (id: string): void => {
  console.log('点击查看教师详情，教师ID:', id)
  console.log('教师ID类型:', typeof id)
  
  // 验证ID是否有效
  if (!id || id === '' || id === 'undefined' || id === 'null') {
    console.error('教师ID无效:', id)
    message.error('教师ID无效，无法查看详情')
    return
  }
  
  // 确保ID是字符串格式
  const teacherId = String(id).trim()
  console.log('处理后的教师ID:', teacherId)
  
  // 跳转到教师详情页
  const detailPath = `/student/teacher-detail/${teacherId}`
  console.log('跳转路径:', detailPath)
  
  router.push(detailPath)
}

// 联系教师
const contact_teacher = (id: string): void => {
  message.info('联系功能即将上线，敬请期待')
}

// 查看收藏的教师
const view_favorites = (): void => {
  router.push('/student/teacher-favorites')
}

// 切换收藏状态
const toggle_favorite = (id: string): void => {
  const index = favorite_ids.value.indexOf(id)
  if (index === -1) {
    // 添加收藏
    favorite_ids.value.push(id)
    message.success('已添加到收藏')
  } else {
    // 取消收藏
    favorite_ids.value.splice(index, 1)
    message.success('已取消收藏')
  }
  
  // 保存到本地存储
  localStorage.setItem('favorite_teachers', JSON.stringify(favorite_ids.value))
}

// 检查是否已收藏
const is_favorite = (id: string): boolean => {
  return favorite_ids.value.includes(id)
}

// 安全检查开发环境
const isDevelopment = (): boolean => {
  try {
    if (typeof import.meta !== 'undefined' && import.meta.env) {
      return import.meta.env.DEV === true || import.meta.env.NODE_ENV === 'development'
    }
    return false
  } catch (error) {
    console.warn('无法检查开发环境:', error)
    return false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  // 在开发环境下进行API配置检查
  if (isDevelopment()) {
    console.log('=== 开发环境：进行API配置检查 ===')
    // checkAPIConfig()  // TODO: 暂时注释，工具函数未实现
  }
  
  // 从本地存储加载收藏列表
  const saved_favorites = localStorage.getItem('favorite_teachers')
  if (saved_favorites) {
    try {
      favorite_ids.value = JSON.parse(saved_favorites)
    } catch (e) {
      console.error('解析收藏数据失败:', e)
      favorite_ids.value = []
    }
  }
  
  // 获取教师数据
  fetchTeacherData()
  
  // 在开发环境下测试API
  if (isDevelopment()) {
    setTimeout(() => {
      console.log('=== 开发环境：测试教师API ===')
      // testTeacherAPI()  // TODO: 暂时注释，工具函数未实现
    }, 2000) // 延迟2秒执行，确保教师数据已加载
  }
})
</script>

<style scoped>
.teachers_page {
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

.favorite_btn {
  background-color: #2080f0;
}

.filter_area {
  display: flex;
  margin-bottom: 24px;
  align-items: center;
}

.search_input {
  width: 250px;
  margin-right: 16px;
}

.filter_select {
  width: 180px;
  margin-right: 16px;
}

.reset_btn {
  color: #2080f0;
}

.teacher_cards {
  margin-bottom: 24px;
}

.teacher_card {
  height: 100%;
}

.card_header {
  display: flex;
  align-items: center;
  padding: 16px 0;
}

.teacher_avatar {
  margin-right: 16px;
}

.teacher_basic_info {
  flex: 1;
}

.teacher_name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 4px;
}

.teacher_title {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.teacher_college {
  font-size: 14px;
  color: #666;
}

.favorite_icon {
  color: #f0a020;
}

.teacher_info {
  margin-bottom: 16px;
}

.info_item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: #333;
  font-size: 14px;
}

.info_item svg {
  margin-right: 8px;
  color: #2080f0;
}

.info_label {
  font-weight: bold;
  margin-right: 4px;
  width: 80px;
}

.rating_value {
  margin-left: 8px;
  color: #f0a020;
  font-weight: bold;
}

.card_footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>