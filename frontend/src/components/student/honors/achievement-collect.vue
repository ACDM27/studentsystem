<template>
  <div class="collect_page">
    <!-- 页面标题区域 -->
    <header class="header">
      <div class="header_top">
        <n-button 
          text 
          size="large" 
          @click="go_back"
          class="back_btn"
        >
          <template #icon>
            <ArrowLeft :size="20" />
          </template>
          返回成果展示
        </n-button>
      </div>
      <h1>成果收集</h1>
      <p>填写您的成果信息，记录成长足迹</p>
    </header>

    <!-- 表单区域 -->
    <n-card class="form_card">
      <n-form 
        ref="form_ref" 
        :model="form_data" 
        :rules="form_rules" 
        label-placement="top"
        require-mark-placement="right-hanging"
        size="medium"
      >
        <!-- 基本信息区域 -->
        <div class="form_section">
          <h3 class="section_title">
            <FileText :size="20" />
            基本信息
          </h3>
          
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="学号" path="student_id">
                <n-input 
                  v-model:value="form_data.student_id" 
                  placeholder="请输入学号"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <n-form-item label="姓名" path="name">
                <n-input 
                  v-model:value="form_data.name" 
                  placeholder="请输入姓名"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="成果标题" path="title">
                <n-input 
                  v-model:value="form_data.title" 
                  placeholder="请输入成果标题"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <n-form-item label="成果类别" path="category">
                <n-select 
                  v-model:value="form_data.category" 
                  :options="category_opts" 
                  placeholder="请选择成果类别"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 详细信息区域 -->
        <div class="form_section">
          <h3 class="section_title">
            <Award :size="20" />
            详细信息
          </h3>
          
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="奖项" path="award">
                <n-select 
                  v-model:value="form_data.award" 
                  :options="award_opts" 
                  placeholder="请选择奖项"
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <n-form-item label="等级" path="level">
                <n-select 
                  v-model:value="form_data.level" 
                  :options="level_opts" 
                  placeholder="请选择等级"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="获奖日期" path="date">
                <n-date-picker 
                  v-model:value="form_data.date" 
                  type="date" 
                  placeholder="选择获奖日期"
                  @update:value="handle_date_change"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <n-form-item label="导师所属学院" path="tutor_department">
                <n-select 
                  v-model:value="form_data.tutor_department" 
                  :options="department_opts" 
                  placeholder="请选择所属学院"
                  @update:value="handle_department_change"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="导师姓名" path="tutor_name">
                <n-select 
                  v-model:value="form_data.tutor_name" 
                  :options="filtered_teacher_opts" 
                  placeholder="请先选择学院，再选择导师"
                  :disabled="!form_data.tutor_department"
                  clearable
                  filterable
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <!-- 预留空位，保持布局平衡 -->
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 附件上传区域 -->
        <div class="form_section">
          <h3 class="section_title">
            <Upload :size="20" />
            附件上传
          </h3>
          
          <n-form-item label="相关文件" path="attachments">
            <n-upload
              v-model:file-list="form_data.attachments"
              multiple
              directory-dnd
              :max="5"
              list-type="text"
              @before-upload="before_upload"
              @remove="handle_file_remove"
            >
              <n-upload-dragger>
                <div style="margin-bottom: 12px">
                  <n-icon size="48" :depth="3">
                    <Upload />
                  </n-icon>
                </div>
                <n-text style="font-size: 16px">
                  点击或者拖动文件到该区域来上传
                </n-text>
                <n-p depth="3" style="margin: 8px 0 0 0">
                  支持上传证书、获奖证明、论文等相关文件，最多5个文件
                </n-p>
              </n-upload-dragger>
            </n-upload>
          </n-form-item>
        </div>

        <!-- 操作按钮 -->
        <div class="form_actions">
          <n-space justify="center" size="large">
            <n-button size="large" @click="reset_form">
              <template #icon>
                <Refresh :size="20" />
              </template>
              重置表单
            </n-button>
            <n-button size="large" @click="save_draft">
              <template #icon>
                <Save :size="20" />
              </template>
              保存草稿
            </n-button>
            <n-button type="primary" size="large" @click="submitAchievementForm" :loading="submitting">
              <template #icon>
                <Send :size="20" />
              </template>
              提交成果
            </n-button>
          </n-space>
        </div>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import type { FormInst, UploadFileInfo } from 'naive-ui'
