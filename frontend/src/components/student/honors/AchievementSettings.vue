<template>
  <div class="achievement_settings_page">
    <!-- 页面顶部区域 -->
    <div class="header_area">
      <div class="title_info">
        <n-button quaternary @click="go_back">
          <template #icon>
            <IconArrowLeft :size="24" />
          </template>
          返回
        </n-button>
        <h2>成果规则设置</h2>
      </div>
    </div>

    <!-- 规则设置卡片 -->
    <n-card class="settings_card" title="成果规则配置">
      <n-tabs type="line" animated>
        <!-- 基本规则设置 -->
        <n-tab-pane name="basic" tab="基本规则">
          <n-form
            ref="formRef"
            :model="basicSettings"
            :rules="basicRules"
            label-placement="left"
            label-width="120px"
            require-mark-placement="right-hanging"
          >
            <n-form-item label="成果收集开放" path="isOpen">
              <n-switch v-model:value="basicSettings.isOpen" />
            </n-form-item>
            <n-form-item label="每学期最大数量" path="maxPerSemester">
              <n-input-number v-model:value="basicSettings.maxPerSemester" :min="1" :max="20" />
            </n-form-item>
            <n-form-item label="单次提交最大数量" path="maxPerSubmission">
              <n-input-number v-model:value="basicSettings.maxPerSubmission" :min="1" :max="10" />
            </n-form-item>
            <n-form-item label="允许的文件类型" path="allowedFileTypes">
              <n-select
                v-model:value="basicSettings.allowedFileTypes"
                multiple
                :options="fileTypeOptions"
                placeholder="请选择允许上传的文件类型"
              />
            </n-form-item>
            <n-form-item label="单个文件最大大小(MB)" path="maxFileSize">
              <n-input-number v-model:value="basicSettings.maxFileSize" :min="1" :max="50" />
            </n-form-item>
          </n-form>
        </n-tab-pane>

        <!-- 成果类型设置 -->
        <n-tab-pane name="types" tab="成果类型">
          <div class="type_settings">
            <div class="type_list">
              <n-list bordered>
                <n-list-item v-for="type in achievementTypes" :key="type.id">
                  <div class="type_item">
                    <div class="type_info">
                      <component :is="get_type_icon(type.id)" :size="24" />
                      <span class="type_name">{{ type.name }}</span>
                    </div>
                    <div class="type_actions">
                      <n-button text @click="edit_type(type)">
                        <template #icon>
                          <IconEdit :size="20" />
                        </template>
                      </n-button>
                      <n-popconfirm
                        positive-text="确定"
                        negative-text="取消"
                        @positive-click="delete_type(type.id)"
                      >
                        <template #trigger>
                          <n-button text>
                            <template #icon>
                              <IconTrash :size="20" />
                            </template>
                          </n-button>
                        </template>
                        确定要删除此成果类型吗？
                      </n-popconfirm>
                    </div>
                  </div>
                </n-list-item>
              </n-list>
              <n-button class="add_type_btn" @click="showAddTypeModal = true">
                <template #icon>
                  <IconPlus :size="20" />
                </template>
                添加成果类型
              </n-button>
            </div>
          </div>
        </n-tab-pane>

        <!-- 审核流程设置 -->
        <n-tab-pane name="approval" tab="审核流程">
          <n-form
            :model="approvalSettings"
            label-placement="left"
            label-width="120px"
          >
            <n-form-item label="启用审核流程" path="enableApproval">
              <n-switch v-model:value="approvalSettings.enableApproval" />
            </n-form-item>
            <n-form-item label="审核级别" path="approvalLevels">
              <n-select
                v-model:value="approvalSettings.approvalLevels"
                :options="approvalLevelOptions"
                placeholder="请选择审核级别"
                :disabled="!approvalSettings.enableApproval"
              />
            </n-form-item>
            <n-form-item label="审核人员" path="approvers">
              <n-select
                v-model:value="approvalSettings.approvers"
                multiple
                :options="approverOptions"
                placeholder="请选择审核人员"
                :disabled="!approvalSettings.enableApproval"
              />
            </n-form-item>
            <n-form-item label="审核时限(天)" path="approvalTimeLimit">
              <n-input-number
                v-model:value="approvalSettings.approvalTimeLimit"
                :min="1"
                :max="30"
                :disabled="!approvalSettings.enableApproval"
              />
            </n-form-item>
          </n-form>
        </n-tab-pane>
      </n-tabs>

      <div class="form_actions">
        <n-button type="primary" @click="save_settings">保存设置</n-button>
        <n-button @click="reset_settings">重置</n-button>
      </div>
    </n-card>

    <!-- 添加成果类型弹窗 -->
    <n-modal
      v-model:show="showAddTypeModal"
      title="添加成果类型"
      preset="card"
      style="width: 500px"
    >
      <n-form
        ref="typeFormRef"
        :model="newType"
        :rules="typeRules"
        label-placement="left"
        label-width="100px"
      >
        <n-form-item label="类型名称" path="name">
          <n-input v-model:value="newType.name" placeholder="请输入成果类型名称" />
        </n-form-item>
        <n-form-item label="类型描述" path="description">
          <n-input
            v-model:value="newType.description"
            type="textarea"
            placeholder="请输入成果类型描述"
          />
        </n-form-item>
        <n-form-item label="图标" path="icon">
          <n-select
            v-model:value="newType.icon"
            :options="iconOptions"
            placeholder="请选择图标"
          />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddTypeModal = false">取消</n-button>
          <n-button type="primary" @click="add_type">确定</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import type { FormInst, FormRules, SelectOption } from 'naive-ui'
