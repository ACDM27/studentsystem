<template>
  <div class="achievement-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">成果审核管理</h2>
    </div>

    <!-- 筛选条件 -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="状态">
          <el-select
            v-model="filters.status"
            placeholder="全部"
            clearable
            @change="handleFilter"
          >
            <el-option label="待审核" value="pending" />
            <el-option label="已通过" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>

        <el-form-item label="学生姓名">
          <el-input
            v-model="filters.studentName"
            placeholder="请输入学生姓名"
            clearable
            @clear="handleFilter"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleFilter">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><RefreshRight /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 成果列表 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="achievementList"
        stripe
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="student_name" label="学生姓名" width="120" />
        
        <el-table-column prop="title" label="成果标题" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="type" label="成果类型" width="100">
          <template #default="{ row }">
            {{ ACHIEVEMENT_TYPE_TEXT[row.type] || row.type }}
          </template>
        </el-table-column>
        
        <el-table-column prop="teacher_name" label="指导教师" width="120" />
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="STATUS_COLOR[row.status]">
              {{ STATUS_TEXT[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="create_time" label="提交时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.create_time) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="handleViewDetail(row)"
            >
              查看详情
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              size="small"
              @click="handleAudit(row)"
            >
              审核
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页器 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="PAGE_SIZE_OPTIONS"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <achievement-detail-dialog
      v-model="detailDialogVisible"
      :achievement="currentAchievement"
      @success="handleAuditSuccess"
    />

    <!-- 审核弹窗 -->
    <audit-dialog
      v-model="auditDialogVisible"
      :achievement="currentAchievement"
      @success="handleAuditSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, RefreshRight } from '@element-plus/icons-vue'
import { getAchievementsForReview } from '@/api'
import type { Achievement } from '@/api/types'
import {
  STATUS_TEXT,
  STATUS_COLOR,
  ACHIEVEMENT_TYPE_TEXT,
  DEFAULT_PAGE_SIZE,
  PAGE_SIZE_OPTIONS
} from '@/utils/constants'
import AchievementDetailDialog from './AchievementDetailDialog.vue'
import AuditDialog from './AuditDialog.vue'

// 筛选条件
const filters = reactive({
  status: '',
  studentName: ''
})

// 分页数据
const pagination = reactive({
  page: 1,
  pageSize: DEFAULT_PAGE_SIZE,
  total: 0
})

// 列表数据
const achievementList = ref<Achievement[]>([])
const loading = ref(false)

// 弹窗状态
const detailDialogVisible = ref(false)
const auditDialogVisible = ref(false)
const currentAchievement = ref<Achievement | null>(null)

/**
 * 加载成果列表
 */
const loadAchievements = async () => {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      page_size: pagination.pageSize
    }

    if (filters.status) {
      params.status = filters.status
    }
    if (filters.studentName) {
      params.student_name = filters.studentName
    }

    const res = await getAchievementsForReview(params)
    achievementList.value = res.list || []
    pagination.total = res.total || 0
  } catch (error) {
    console.error('加载成果列表失败:', error)
    ElMessage.error('加载成果列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 格式化日期时间
 */
const formatDateTime = (dateStr: string): string => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return dateStr
  }
}

/**
 * 处理筛选
 */
const handleFilter = () => {
  pagination.page = 1
  loadAchievements()
}

/**
 * 重置筛选条件
 */
const handleReset = () => {
  filters.status = ''
  filters.studentName = ''
  pagination.page = 1
  loadAchievements()
}

/**
 * 处理分页大小变化
 */
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  loadAchievements()
}

/**
 * 处理页码变化
 */
const handlePageChange = (page: number) => {
  pagination.page = page
  loadAchievements()
}

/**
 * 查看详情
 */
const handleViewDetail = (achievement: Achievement) => {
  currentAchievement.value = achievement
  detailDialogVisible.value = true
}

/**
 * 审核成果
 */
const handleAudit = (achievement: Achievement) => {
  currentAchievement.value = achievement
  auditDialogVisible.value = true
}

/**
 * 审核成功回调
 */
const handleAuditSuccess = () => {
  loadAchievements()
}

// 组件挂载时加载数据
onMounted(() => {
  loadAchievements()
})
</script>

<style scoped>
.achievement-list-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #1e2730;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  margin: 0;
}

.table-card {
  margin-bottom: 20px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