import {
  IconFileText as FileText,
  IconAward as Award,
  IconUpload as Upload,
  IconRefresh as Refresh,
  IconDeviceFloppy as Save,
  IconSend as Send,
  IconArrowLeft as ArrowLeft
} from '@tabler/icons-vue'
import {
  submitAchievement,
  getTeachers
} from '@/api'

// === API 适配器 ===

// 1. 创建成果适配器
const createAchievement = async (payload: any): Promise<any> => {
  const d = payload.data
  // 转换数据格式
  return submitAchievement({
      teacher_id: 1, // 默认 ID，因为旧表单未提供 ID
      title: d.title,
      type: d.category || 'competition',
      content_json: { ...d },
      evidence_url: ''
  })
}

// 2. 教师列表适配器 (包装为兼容 Strapi 的 { data: [] } 格式)
const fetchTeachers = async (): Promise<any> => {
  const list = await getTeachers()
  return { data: Array.isArray(list) ? list : [] }
}

// 3. 按学院获取教师 (前端过滤)
const fetchTeachersByDept = async (deptName: string): Promise<any> => {
  const list = await getTeachers() as any[]
  const filtered = list.filter(t => 
    (t.college && t.college.includes(deptName)) || 
    (t.department && t.department.includes(deptName))
  )
  return { data: filtered }
}

// 4. 按学院ID获取教师 (回退到获取所有，由前端逻辑进一步处理)
const fetchTeachersByDepartmentId = async (id: string): Promise<any> => {
  return fetchTeachers() 
}

// 5. 获取学院列表 (Mock，直接返回空，触发组件内的 Fallback 数据)
const fetchTeacherDepartments = async (): Promise<any> => {
  return { data: [] }
}
const router = useRouter()
const message = useMessage()

// 表单引用
const form_ref = ref<FormInst | null>(null)

// 提交状态
const submitting = ref(false)

// 表单数据
const form_data = ref({
  student_id: '',
  name: '',
  category: '1', // 成果类别，对应后端category字段，默认为竞赛类
  award: '', // 奖项，对应后端award字段
  date: null as number | null, // 获奖日期，对应后端date字段
  level: '',
  title: '',
  tutor_department: '', // 导师所属学院
  tutor_name: '', // 导师姓名
  attachments: [] as UploadFileInfo[]
})

// 表单验证规则
const form_rules = {
  student_id: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { 
      pattern: /^[0-9]+$/, 
      message: '学号只能包含数字', 
      trigger: 'blur' 
    }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 50, message: '姓名长度应在2-50字符之间', trigger: 'blur' }
  ],
  title: [
    { required: true, message: '请输入成果标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度应在2-100字符之间', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择成果类别', trigger: 'change' }
  ],
  award: [
    { required: true, message: '请选择奖项', trigger: 'change' }
  ],
  level: [
    { required: true, message: '请选择等级', trigger: 'change' }
  ],
  date: [
    { 
      required: true, 
      message: '请选择获奖日期', 
      trigger: 'change',
      validator: (rule: any, value: number | null) => {
        if (!value) {
          return new Error('请选择获奖日期')
        }
        const selected_date = new Date(value)
        const today = new Date()
        if (selected_date > today) {
          return new Error('获奖日期不能晚于今天')
        }
        return true
      }
    }
  ],
  tutor_department: [
    { required: true, message: '请选择导师所属学院', trigger: 'change' }
  ],
  tutor_name: [
    { required: true, message: '请选择导师姓名', trigger: 'change' }
  ]
}

