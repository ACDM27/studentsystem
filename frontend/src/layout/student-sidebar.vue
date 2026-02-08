<template>
  <div class="sidebar-container" :class="{ 'is-collapse': is_collapse }">
    <!-- 顶部标题区域 -->
    <div class="logo-container">
      <div class="logo-icon">
        <n-icon size="24" style="display: flex; align-items: center;">
          <IconSchool :size="24" />
        </n-icon>
      </div>
      <transition name="fade">
        <h1 class="logo-title" v-show="!is_collapse">学生综合信息服务平台</h1>
      </transition>
    </div>

    <!-- 中部菜单区域 -->
    <div class="menu-container">
      <n-scrollbar style="max-height: 100%;">
        <div class="menu-wrapper">
          <template v-for="group in menu_options" :key="group.key">
            <div class="menu-group" :class="{ 'is-collapsed': groupCollapsed[group.key] }">
              <!-- 分组标题 -->
              <div 
                class="menu-group-title" 
                :class="{ 'is-sidebar-collapsed': is_collapse }"
                @click="toggleGroup(group.key)"
                @mouseenter="handleGroupHover(group, $event)"
                @mouseleave="handleGroupLeave"
              >
                <div class="group-title-content">
                  <!-- 收起状态显示分组图标 -->
                  <n-icon 
                    v-if="is_collapse"
                    class="group-main-icon"
                    size="18"
                  >
                    <component :is="group.icon" />
                  </n-icon>
                  <span class="group-text" v-show="!is_collapse">{{ group.label }}</span>
                  <!-- 展开状态显示箭头 -->
                  <n-icon 
                    v-if="!is_collapse"
                    class="group-icon" 
                    :class="{ 'is-expanded': !groupCollapsed[group.key] }"
                    size="14"
                  >
                    <CaretRight />
                  </n-icon>
                </div>
                <div class="group-divider" v-if="!is_collapse"></div>
              </div>
              
              <!-- 子菜单项 -->
              <transition name="menu-slide">
                <div v-show="!groupCollapsed[group.key] && !is_collapse" class="menu-items">
                  <div
                    v-for="item in group.children"
                    :key="item.key"
                    class="menu-item"
                    :class="{ 'is-active': activeMenu === item.key }"
                    @click="handleMenuClick(item.key)"
                  >
                    <div class="menu-item-content">
                      <div class="menu-item-icon">
                        <n-icon size="18">
                          <component :is="item.icon" />
                        </n-icon>
                      </div>
                      <transition name="fade">
                        <span class="menu-item-text" v-show="!is_collapse">{{ item.label }}</span>
                      </transition>
                      <div class="menu-item-indicator" v-if="activeMenu === item.key"></div>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </template>
        </div>
      </n-scrollbar>
    </div>

    <!-- 底部用户信息区域 -->
    <div class="user-container">
      <n-dropdown :options="user_options" @select="handleUserSelect" trigger="click">
        <div class="user-info" :class="{ 'is-collapsed': is_collapse }">
          <div class="user-avatar">
            <n-avatar 
              round 
              size="medium" 
              :src="user_avatar" 
              fallback-src="" 
              style="background-color: #409eff;"
            >
              {{ username.charAt(0) }}
            </n-avatar>
          </div>
          <transition name="fade">
            <div class="user-detail" v-show="!is_collapse">
              <span class="user-name" :class="{ 'loading': loading }">{{ username }}</span>
              <span class="user-role">{{ user_role }}</span>
            </div>
          </transition>
          <transition name="fade">
            <n-icon class="user-dropdown-icon" v-show="!is_collapse" size="14">
              <CaretDown />
            </n-icon>
          </transition>
        </div>
      </n-dropdown>
    </div>

    <!-- 侧边栏折叠按钮 -->
    <div class="collapse-btn" @click="toggleCollapse">
      <n-icon size="16" class="collapse-icon">
        <IconChevronLeft v-if="!is_collapse" :size="16" />
        <IconChevronRight v-else :size="16" />
      </n-icon>
    </div>

    <!-- 悬停弹窗 -->
    <teleport to="body">
      <div
        v-if="tooltipVisible && is_collapse && tooltipData"
        class="sidebar-tooltip"
        :style="tooltipStyle"
        @mouseenter="handleTooltipEnter"
        @mouseleave="handleTooltipLeave"
      >
        <div class="tooltip-content">
          <div
            v-for="item in tooltipData.children"
            :key="item.key"
            class="tooltip-item"
            :class="{ 'is-active': activeMenu === item.key }"
            @click="handleMenuClick(item.key)"
          >
            <n-icon size="16" class="tooltip-item-icon">
              <component :is="item.icon" />
            </n-icon>
            <span class="tooltip-item-text">{{ item.label }}</span>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, h, computed, reactive, onMounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NIcon, NDropdown, NAvatar, NScrollbar } from 'naive-ui'
