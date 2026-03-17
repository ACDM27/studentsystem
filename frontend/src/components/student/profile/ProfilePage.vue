<template>
  <div class="profile-page">
    <div class="profile-header">
      <h2 class="page-title">个人资料</h2>
    </div>

    <div class="profile-content">
      <!-- 左侧：头像与基本状态 -->
      <div class="profile-sidebar">
        <n-card class="avatar-card">
          <div class="avatar-wrapper">
            <n-avatar
              round
              :size="120"
              :src="avatarDisplayUrl"
              class="main-avatar"
            >
              <template #fallback>
                <n-icon size="60"><IconUser /></n-icon>
              </template>
            </n-avatar>
            <div class="avatar-upload-trigger" @click="triggerAvatarUpload">
              <n-icon size="20"><IconCamera /></n-icon>
            </div>
          </div>
          <input
            ref="avatarInputRef"
            type="file"
            accept="image/*"
            style="display: none"
            @change="handleAvatarChange"
          />
          <div class="user-brief">
            <h3 class="display-name">{{ profileData.basic_info?.name || '学生' }}</h3>
            <p class="display-role">学生用户</p>
          </div>
        </n-card>

        <!-- 成果概览（移动至此） -->
        <n-card title="成果统计" class="stats-card">
          <div class="stats-list">
            <div class="stats-item">
              <span class="label">总成果</span>
              <span class="value">{{ profileData.statistics?.total_achievements || 0 }}</span>
            </div>
            <div class="stats-item">
              <span class="label">已通过</span>
              <span class="value text-success">{{ profileData.statistics?.approved_achievements || 0 }}</span>
            </div>
            <div class="stats-item">
              <span class="label">待审核</span>
              <span class="value text-warning">{{ profileData.statistics?.pending_achievements || 0 }}</span>
            </div>
          </div>
        </n-card>
      </div>

      <!-- 右侧：详细资料 -->
      <div class="profile-main">
        <n-card title="详细档案" class="detail-card">
          <div v-if="loading" class="loading-container">
            <n-spin size="large" />
          </div>

          <n-grid v-else :cols="2" :x-gap="24" :y-gap="24">
            <n-grid-item>
              <div class="info-group">
                <label>姓名</label>
                <div class="info-value">{{ profileData.basic_info?.name || '---' }}</div>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="info-group">
                <label>学号</label>
                <div class="info-value">{{ profileData.basic_info?.student_id || '---' }}</div>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="info-group">
                <label>学院</label>
                <div class="info-value">{{ profileData.basic_info?.college || '---' }}</div>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="info-group">
                <label>专业</label>
                <div class="info-value">{{ profileData.basic_info?.major || '---' }}</div>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="info-group">
                <label>班级</label>
                <div class="info-value">{{ profileData.basic_info?.class_name || '---' }}</div>
              </div>
            </n-grid-item>
            <n-grid-item>
              <div class="info-group">
                <label>电子邮箱</label>
                <div class="info-value">{{ profileData.basic_info?.email || '---' }}</div>
              </div>
            </n-grid-item>
          </n-grid>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { 
  NCard, NAvatar, NIcon, NGrid, NGridItem, NTag, NSpin, NStatistic, useMessage 
} from 'naive-ui'
import { IconUser, IconCamera } from '../../../utils/icons'
import { getStudentProfile, updateAvatar } from '@/api'

const message = useMessage()
const loading = ref(true)
const profileData = ref<any>({})
const avatarInputRef = ref<HTMLInputElement | null>(null)

// 默认人员头像
const default_avatar = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23e0e0e0"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>'

const avatarDisplayUrl = computed(() => {
  const url = profileData.value.basic_info?.avatar_url
  if (!url) return default_avatar
  if (url.startsWith('/uploads/')) {
    const token = localStorage.getItem('token')
    return url + (token ? `?token=${token}` : '')
  }
  return url
})

const fetchProfile = async () => {
  try {
    loading.value = true
    const res = await getStudentProfile()
    profileData.value = res || {}
  } catch (err) {
    console.error('获取个人档案失败:', err)
    message.error('无法加载个人资料')
  } finally {
    loading.value = false
  }
}

const triggerAvatarUpload = () => {
  avatarInputRef.value?.click()
}

const handleAvatarChange = async (e: Event) => {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  try {
    const res = await updateAvatar(file)
    if (res && res.avatar_url) {
      if (!profileData.value.basic_info) profileData.value.basic_info = {}
      profileData.value.basic_info.avatar_url = res.avatar_url
      
      // 发送全局事件同步侧边栏头像
      window.dispatchEvent(new CustomEvent('avatar-updated', { 
        detail: { url: res.avatar_url } 
      }))
      
      message.success('头像更新成功')
    }
  } catch (err: any) {
    message.error('头像上传失败')
  } finally {
    input.value = ''
  }
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString()
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-page {
  padding: 24px;
  max-width: 1100px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.page-desc {
  color: #666;
  font-size: 16px;
}

.profile-content {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
}

/* 左侧栏样式 */
.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.avatar-card {
  text-align: center;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  margin: 20px 0;
}

.main-avatar {
  border: 4px solid #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.avatar-upload-trigger {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 36px;
  height: 36px;
  background: #1890ff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.4);
  cursor: pointer;
  transition: all 0.2s;
}

.avatar-upload-trigger:hover {
  transform: scale(1.1);
  background: #40a9ff;
}

.user-brief .display-name {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.user-brief .display-role {
  color: #999;
  font-size: 14px;
}

.stats-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 8px 0;
}

.stats-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: #fafafa;
  border-radius: 8px;
  transition: all 0.2s;
}

.stats-item:hover {
  background: #f0f7ff;
}

.stats-item .label {
  color: #666;
  font-size: 14px;
}

.stats-item .value {
  font-weight: 700;
  font-size: 18px;
  color: #1a1a1a;
  font-family: 'Din Alternate', 'Inter', sans-serif;
}

.text-success {
  color: #18a058 !important;
}

.text-warning {
  color: #f0a020 !important;
}

/* 右侧主区域样式 */
.profile-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-group label {
  display: block;
  font-size: 13px;
  color: #8c8c8c;
  margin-bottom: 8px;
}

.info-value {
  font-size: 16px;
  color: #262626;
  font-weight: 500;
  padding: 12px 16px;
  background: #f5f5f5;
  border-radius: 8px;
}

.bio-value {
  min-height: 80px;
  line-height: 1.6;
}

.loading-container {
  padding: 100px 0;
  display: flex;
  justify-content: center;
}

@media (max-width: 900px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
}
</style>