// 选项配置 - 保留数字值，映射为后端字段值
const category_opts = [
  { label: '竞赛类', value: '1', backendValue: 'competition' },
  { label: '科研类', value: '2', backendValue: 'research' },
  { label: '项目类', value: '3', backendValue: 'project' },
  { label: '论文类', value: '4', backendValue: 'paper' },
  { label: '专利类', value: '5', backendValue: 'patent' },
  { label: '证书类', value: '6', backendValue: 'certification' }
]

// 修正奖项配置，确保标签与值匹配
const award_opts = [
  { label: '特等奖', value: 'grandprize' },
  { label: '一等奖', value: 'firstprize' },
  { label: '二等奖', value: 'secondprize' },
  { label: '三等奖', value: 'thirdprize' },
  { label: '优秀奖', value: 'honorablemention' },
]

const level_opts = [
  { label: '国家级', value: 'international' },
  { label: '省部级', value: 'provincial' },
  { label: '校级', value: 'university' },
  { label: '院级', value: 'college' }
]

// 学院选项配置 - 改为响应式，支持从后端动态获取
const department_opts = ref([
  { label: '计算机学院', value: '计算机学院' },
  { label: '软件学院', value: '软件学院' },
  { label: '人工智能学院', value: '人工智能学院' }
])

// 教师数据管理
const teachers_data = ref<any[]>([])
const current_department_teachers = ref<any[]>([])
const loading_teachers = ref(false)

// 根据当前学院的教师数据生成选项
const filtered_teacher_opts = computed(() => {
  if (!form_data.value.tutor_department) {
    return []
  }
  
  return current_department_teachers.value.map(teacher => ({
    label: teacher.name || '未知教师',
    value: teacher.name || '',
    teacher_id: teacher.id
  }))
})

// 允许的文件类型配置
const allowed_file_types = {
  'application/pdf': 'PDF文件',
  'image/jpeg': 'JPEG图片',
  'image/jpg': 'JPG图片',
  'image/png': 'PNG图片',
  'application/msword': 'Word文档',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Word文档',
  'application/vnd.ms-excel': 'Excel文档',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Excel文档'
}

// 最大文件大小（10MB）
const MAX_FILE_SIZE = 10 * 1024 * 1024

// 方法
const go_back = () => {
  router.push('/student/achievement')
}

const handle_date_change = (value: number | null) => {
  // 日期变化时无需额外处理，直接使用 date
  console.log('日期已更新:', value ? new Date(value).toLocaleDateString() : '未选择')
}

// 处理学院变化
const handle_department_change = async (value: string) => {
  // 清空导师选择
  form_data.value.tutor_name = ''
  console.log('学院已更新:', value)
  
  // 根据选择的学院获取对应的教师信息
  if (value) {
    await fetch_teachers_by_department(value)
  }
}

// 获取所有教师数据（初始化时使用）
const fetch_teachers_data = async () => {
  if (loading_teachers.value) return
  
  try {
    loading_teachers.value = true
    console.log('开始获取教师数据...')
    
    const response = await fetchTeachers()
    console.log('教师API响应:', response)
    
    if (response && response.data) {
      let teacherData: any[] = []
      
      // 处理不同的响应格式
      if (Array.isArray(response.data)) {
        teacherData = response.data
      } else if (response.data.data && Array.isArray(response.data.data)) {
        teacherData = response.data.data
      } else if (response.data.data && typeof response.data.data === 'object') {
        // 处理Strapi格式
        const strapiData = response.data.data
        if (Array.isArray(strapiData)) {
          teacherData = strapiData.map((item: any) => ({
            id: item.id,
            ...item.attributes
          }))
        }
      }
      
      // 标准化教师数据
      teachers_data.value = teacherData.map((item: any) => ({
        id: item.id?.toString() || '',
        name: item.name || '',
        title: item.title || '',
        department: item.department || item.college || '',
        research_direction: item.research_direction || item.researchContent || '',
        email: item.email || '',
        phone: item.phone || ''
      }))
      
      console.log('处理后的教师数据:', teachers_data.value)
      message.success(`成功加载 ${teachers_data.value.length} 位教师信息`)
    } else {
      console.warn('教师API返回数据格式异常')
      message.warning('教师数据加载异常，请稍后重试')
    }
  } catch (error: any) {
    console.error('获取教师数据失败:', error)
    message.error('获取教师信息失败，请检查网络连接')
  } finally {
    loading_teachers.value = false
  }
}