import {
  IconHome,
  IconChartBar,
  IconBook,
  IconFileText,
  IconUsers,
  IconAward,
  IconMessageCircle,
  IconCalendar,
  IconUser,
  IconLogout,
  IconSettings,
  IconChevronLeft,
  IconChevronRight,
  IconSchool,
  IconFileDescription,
  IconHelpCircle,
  CaretDown,
  CaretRight
} from '../utils/icons'
import { getStudentMe, getStudentProfile } from '@/api'

const router = useRouter()
const route = useRoute()
const is_collapse = inject('sidebarCollapsed', ref(false))
const user_name = ref('加载中...')
const username = computed(() => user_name.value)
const user_role = ref('学生')
const user_avatar = ref('')
const user_email = ref('')
const user_confirmed = ref(false)
const user_blocked = ref(false)
const activeMenu = ref('dashboard')
const loading = ref(false)

// 定义菜单项和菜单组的接口
interface MenuItem {
  label: string
  key: string
  icon: () => any
}

interface MenuGroup {
  label: string
  key: string
  type: string
  icon: () => any
  children: MenuItem[]
}

// 悬停弹窗相关
const tooltipVisible = ref(false)
const tooltipData = ref<MenuGroup | null>(null)
const tooltipStyle = ref<Record<string, string>>({})

/* ---------- 分组折叠状态 ---------- */
const groupCollapsed = reactive<Record<string, boolean>>({
  study_mgmt: false,
  info_query: false,
  career_dev: false,
  portrait: false
})

const menu_options = ref([
  {
    label: '学习管理',
    key: 'study_mgmt',
    type: 'group',
    icon: () => h(IconBook), // 学习管理图标
    children: [
      { label: '首页仪表盘', key: 'dashboard', icon: () => h(IconHome) },
      { label: '成果收集与展示', key: 'achievement', icon: () => h(IconAward) }
    ]
  },
  {
    label: '信息查询',
    key: 'info_query',
    type: 'group',
    icon: () => h(IconHelpCircle), // 信息查询图标
    children: [
      { label: '教师信息查询', key: 'teacher_info', icon: () => h(IconUsers) },
      { label: '课程安排', key: 'course_schedule', icon: () => h(IconCalendar) }
    ]
  },
  {
    label: '就业发展',
    key: 'career_dev',
    type: 'group',
    icon: () => h(IconAward), // 就业发展图标
    children: [
      { label: '简历生成', key: 'resume', icon: () => h(IconUser) },
      { label: '就业推荐', key: 'job-recommendation', icon: () => h(IconUsers) },
      { label: '人才市场', key: 'talent_market', icon: () => h(IconChartBar) }
    ]
  },
  {
    label: '个人画像',
    key: 'portrait',
    type: 'group',
    icon: () => h(IconUser), // 个人画像图标
    children: [
      { label: 'AI智能分析', key: 'portrait_analysis', icon: () => h(IconChartBar) },
      { label: 'AI对话助手', key: 'portrait_chat', icon: () => h(IconMessageCircle) }
    ]
  }
])

/* ---------- 用户下拉 ---------- */
const user_options = ref([
  { 
    label: '个人资料', 
    key: 'profile', 
    icon: () => h(IconUser),
    props: { onClick: () => console.log('个人资料') }
  },
  { 
    label: '系统设置', 
    key: 'settings', 
    icon: () => h(IconSettings),
    props: { onClick: () => console.log('系统设置') }
  },
  { 
    type: 'divider' 
  },
  { 
    label: '退出登录', 
    key: 'logout', 
    icon: () => h(IconLogout),
    props: { onClick: () => handleLogout() }
  }
])

