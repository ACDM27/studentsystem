<template>
  <div class="admin-dashboard">
    <el-card class="welcome-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>欢迎，{{ adminName }}</span>
        </div>
      </template>
      <div class="welcome-content">
        <p>您已成功登录学生综合信息服务平台管理端。</p>
        <p>请从左侧菜单选择功能进行操作。</p>
      </div>
    </el-card>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="待审核成果" :value="stats.pending">
            <template #suffix>
              <span class="stat-unit">个</span>
            </template>
          </el-statistic>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="已通过成果" :value="stats.approved">
            <template #suffix>
              <span class="stat-unit">个</span>
            </template>
          </el-statistic>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic title="总成果数" :value="stats.total">
            <template #suffix>
              <span class="stat-unit">个</span>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="quick-actions-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>快捷操作</span>
        </div>
      </template>
      <div class="quick-actions">
        <el-button type="primary" size="large" @click="goToAchievements">
          <el-icon><List /></el-icon>
          查看成果审核
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { List } from '@element-plus/icons-vue'
import { getAdminInfo } from '@/utils/admin-auth'
import { getAchievementsForReview } from '@/api'

const router = useRouter()

// 管理员信息
const adminName = ref('管理员')

// 统计数据
const stats = ref({
  pending: 0,
  approved: 0,
  total: 0
})

/**
 * 加载统计数据
 */
const loadStats = async () => {
  try {
    // 加载所有成果统计
    const [allRes, pendingRes, approvedRes] = await Promise.all([
      getAchievementsForReview({}),
      getAchievementsForReview({ status: 'pending' }),
      getAchievementsForReview({ status: 'approved' })
    ])

    stats.value = {
      total: allRes.total || 0,
      pending: pendingRes.total || 0,
      approved: approvedRes.total || 0
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.error('加载统计数据失败')
  }
}

/**
 * 跳转到成果审核页
 */
const goToAchievements = () => {
  router.push('/admin/achievements')
}

// 组件挂载时加载数据
onMounted(() => {
  const adminInfo = getAdminInfo()
  if (adminInfo) {
    adminName.value = adminInfo.name || '管理员'
  }
  loadStats()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  font-size: 18px;
  font-weight: 600;
}

.welcome-content {
  font-size: 14px;
  line-height: 1.8;
  color: #606266;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-unit {
  font-size: 14px;
  color: #909399;
}

.quick-actions-card {
  margin-bottom: 20px;
}

.quick-actions {
  display: flex;
  gap: 12px;
}
</style>