// 根据学院获取教师数据
const fetch_teachers_by_department = async (department: string) => {
  try {
    loading_teachers.value = true
    console.log(`开始获取${department}学院教师数据...`)
    
    // 首先尝试获取所有学院信息，然后匹配
    console.log('尝试获取所有学院信息...')
    let allDepartmentsResponse
    try {
      allDepartmentsResponse = await fetchTeacherDepartments()
      console.log('所有学院信息API响应:', allDepartmentsResponse)
    } catch (error) {
      console.warn('无法从后端获取学院信息，使用备用数据:', error)
      // 如果后端没有学院数据，使用前端定义的学院映射
      allDepartmentsResponse = {
        data: [
          { id: '1', code: 'computer', name: '计算机学院', attributes: { code: 'computer', name: '计算机学院' } },
          { id: '2', code: 'math', name: '数学学院', attributes: { code: 'math', name: '数学学院' } },
          { id: '3', code: 'physics', name: '物理学院', attributes: { code: 'physics', name: '物理学院' } },
          { id: '4', code: 'chemistry', name: '化学学院', attributes: { code: 'chemistry', name: '化学学院' } },
          { id: '5', code: 'biology', name: '生物学院', attributes: { code: 'biology', name: '生物学院' } },
          { id: '6', code: 'economics', name: '经济学院', attributes: { code: 'economics', name: '经济学院' } },
          { id: '7', code: 'management', name: '管理学院', attributes: { code: 'management', name: '管理学院' } },
          { id: '8', code: 'foreign', name: '外语学院', attributes: { code: 'foreign', name: '外语学院' } }
        ]
      }
    }
    
    let departmentId: string | null = null
    
    // 处理所有学院信息响应
    if (allDepartmentsResponse) {
      console.log('原始学院API响应:', allDepartmentsResponse)
      let allDepartmentData: any[] = []
      
      // 处理Strapi v5的响应格式
      if (allDepartmentsResponse.data) {
        if (Array.isArray(allDepartmentsResponse.data)) {
          allDepartmentData = allDepartmentsResponse.data
        } else if (allDepartmentsResponse.data.data && Array.isArray(allDepartmentsResponse.data.data)) {
          allDepartmentData = allDepartmentsResponse.data.data
        } else if (typeof allDepartmentsResponse.data === 'object' && allDepartmentsResponse.data.id) {
          // 单个对象的情况
          allDepartmentData = [allDepartmentsResponse.data]
        }
      } else if (Array.isArray(allDepartmentsResponse)) {
        allDepartmentData = allDepartmentsResponse
      }
      
      console.log('解析后的学院数据:', allDepartmentData)
      console.log('当前查找的学院代码:', department)
      
      // 查找匹配的学院（通过code字段或name字段）
      const matchedDepartment = allDepartmentData.find((dept: any) => {
        const deptData = dept.attributes || dept
        const code = deptData.code || deptData.Code
        const name = deptData.name || deptData.Name
        
        console.log(`检查学院: ID=${dept.id}, code=${code}, name=${name}`)
        
        return code === department || 
               name === department ||
               code === department.toLowerCase() ||
               name?.toLowerCase().includes(department.toLowerCase()) ||
               department.toLowerCase().includes(name?.toLowerCase())
      })
      
      if (matchedDepartment) {
        departmentId = matchedDepartment.id?.toString()
        console.log(`找到匹配的学院:`, matchedDepartment, `ID: ${departmentId}`)
      } else {
        console.log(`未找到匹配的学院，可用学院:`, allDepartmentData.map(d => ({
          id: d.id,
          code: d.attributes?.code || d.code || d.attributes?.Code || d.Code,
          name: d.attributes?.name || d.name || d.attributes?.Name || d.Name
        })))
        console.log(`查找条件: ${department}`)
      }
    } else {
      console.error('学院API响应为空或无效')
    }
    
    // 如果找到学院ID，则根据学院ID获取教师信息
    if (departmentId) {
      console.log(`使用学院ID ${departmentId} 获取教师信息...`)
      let response
      try {
        response = await fetchTeachersByDepartmentId(departmentId)
        console.log(`${department}学院教师API响应:`, response)
      } catch (error) {
        console.warn(`通过学院ID获取教师失败，尝试备用方法:`, error)
        // 如果通过学院ID获取失败，回退到原方法
        response = await fetchTeachersByDept(department)
        console.log(`${department}学院教师API响应(备用方法):`, response)
      }
      
      if (response && response.data) {
        let teacherData: any[] = []
        
        // 处理不同的响应格式
        if (Array.isArray(response.data)) {
          teacherData = response.data
        } else if (response.data.data && Array.isArray(response.data.data)) {
          teacherData = response.data.data
        } else if (response.data.data && typeof response.data.data === 'object') {
          // 处理Strapi格式
          const strapiData = response.data.data
          if (Array.isArray(strapiData)) {
            teacherData = strapiData.map((item: any) => ({
              id: item.id,
              ...item.attributes
            }))
          }
        }
        
        // 标准化教师数据并存储到当前学院教师数据中
        current_department_teachers.value = teacherData.map((item: any) => ({
          id: item.id?.toString() || '',
          name: item.name || '',
          title: item.title || '',
          department: item.department || item.college || department,
          research_direction: item.research_direction || item.researchContent || '',
          email: item.email || '',
          phone: item.phone || ''
        }))
        
        console.log(`${department}学院教师数据加载成功:`, current_department_teachers.value)
        message.success(`成功加载 ${current_department_teachers.value.length} 位${department}学院教师信息`)
      } else {
        console.warn(`${department}学院教师API返回数据格式异常`)
        message.warning(`${department}学院教师数据加载异常，请稍后重试`)
        current_department_teachers.value = []
      }
    } else {
      // 如果没有找到学院ID，回退到原来的方法
      console.log(`未找到${department}学院信息，使用备用方法获取教师数据`)
      const response = await fetchTeachersByDept(department)
      console.log(`${department}学院教师API响应(备用方法):`, response)
      
      if (response && response.data) {
        let teacherData: any[] = []
        
        // 处理不同的响应格式
        if (Array.isArray(response.data)) {
          teacherData = response.data
        } else if (response.data.data && Array.isArray(response.data.data)) {
          teacherData = response.data.data
        } else if (response.data.data && typeof response.data.data === 'object') {
          // 处理Strapi格式
          const strapiData = response.data.data
          if (Array.isArray(strapiData)) {
            teacherData = strapiData.map((item: any) => ({
              id: item.id,
              ...item.attributes
            }))
          }
        }
        
        // 标准化教师数据并存储到当前学院教师数据中
        current_department_teachers.value = teacherData.map((item: any) => ({
          id: item.id?.toString() || '',
          name: item.name || '',
          title: item.title || '',
          department: item.department || item.college || department,
          research_direction: item.research_direction || item.researchContent || '',
          email: item.email || '',
          phone: item.phone || ''
        }))
        
        console.log(`${department}学院教师数据加载成功(备用方法):`, current_department_teachers.value)
        message.success(`成功加载 ${current_department_teachers.value.length} 位${department}学院教师信息`)
      } else {
        console.warn(`${department}学院教师API返回数据格式异常`)
        message.warning(`${department}学院教师数据加载异常，请稍后重试`)
        current_department_teachers.value = []
      }
    }
  } catch (error: any) {
    console.error(`获取${department}学院教师数据失败:`, error)
    message.error(`获取${department}学院教师信息失败，请检查网络连接`)
    current_department_teachers.value = []
  } finally {
    loading_teachers.value = false
  }
}