/* ---------- 获取用户信息 ---------- */
const fetchUserInfo = async () => {
  try {
    loading.value = true
    console.log('开始获取用户信息...')
    
    // 检查是否有token
    const token = localStorage.getItem('token')
    console.log('当前token:', token ? '存在' : '不存在')
    
    // 获取基本用户信息
    console.log('调用getStudentMe API...')
    const userResponse = await getStudentMe()
    console.log('getStudentsMe响应:', userResponse)
    
    if (userResponse) {
      // 设置基本用户信息 - 优先使用档案姓名
      user_name.value = userResponse.name || userResponse.username || '用户'
      user_email.value = userResponse.email || ''
      user_confirmed.value = userResponse.confirmed || false
      user_blocked.value = userResponse.blocked || false
      
      console.log('设置用户基本信息:', {
        name: user_name.value,
        email: user_email.value,
        confirmed: user_confirmed.value,
        blocked: user_blocked.value
      })
      
      // 设置用户角色
      if (userResponse.role) {
        // 后端可能返回字符串或对象
        const roleName = typeof userResponse.role === 'string' ? userResponse.role : userResponse.role.name
        user_role.value = roleName === 'student' ? '学生' : (roleName === 'admin' ? '管理员' : roleName)
        console.log('设置用户角色:', user_role.value)
      }
    } else {
      console.warn('getStudentsMe返回空响应')
    }
    
    // 尝试获取详细档案信息
    try {
      console.log('调用getStudentProfile API...')
      const profileResponse = await getStudentProfile()
      console.log('getStudentsProfile响应:', profileResponse)
      
      // 修正：后端返回的是 basic_info 字段
      if (profileResponse && profileResponse.basic_info) {
        // 如果档案中有姓名，优先使用档案中的姓名
        if (profileResponse.basic_info.name) {
          user_name.value = profileResponse.basic_info.name
          console.log('使用档案姓名:', user_name.value)
        }
        // 设置头像
        if (profileResponse.basic_info.avatar_url) {
          user_avatar.value = profileResponse.basic_info.avatar_url
          console.log('设置用户头像:', user_avatar.value)
        }
      } else {
        console.warn('getStudentsProfile返回空档案信息')
      }
    } catch (profileError) {
      // 档案信息获取失败时，继续使用基本用户信息
      console.warn('获取用户档案信息失败:', profileError)
    }
    
    console.log('用户信息获取完成')
    
  } catch (error: any) {
    console.error('获取用户信息失败:', error)
    console.error('错误详情:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data
    })
    
    // 如果是401错误，说明需要登录
    if (error.response?.status === 401) {
      console.warn('用户未登录，显示默认信息')
      user_name.value = '未登录用户'
    } else {
      user_name.value = '用户'
    }
    user_role.value = '学生'
  } finally {
    loading.value = false
  }
}

/* ---------- 组件挂载时初始化 ---------- */
onMounted(() => {
  // 根据当前路由设置活跃菜单
  updateActiveMenu()
  // 获取用户信息
  fetchUserInfo()
})

/* ---------- 监听路由变化 ---------- */
watch(() => route.path, () => {
  updateActiveMenu()
}, { immediate: true })

/* ---------- 更新活跃菜单 ---------- */
function updateActiveMenu() {
  const path = route.path
  const routeMap: Record<string, string> = {
    '/student/dashboard': 'dashboard',
    '/student/achievement': 'achievement',
    '/student/achievement-collect': 'achievement',
    '/student/certificate-ocr': 'achievement',
    '/student/teacher-info': 'teacher_info',
    '/student/teachers': 'teacher_info',
    '/student/teacher-favorites': 'teacher_info',
    '/student/courses': 'course_schedule',
    '/student/course-schedule': 'course_schedule',
    '/student/resume': 'resume',
    '/student/job-recommendation': 'job-recommendation',
    '/student/talent-market': 'talent_market',
    '/student/portrait': 'portrait_analysis',
    '/student/portrait/chat': 'portrait_chat',
    '/student/portrait/ai-chat': 'portrait_ai_chat'
  }
  
  // 特殊处理教师详情页面
  if (path.startsWith('/student/teacher-detail/')) {
    activeMenu.value = 'teacher_info'
    return
  }
  
  activeMenu.value = routeMap[path] || 'dashboard'
}

/* ---------- 切换分组展开/折叠 ---------- */
function toggleGroup(groupKey: string) {
  if (is_collapse.value) return
  groupCollapsed[groupKey] = !groupCollapsed[groupKey]
}