import {
  IconArrowLeft,
  IconEdit,
  IconTrash,
  IconPlus,
  IconBook2,
  IconCode,
  IconUsers,
  IconAward,
  IconMusic,
  IconFileText,
  IconBulb,
  IconCertificate
} from '@tabler/icons-vue'

const router = useRouter()
const message = useMessage()

// 表单引用
const formRef = ref<FormInst | null>(null)
const typeFormRef = ref<FormInst | null>(null)

// 基本设置数据
const basicSettings = reactive({
  isOpen: true,
  maxPerSemester: 10,
  maxPerSubmission: 3,
  allowedFileTypes: ['pdf', 'jpg', 'png'],
  maxFileSize: 10
})

// 审核流程设置
const approvalSettings = reactive({
  enableApproval: true,
  approvalLevels: 'department',
  approvers: ['teacher1', 'teacher2'],
  approvalTimeLimit: 7
})

// 新增类型数据
const newType = reactive({
  name: '',
  description: '',
  icon: ''
})

// 成果类型列表
const achievementTypes = ref([
  { id: '1', name: '竞赛', description: '包括各类学科竞赛、创新创业比赛等' },
  { id: '2', name: '科研', description: '包括科研项目、研究成果等' },
  { id: '3', name: '项目', description: '包括创新创业项目、实践项目等' },
  { id: '4', name: '论文', description: '包括学术论文、研究报告等' },
  { id: '5', name: '专利', description: '包括发明专利、实用新型专利、外观设计专利等' },
  { id: '6', name: '证书', description: '包括专业资格证书、技能证书等' }
])

// 表单验证规则
const basicRules: FormRules = {
  maxPerSemester: [
    { required: true, message: '请输入每学期最大数量', trigger: 'blur' },
    { type: 'number', min: 1, max: 20, message: '数量必须在1-20之间', trigger: 'blur' }
  ],
  maxPerSubmission: [
    { required: true, message: '请输入单次提交最大数量', trigger: 'blur' },
    { type: 'number', min: 1, max: 10, message: '数量必须在1-10之间', trigger: 'blur' }
  ],
  allowedFileTypes: [
    { required: true, type: 'array', min: 1, message: '请至少选择一种文件类型', trigger: 'blur' }
  ],
  maxFileSize: [
    { required: true, message: '请输入最大文件大小', trigger: 'blur' },
    { type: 'number', min: 1, max: 50, message: '大小必须在1-50MB之间', trigger: 'blur' }
  ]
}