const before_upload = (data: { file: UploadFileInfo }) => {
  const file = data.file
  
  // 检查文件类型
  if (!file.type || !allowed_file_types[file.type as keyof typeof allowed_file_types]) {
    const allowed_types = Object.values(allowed_file_types).join('、')
    message.error(`只支持以下文件类型：${allowed_types}`)
    return false
  }
  
  // 检查文件大小
  if ((file.file?.size || 0) > MAX_FILE_SIZE) {
    message.error('文件大小不能超过10MB')
    return false
  }
  
  // 检查文件名长度
  if (file.name && file.name.length > 100) {
    message.error('文件名长度不能超过100个字符')
    return false
  }
  
  // 检查是否有重复文件
  const existing_files = form_data.value.attachments
  const is_duplicate = existing_files.some(existing_file => 
    existing_file.name === file.name && existing_file.file?.size === file.file?.size
  )
  
  if (is_duplicate) {
    message.warning('该文件已存在，请勿重复上传')
    return false
  }
  
  return true
}

const handle_file_remove = (data: { file: UploadFileInfo }) => {
  message.info('文件已移除')
}

const reset_form = () => {
  form_ref.value?.restoreValidation()
  Object.assign(form_data.value, {
    student_id: '',
    name: '',
    category: '1', // 默认为竞赛类
    award: '',
    date: null,
    level: '',
    title: '',
    tutor_department: '',
    tutor_name: '',
    attachments: []
  })
  message.success('表单已重置')
}