/* ---------- 处理分组悬停 ---------- */
function handleGroupHover(group: any, event: MouseEvent) {
  if (!is_collapse.value) return
  
  const target = event.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()
  
  tooltipData.value = group
  
  // 立即显示弹窗
  tooltipVisible.value = true
  
  // 使用 nextTick 确保弹窗位置计算准确
  nextTick(() => {
    tooltipStyle.value = {
      position: 'fixed',
      left: rect.right + 8 + 'px',
      top: rect.top + 'px',
      zIndex: '1000',
      opacity: '1',
      transform: 'translateX(0)',
      transition: 'all 0.2s ease-out'
    }
  })
}

/* ---------- 处理分组离开 ---------- */
function handleGroupLeave() {
  if (is_collapse.value) {
    // 不立即隐藏，等待可能的鼠标移入弹窗
    setTimeout(() => {
      if (tooltipVisible.value && !isTooltipHovered.value) {
        tooltipVisible.value = false
      }
    }, 50)
  }
}

// 跟踪弹窗的悬停状态
const isTooltipHovered = ref(false)

/* ---------- 处理弹窗进入 ---------- */
function handleTooltipEnter() {
  isTooltipHovered.value = true
  tooltipVisible.value = true
}

/* ---------- 处理弹窗离开 ---------- */
function handleTooltipLeave() {
  isTooltipHovered.value = false
  tooltipVisible.value = false
}

/* ---------- 隐藏弹窗 ---------- */
function hideTooltip() {
  if (is_collapse.value) {
    isTooltipHovered.value = false
    tooltipVisible.value = false
  }
}

/* ---------- 折叠侧边栏 ---------- */
function toggleCollapse() {
  if (typeof is_collapse === 'object' && 'value' in is_collapse) {
    is_collapse.value = !is_collapse.value
  }
  // 折叠时隐藏弹窗
  if (is_collapse.value) {
    tooltipVisible.value = false
  }
}

/* ---------- 菜单点击 ---------- */
function handleMenuClick(key: string) {
  activeMenu.value = key
  
  const routeMap: Record<string, string> = {
    dashboard: '/student/dashboard',
    achievement: '/student/achievement',
    teacher_info: '/student/teacher-info',
    course_schedule: '/student/course-schedule',
    resume: '/student/resume',
    'job-recommendation': '/student/job-recommendation',
    talent_market: '/student/talent-market',
    portrait_analysis: '/student/portrait',
    portrait_chat: '/student/portrait/chat'
  }
  
  if (routeMap[key]) {
    router.push(routeMap[key])
  }
  
  // 点击菜单后隐藏弹窗
  tooltipVisible.value = false
}

/* ---------- 用户下拉选择 ---------- */
function handleUserSelect(key: string) {
  if (key === 'logout') {
    handleLogout()
  }
}

/* ---------- 登出处理 ---------- */
function handleLogout() {
  // 清除认证信息
  localStorage.removeItem('token')
  localStorage.removeItem('userInfo')
  // 跳转到学生端登录页
  router.push('/student/login')
}
</script>

<style scoped>
/* ========== 容器样式 ========== */
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(180deg, #1a237e 0%, #0d47a1 100%);
  color: #fff;
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
  width: 260px;
  position: relative;
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
}

.sidebar-container.is-collapse {
  width: 64px;
}

/* ========== 顶部Logo区域 ========== */
.logo-container {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  height: 64px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
}

.logo-icon {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  color: #fff;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
  transition: all 0.3s ease;
}

.logo-icon:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.logo-title {
  font-size: 16px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
  color: #fff;
  letter-spacing: 0.5px;
}

/* ========== 菜单容器 ========== */
.menu-container {
  flex: 1;
  overflow: hidden;
  padding: 8px 0;
}

.menu-wrapper {
  padding: 0 8px;
}

/* ========== 菜单分组 ========== */
.menu-group {
  margin-bottom: 16px;
}

.menu-group-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px 8px;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s ease;
  position: relative;
}