const typeRules: FormRules = {
  name: [
    { required: true, message: '请输入类型名称', trigger: 'blur' },
    { min: 2, max: 20, message: '名称长度必须在2-20个字符之间', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入类型描述', trigger: 'blur' },
    { min: 5, max: 100, message: '描述长度必须在5-100个字符之间', trigger: 'blur' }
  ],
  icon: [
    { required: true, message: '请选择图标', trigger: 'blur' }
  ]
}

// 选项数据
const fileTypeOptions: SelectOption[] = [
  { label: 'PDF文档', value: 'pdf' },
  { label: 'JPG图片', value: 'jpg' },
  { label: 'PNG图片', value: 'png' },
  { label: 'DOC文档', value: 'doc' },
  { label: 'DOCX文档', value: 'docx' },
  { label: 'XLS表格', value: 'xls' },
  { label: 'XLSX表格', value: 'xlsx' },
  { label: 'PPT演示文稿', value: 'ppt' },
  { label: 'PPTX演示文稿', value: 'pptx' },
  { label: 'ZIP压缩包', value: 'zip' }
]

const approvalLevelOptions: SelectOption[] = [
  { label: '学院级审核', value: 'department' },
  { label: '学校级审核', value: 'school' },
  { label: '双级审核', value: 'both' }
]

const approverOptions: SelectOption[] = [
  { label: '张老师', value: 'teacher1' },
  { label: '李老师', value: 'teacher2' },
  { label: '王老师', value: 'teacher3' },
  { label: '赵主任', value: 'director1' },
  { label: '刘院长', value: 'dean1' }
]

const iconOptions: SelectOption[] = [
  { label: '书本', value: 'book' },
  { label: '代码', value: 'code' },
  { label: '团队', value: 'users' },
  { label: '奖杯', value: 'award' },
  { label: '文档', value: 'file' },
  { label: '灯泡', value: 'bulb' },
  { label: '证书', value: 'certificate' }
]

// 显示控制
const showAddTypeModal = ref(false)

// 获取类型图标
const get_type_icon = (typeId: string) => {
  const iconMap: Record<string, any> = {
    '1': IconAward,
    '2': IconBook2,
    '3': IconCode,
    '4': IconFileText,
    '5': IconBulb,
    '6': IconCertificate
  }
  return iconMap[typeId] || IconFileText
}

// 返回上一页
const go_back = () => {
  router.back()
}

// 编辑类型
const edit_type = (type: any) => {
  // 实际项目中应该打开编辑弹窗并填充数据
  message.info(`编辑类型: ${type.name}`)
}

// 删除类型
const delete_type = (id: string) => {
  // 实际项目中应该调用API删除数据
  achievementTypes.value = achievementTypes.value.filter(type => type.id !== id)
  message.success('删除成功')
}

// 添加类型
const add_type = () => {
  typeFormRef.value?.validate((errors) => {
    if (!errors) {
      // 实际项目中应该调用API保存数据
      const newId = (achievementTypes.value.length + 1).toString()
      achievementTypes.value.push({
        id: newId,
        name: newType.name,
        description: newType.description
      })
      message.success('添加成功')
      showAddTypeModal.value = false
      // 重置表单
      newType.name = ''
      newType.description = ''
      newType.icon = ''
    }
  })
}

// 保存设置
const save_settings = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      // 实际项目中应该调用API保存数据
      message.success('设置保存成功')
      console.log('基本设置:', basicSettings)
      console.log('审核设置:', approvalSettings)
    }
  })
}

// 重置设置
const reset_settings = () => {
  // 重置为初始值
  basicSettings.isOpen = true
  basicSettings.maxPerSemester = 10
  basicSettings.maxPerSubmission = 3
  basicSettings.allowedFileTypes = ['pdf', 'jpg', 'png']
  basicSettings.maxFileSize = 10
  
  approvalSettings.enableApproval = true
  approvalSettings.approvalLevels = 'department'
  approvalSettings.approvers = ['teacher1', 'teacher2']
  approvalSettings.approvalTimeLimit = 7
  
  message.info('已重置为默认设置')
}

// 获取设置数据
const fetch_settings = async () => {
  try {
    // 实际项目中应该调用API获取数据
    // 这里使用模拟数据
    console.log('获取设置数据')
    // 如果有API，可以这样调用
    // const response = await getAchievementSettings()
    // basicSettings.isOpen = response.data.isOpen
    // ...
  } catch (error) {
    console.error('获取设置数据失败:', error)
    message.error('获取设置数据失败，请稍后重试')
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetch_settings()
})
</script>

<style scoped>
.achievement_settings_page {
  padding: 20px;
}

.header_area {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  background-color: #f5f7fa;
  padding: 16px 20px;
  border-radius: 8px;
}

.title_info {
  display: flex;
  align-items: center;
}

.title_info h2 {
  margin: 0 0 0 16px;
  font-size: 20px;
}

.settings_card {
  margin-bottom: 24px;
}

.form_actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.type_settings {
  margin-top: 16px;
}

.type_item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.type_info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type_name {
  font-weight: 500;
}

.type_actions {
  display: flex;
  gap: 8px;
}

.add_type_btn {
  margin-top: 16px;
}
</style>