const save_draft = () => {
  try {
    const draft_data = { ...form_data.value }
    // 不保存文件对象，只保存文件信息
    draft_data.attachments = draft_data.attachments.map(file => ({
      ...file,
      file: null // 清除文件对象，避免序列化问题
    }))
    
    localStorage.setItem('achievement_draft', JSON.stringify(draft_data))
    message.success('草稿已保存')
  } catch (error) {
    console.error('保存草稿失败:', error)
    message.error('保存草稿失败，请重试')
  }
}

// 主要提交函数
const submitAchievementForm = async () => {
  try {
    // 表单验证
    await form_ref.value?.validate()
    submitting.value = true
    
    // 获取当前选择的 category 数字值
    const selectedCategory = form_data.value.category;
    
    // 找到对应的后端字段值
    const selectedCategoryOption = category_opts.find(option => option.value === selectedCategory);
    const categoryBackendValue = selectedCategoryOption ? selectedCategoryOption.backendValue : '';

    // 构建符合后端API要求的提交数据格式
    const submit_data = {
      data: {
        student_id: form_data.value.student_id.trim(),
        name: form_data.value.name.trim(),
        category: categoryBackendValue,  // 使用映射后的值
        award: form_data.value.award,
        level: form_data.value.level,
        date: form_data.value.date ? new Date(form_data.value.date).toISOString() : new Date().toISOString(),
        title: form_data.value.title.trim(),
        tutor_department: form_data.value.tutor_department,
        tutor_name: form_data.value.tutor_name,
      }
    }
    
    console.log('提交数据:', submit_data)
    
    // 调用API提交到 /api/achievements
    const response = await createAchievement(submit_data)
    
    // 注意：响应拦截器已经返回了 response.data，所以这里的 response 就是数据本身
    // 只要没抛出异常就是成功
    console.log('提交成功，响应数据:', response)
    message.success('成果提交成功！')
    // 清除草稿
    localStorage.removeItem('achievement_draft')
    // 返回成果展示页面
    router.push('/student/achievement')
    
  } catch (error: any) {
    console.error('提交失败:', error)
    
    // 详细的错误处理
    if (error.name === 'ValidationError') {
      message.error('请完善必填信息后再提交')
    } else if (error.response?.status === 400) {
      message.error('数据格式有误，请检查后重试')
    } else if (error.response?.status === 401) {
      message.error('身份验证失败，请重新登录')
    } else if (error.response?.status === 403) {
      message.error('权限不足，无法提交成果')
    } else if (error.response?.status === 500) {
      message.error('服务器错误，请稍后重试')
    } else if (error.message?.includes('网络')) {
      message.error('网络连接异常，请检查网络后重试')
    } else {
      message.error('提交失败，请重试或联系管理员')
    }
  } finally {
    submitting.value = false
  }
}