.menu-group-title:hover {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.menu-group-title.is-sidebar-collapsed {
  justify-content: center;
  padding: 12px 8px;
}

.group-title-content {
  display: flex;
  align-items: center;
  width: 100%;
  justify-content: space-between;
}

.group-icon {
  margin-left: 8px;
  transition: transform 0.3s ease;
  color: #bfcbd9;
}

.group-icon.is-expanded {
  transform: rotate(90deg);
}

.group-main-icon {
  color: #409eff;
  transition: all 0.3s ease;
}

.menu-group-title:hover .group-main-icon {
  color: #67c23a;
  transform: scale(1.1);
}

.group-text {
  font-size: 13px;
  font-weight: 600;
  color: #bfcbd9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.group-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.1) 50%, transparent 100%);
  margin-top: 8px;
}

/* ========== 菜单项 ========== */
.menu-items {
  padding-left: 8px;
}

.menu-item {
  position: relative;
  margin-bottom: 4px;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateX(2px);
}

.menu-item.is-active {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.menu-item.is-active:hover {
  transform: translateX(0);
}

.menu-item-content {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  position: relative;
}

.menu-item-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  margin-right: 12px;
  color: #bfcbd9;
  transition: all 0.3s ease;
}

.menu-item.is-active .menu-item-icon {
  color: #fff;
}

.menu-item-text {
  font-size: 14px;
  font-weight: 500;
  color: #e4e7ed;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.menu-item.is-active .menu-item-text {
  color: #fff;
  font-weight: 600;
}

.menu-item-indicator {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 20px;
  background: #fff;
  border-radius: 2px;
  opacity: 0.8;
}

/* ========== 用户信息区域 ========== */
.user-container {
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.08);
}

.user-info.is-collapsed {
  justify-content: center;
  padding: 8px;
}

.user-avatar {
  margin-right: 12px;
  position: relative;
}

.user-avatar::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 8px;
  height: 8px;
  background: #67c23a;
  border: 2px solid #304156;
  border-radius: 50%;
}

.user-detail {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 2px;
  transition: opacity 0.3s ease;
}

.user-name.loading {
  opacity: 0.7;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
}

.user-role {
  font-size: 12px;
  color: #bfcbd9;
}

.user-dropdown-icon {
  color: #bfcbd9;
  transition: transform 0.3s ease;
}

.user-info:hover .user-dropdown-icon {
  transform: rotate(180deg);
}

/* ========== 折叠按钮 ========== */
.collapse-btn {
  position: absolute;
  top: 80px;
  right: -12px;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  border: 2px solid #304156;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
  z-index: 10;
}

.collapse-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.collapse-icon {
  color: #fff;
  transition: transform 0.3s ease;
}

/* ========== 悬停弹窗样式 ========== */
.sidebar-tooltip {
  background: linear-gradient(135deg, #304156 0%, #273445 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  padding: 8px 0;
  min-width: 180px;
  max-width: 220px;
  z-index: 9999;
  opacity: 0;
  transform: translateX(-10px);
  transition: opacity 0.2s ease-out, transform 0.2s ease-out;
  pointer-events: auto;
}

.tooltip-content {
  padding: 0;
}

.tooltip-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tooltip-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.tooltip-item.is-active {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
}

.tooltip-item-icon {
  margin-right: 12px;
  color: #bfcbd9;
  transition: color 0.3s ease;
}

.tooltip-item.is-active .tooltip-item-icon {
  color: #fff;
}

.tooltip-item-text {
  font-size: 14px;
  color: #e4e7ed;
  transition: color 0.3s ease;
}

.tooltip-item.is-active .tooltip-item-text {
  color: #fff;
  font-weight: 600;
}

/* ========== 动画效果 ========== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.menu-slide-enter-active,
.menu-slide-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.menu-slide-enter-from,
.menu-slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

.menu-slide-enter-to,
.menu-slide-leave-from {
  max-height: 500px;
  opacity: 1;
  transform: translateY(0);
}

/* ========== 响应式设计 ========== */
@media (max-width: 768px) {
  .sidebar-container {
    width: 100%;
    position: fixed;
    z-index: 1000;
    transform: translateX(-100%);
  }
  
  .sidebar-container:not(.is-collapse) {
    transform: translateX(0);
  }
  
  .sidebar-tooltip {
    display: none;
  }
}

/* ========== 滚动条样式 ========== */
:deep(.n-scrollbar-rail) {
  background: rgba(255, 255, 255, 0.05);
}

:deep(.n-scrollbar-rail__scrollbar) {
  background: rgba(255, 255, 255, 0.2);
}

:deep(.n-scrollbar-rail__scrollbar:hover) {
  background: rgba(255, 255, 255, 0.3);
}

/* ========== 暗色模式适配 ========== */
@media (prefers-color-scheme: dark) {
  .sidebar-container {
    background: linear-gradient(180deg, #1f2937 0%, #111827 100%);
  }
  
  .logo-container {
    border-bottom-color: rgba(255, 255, 255, 0.1);
  }
  
  .user-container {
    border-top-color: rgba(255, 255, 255, 0.1);
  }
  
  .sidebar-tooltip {
    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
  }
}
</style>