// 动态获取学院列表
const init_departments = async () => {
  try {
    console.log('正在从后端同步学院列表...')
    const response = await fetchTeachers()
    if (response && response.data && Array.isArray(response.data)) {
      const teachers = response.data
      const depts = new Set<string>()
      
      teachers.forEach((t: any) => {
        // 优先使用 department 字段，兼容 college 字段
        const dept = t.department || t.college
        if (dept) {
          depts.add(dept)
        }
      })
      
      if (depts.size > 0) {
        department_opts.value = Array.from(depts).map(d => ({
          label: d,
          value: d
        }))
        console.log('学院列表已同步:', department_opts.value)
      }
    }
  } catch (error) {
    console.error('同步学院列表失败，使用默认值:', error)
  }
}

// 页面初始化
onMounted(() => {
  // 1. 同步学院数据
  init_departments()

  // 页面初始化，不再预加载所有教师数据
  // 教师数据将在用户选择学院时按需加载
  
  // 尝试恢复草稿
  try {
    const draft = localStorage.getItem('achievement_draft')
    if (draft) {
      const draft_data = JSON.parse(draft)
      // 恢复基本数据，但不恢复文件列表（文件对象无法序列化）
      Object.assign(form_data.value, {
        ...draft_data,
        attachments: [] // 重置文件列表
      })
      message.info('已恢复上次保存的草稿（不包含文件）')
    }
  } catch (error) {
    console.error('恢复草稿失败:', error)
    localStorage.removeItem('achievement_draft') // 清除损坏的草稿
  }
})
</script>

<style scoped>
.collect_page {
  padding: 16px;
  font-family: "Microsoft YaHei", sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 24px;
  padding: 20px 0;
}

.header_top {
  margin-bottom: 16px;
}

.back_btn {
  color: #409eff;
  font-size: 14px;
  padding: 8px 12px;
  transition: all 0.3s ease;
}

.back_btn:hover {
  background-color: #f0f8ff;
  color: #337ecc;
}

.header h1 {
  font-weight: 700;
  font-size: 28px;
  margin: 0;
  color: #333;
}

.header p {
  color: #666;
  font-size: 16px;
  margin: 8px 0 0 0;
}

.form_card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form_section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.form_section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section_title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.form_actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .collect_page {
    padding: 12px;
  }
  
  .form_section {
    margin-bottom: 24px;
  }
  
  .section_title {
    font-size: 14px;
  }
  
  /* 移动端表单布局调整 */
  :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
}

/* 文件上传样式优化 */
:deep(.n-upload-dragger) {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

:deep(.n-upload-dragger:hover) {
  border-color: #409eff;
  background-color: #f0f8ff;
}

/* 表单项间距优化 */
:deep(.n-form-item) {
  margin-bottom: 0;
}

/* 按钮样式优化 */
:deep(.n-button) {
  border-radius: 6px;
}

/* 输入框样式优化 */
:deep(.n-input) {
  border-radius: 6px;
}

:deep(.n-select) {
  border-radius: 6px;
}

:deep(.n-date-picker) {
  width: 100%;
}
</style>