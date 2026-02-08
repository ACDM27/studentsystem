<template>
  <div class="teacher_detail_page">
    <!-- 页面顶部区域 - 显示教师名称和职称 -->
    <n-card class="header_card">
      <div class="header_area">
        <div class="back_btn">
          <n-button quaternary @click="goBack">
            <template #icon>
              <ArrowLeft :size="24" />
            </template>
            返回列表
          </n-button>
        </div>
        <div class="title_info">
          <div class="title_row">
            <User :size="24" />
            <h2>{{ teacher_data?.name || '教师详情' }}</h2>
            <span class="teacher_title">{{ title_map[teacher_data?.title || ''] || teacher_data?.title || '' }}</span>
          </div>
        </div>
        <div class="action_btns">
          <n-button type="primary" @click="toggleFavorite" class="favorite_btn">
            <template #icon>
              <StarFilled v-if="is_favorite" :size="24" />
              <Star v-else :size="24" />
            </template>
            {{ is_favorite ? '已收藏' : '收藏教师' }}
          </n-button>
        </div>
      </div>
    </n-card>

    <!-- 加载状态 -->
    <n-spin :show="loading" description="加载教师信息中...">
      <template #description>
        <span>加载教师信息中...</span>
      </template>

      <!-- 主要内容区域 -->
      <div class="detail_content" v-if="teacher_data">
        <!-- 基本信息和联系方式 -->
        <n-grid :cols="24" :x-gap="16">
          <!-- 左侧基本信息 -->
          <n-grid-item :span="16">
            <n-card title="基本信息" class="info_card">
              <div class="basic_info">
                <div class="avatar_area">
                  <n-avatar
                    round
                    :size="120"
                    :src="getAvatarUrl(teacher_data)"
                    fallback-src="/placeholder-avatar.jpg"
                  />
                </div>
                <div class="info_list">
                  <div class="info_item">
                    <Award :size="24" />
                    <span class="info_label">职称：</span>
                    <span>{{ title_map[teacher_data.title || ''] || teacher_data.title || '暂无信息' }}</span>
                  </div>
                  <div class="info_item">
                    <Building :size="24" />
                    <span class="info_label">所属学院：</span>
                    <span>{{ teacher_data.college || '暂无信息' }}</span>
                  </div>
                  <div class="info_item">
                    <Compass :size="24" />
                    <span class="info_label">研究方向：</span>
                    <span>{{ teacher_data.research_direction || '暂无信息' }}</span>
                  </div>
                  <div class="info_item">
                    <Star :size="24" />
                    <span class="info_label">教学评分：</span>
                    <n-rate readonly :value="teacher_data.rating || 0" :count="5" />
                    <span class="rating_value">{{ (teacher_data.rating || 0).toFixed(1) }}</span>
                  </div>
                  <div class="info_item">
                    <Users :size="24" />
                    <span class="info_label">招收学生：</span>
                    <span>{{ teacher_data.student_type || '暂无信息' }}</span>
                  </div>
                  <div class="info_item">
                    <Trophy :size="24" />
                    <span class="info_label">荣誉奖项：</span>
                    <span>{{ teacher_data.honors || '暂无信息' }}</span>
                  </div>
                </div>
              </div>
            </n-card>
          </n-grid-item>

          <!-- 右侧联系方式 -->
          <n-grid-item :span="8">
            <n-card title="联系方式" class="contact_card">
              <div class="contact_info">
                <div class="contact_item">
                  <Mail :size="24" />
                  <span class="contact_label">邮箱：</span>
                  <span>{{ teacher_data.email || '暂无信息' }}</span>
                </div>
                <div class="contact_item">
                  <Phone :size="24" />
                  <span class="contact_label">电话：</span>
                  <span>{{ teacher_data.phone || '暂无信息' }}</span>
                </div>
                <div class="contact_item">
                  <MapPin :size="24" />
                  <span class="contact_label">办公地点：</span>
                  <span>{{ teacher_data.office_location || '暂无信息' }}</span>
                </div>
                <div class="contact_item">
                  <Clock :size="24" />
                  <span class="contact_label">办公时间：</span>
                  <span>{{ teacher_data.office_hours || '暂无信息' }}</span>
                </div>
                <div class="contact_btn_area">
                  <n-button type="primary" block @click="contactTeacher">
                    <template #icon>
                      <Mail :size="24" />
                    </template>
                    联系教师
                  </n-button>
                </div>
              </div>
            </n-card>
          </n-grid-item>
        </n-grid>

        <!-- 详细信息标签页 -->
        <n-card class="tabs_card">
          <n-tabs type="line" animated>
            <!-- 个人简介 -->
            <n-tab-pane name="profile" tab="个人简介">
              <div class="tab_content">
                <n-collapse arrow-placement="right">
                  <!-- 工作经历 -->
                  <n-collapse-item title="工作经历" name="work_exp">
                    <div class="collapse_content">
                      <n-timeline>
                        <n-timeline-item v-for="(exp, index) in work_experience" :key="index" :title="exp.title" :content="exp.content" :time="exp.time" />
                      </n-timeline>
                    </div>
                  </n-collapse-item>
                  
                  <!-- 教育背景 -->
                  <n-collapse-item title="教育背景" name="education">
                    <div class="collapse_content">
                      <n-timeline>
                        <n-timeline-item v-for="(edu, index) in education_background" :key="index" :title="edu.title" :content="edu.content" :time="edu.time" />
                      </n-timeline>
                    </div>
                  </n-collapse-item>
                  
                  <!-- 最新动态 -->
                  <n-collapse-item title="最新动态" name="news">
                    <div class="collapse_content">
                      <div v-for="(news, index) in latest_news" :key="index" class="news_item">
                        <div class="news_title">{{ news.title }}</div>
                        <div class="news_time">{{ news.time }}</div>
                        <div class="news_content">{{ news.content }}</div>
                      </div>
                    </div>
                  </n-collapse-item>
                  
                  <!-- 荣誉奖项 -->
                  <n-collapse-item title="荣誉奖项" name="honors">
                    <div class="collapse_content">
                      <div v-for="(honor, index) in honors_list" :key="index" class="honor_item">
                        <div class="honor_title">{{ honor.title }}</div>
                        <div class="honor_time">{{ honor.time }}</div>
                        <div class="honor_desc">{{ honor.description }}</div>
                      </div>
                    </div>
                  </n-collapse-item>
                </n-collapse>
              </div>
            </n-tab-pane>
            
            <!-- 科研成果 -->
            <n-tab-pane name="research" tab="科研成果">
              <div class="tab_content">
                <n-collapse arrow-placement="right">
                  <!-- 研究方向 -->
                  <n-collapse-item title="研究方向" name="research_dir">
                    <div class="collapse_content">
                      <div class="research_dir_content">{{ teacher_data.research_direction || '暂无研究方向信息' }}</div>
                    </div>
                  </n-collapse-item>
                  
                  <!-- 代表性论文 -->
                  <n-collapse-item title="代表性论文" name="papers">
                    <div class="collapse_content">
                      <div v-for="(paper, index) in papers_list" :key="index" class="paper_item">
                        <div class="paper_title">{{ paper.title }}</div>
                        <div class="paper_authors">{{ paper.authors }}</div>
                        <div class="paper_journal">{{ paper.journal }}</div>
                        <div class="paper_year">{{ paper.year }}</div>
                      </div>
                    </div>
                  </n-collapse-item>
                  
                  <!-- 已发表论文统计 -->
                  <n-collapse-item title="已发表论文统计" name="paper_stats">
                    <div class="collapse_content">
                      <div class="stats_item">
                        <span class="stats_label">SCI论文：</span>
                        <span class="stats_value">{{ paper_stats.sci || 0 }}</span>
                      </div>
                      <div class="stats_item">
                        <span class="stats_label">EI论文：</span>
                        <span class="stats_value">{{ paper_stats.ei || 0 }}</span>
                      </div>
                      <div class="stats_item">
                        <span class="stats_label">核心期刊：</span>
                        <span class="stats_value">{{ paper_stats.core || 0 }}</span>
                      </div>
                      <div class="stats_item">
                        <span class="stats_label">会议论文：</span>
                        <span class="stats_value">{{ paper_stats.conference || 0 }}</span>
                      </div>
                      <div class="stats_item">
                        <span class="stats_label">总引用次数：</span>
                        <span class="stats_value">{{ paper_stats.citations || 0 }}</span>
                      </div>
                    </div>
                  </n-collapse-item>
                </n-collapse>
              </div>
            </n-tab-pane>
            
            <!-- 项目介绍 -->
            <n-tab-pane name="projects" tab="项目介绍">
              <div class="tab_content">
                <div v-for="(project, index) in projects_list" :key="index" class="project_item">
                  <n-card :title="project.title" class="project_card">
                    <div class="project_content">
                      <div class="project_desc">
                        <div class="project_label">项目介绍：</div>
                        <div class="project_text">{{ project.description }}</div>
                      </div>
                      <div class="project_research">
                        <div class="project_label">研究内容：</div>
                        <div class="project_text">{{ project.research_content }}</div>
                      </div>
                      <div class="project_info_row">
                        <div class="project_info_item">
                          <span class="project_info_label">项目经费：</span>
                          <span class="project_info_value">{{ project.funding }}</span>
                        </div>
                        <div class="project_info_item">
                          <span class="project_info_label">承担角色：</span>
                          <span class="project_info_value">{{ project.role }}</span>
                        </div>
                        <div class="project_info_item">
                          <span class="project_info_label">项目状态：</span>
                          <n-tag :type="getProjectStatusType(project.status)">
                            {{ project.status }}
                          </n-tag>
                        </div>
                      </div>
                    </div>
                  </n-card>
                </div>
              </div>
            </n-tab-pane>
            
            <!-- 教学工作 -->
            <n-tab-pane name="teaching" tab="教学工作">
              <div class="tab_content">
                <div v-for="(course, index) in courses_list" :key="index" class="course_item">
                  <n-card :title="course.title" class="course_card">
                    <div class="course_content">
                      <div class="course_info_row">
                        <div class="course_info_item">
                          <span class="course_info_label">课程分类：</span>
                          <span class="course_info_value">{{ course.category }}</span>
                        </div>
                        <div class="course_info_item">
                          <span class="course_info_label">选课学生：</span>
                          <span class="course_info_value">{{ course.students }}</span>
                        </div>
                        <div class="course_info_item">
                          <span class="course_info_label">课程评分：</span>
                          <n-rate readonly :value="course.rating" :count="5" size="small" />
                          <span class="course_rating_value">{{ course.rating.toFixed(1) }}</span>
                        </div>
                      </div>
                      <div class="course_desc">
                        <div class="course_label">课程介绍：</div>
                        <div class="course_text">{{ course.description }}</div>
                      </div>
                    </div>
                  </n-card>
                </div>
              </div>
            </n-tab-pane>
            
            <!-- 招收学生 -->
            <n-tab-pane name="students" tab="招收学生">
              <div class="tab_content">
                <n-card title="指导学生统计" class="students_card">
                  <div class="students_stats">
                    <div class="stats_item">
                      <span class="stats_label">博士生：</span>
                      <span class="stats_value">{{ student_stats.phd || 0 }}</span>
                    </div>
                    <div class="stats_item">
                      <span class="stats_label">硕士生：</span>
                      <span class="stats_value">{{ student_stats.master || 0 }}</span>
                    </div>
                    <div class="stats_item">
                      <span class="stats_label">本科生：</span>
                      <span class="stats_value">{{ student_stats.bachelor || 0 }}</span>
                    </div>
                    <div class="stats_item">
                      <span class="stats_label">已毕业学生：</span>
                      <span class="stats_value">{{ student_stats.graduated || 0 }}</span>
                    </div>
                  </div>
                </n-card>
                
                <n-card title="招生要求" class="requirements_card">
                  <div class="requirements_content">
                    <div v-if="recruitment_requirements.length > 0">
                      <div v-for="(req, index) in recruitment_requirements" :key="index" class="req_item">
                        <div class="req_title">{{ req.title }}</div>
                        <div class="req_content">{{ req.content }}</div>
                      </div>
                    </div>
                    <div v-else class="no_data">暂无招生要求信息</div>
                  </div>
                </n-card>
              </div>
            </n-tab-pane>
            
            <!-- 学生评价 -->
            <n-tab-pane name="reviews" tab="学生评价">
              <div class="tab_content">
                <div v-if="student_reviews.length > 0">
                  <div v-for="(review, index) in student_reviews" :key="index" class="review_item">
                    <n-card class="review_card">
                      <template #header>
                        <div class="review_header">
                          <div class="review_course">{{ review.course }}</div>
                          <div class="review_time">{{ review.time }}</div>
                        </div>
                      </template>
                      <div class="review_content">{{ review.content }}</div>
                      <div class="review_footer">
                        <div class="review_likes">
                          <ThumbUp :size="16" />
                          <span>{{ review.likes }}</span>
                        </div>
                      </div>
                    </n-card>
                  </div>
                </div>
                <div v-else class="no_data">暂无学生评价</div>
              </div>
            </n-tab-pane>
          </n-tabs>
        </n-card>
      </div>
      
      <!-- 无数据提示 -->
      <n-empty v-else description="未找到教师信息" />
    </n-spin>

    <!-- 联系教师模态框 -->
      <div class="contact_form_container">
        <!-- 居中遮罩 -->
        <n-modal
          v-model:show="show_contact_modal"
          preset="dialog"
          :show-icon="false"
          :closable="false"
          :mask-closable="true"
          :style="{ width: '920px', top: '10vh' }"
          content-style="padding: 0"
        >

            <div class="contact_form_container">
              <!-- 标题（可选） -->
              <div class="form_header">
                <h3>加入导师团队申请表</h3>
              </div>

              <!-- 表单内容：一行两列 -->
              <n-form
                ref="contact_form_ref"
                :model="contact_form"
                :rules="contact_rules"
                label-placement="left"
                label-width="auto"
                require-mark-placement="right-hanging"
                style="padding: 24px 32px"
              >
                <n-grid :cols="2" :x-gap="32">
                  <!-- 左侧 -->
                  <n-gi>
                    <div class="form_section">
                      <h4 class="section_title">
                        <User :size="20" />
                        基本信息
                      </h4>

                      <n-form-item label="姓名" path="student_name">
                        <n-input v-model:value="contact_form.student_name" placeholder="请输入您的真实姓名" clearable />
                      </n-form-item>

                      <n-form-item label="学号" path="student_id">
                        <n-input v-model:value="contact_form.student_id" placeholder="请输入您的学号" clearable />
                      </n-form-item>

                      <n-form-item label="邮箱" path="student_email">
                        <n-input v-model:value="contact_form.student_email" placeholder="请输入您的邮箱地址" clearable />
                      </n-form-item>

                      <n-form-item label="手机号" path="student_phone">
                        <n-input v-model:value="contact_form.student_phone" placeholder="请输入您的手机号" clearable />
                      </n-form-item>

                      <n-form-item label="专业" path="student_major">
                        <n-input v-model:value="contact_form.student_major" placeholder="请输入您的专业" clearable />
                      </n-form-item>

                      <n-form-item label="年级" path="student_grade">
                        <n-select
                          v-model:value="contact_form.student_grade"
                          placeholder="请选择您的年级"
                          :options="[
                            { label: '大一', value: '大一' },
                            { label: '大二', value: '大二' },
                            { label: '大三', value: '大三' },
                            { label: '大四', value: '大四' },
                          ]"
                        />
                      </n-form-item>
                    </div>
                  </n-gi>

                  <!-- 右侧 -->
                  <n-gi>
                    <div class="form_section">
                      <h4 class="section_title">
                        <Award :size="20" />
                        申请信息
                      </h4>

                      <n-form-item label="申请理由" path="apply_reason">
                        <n-input
                          v-model:value="contact_form.apply_reason"
                          type="textarea"
                          placeholder="请详细说明您希望加入该教师团队的理由（至少20字）"
                          :rows="5"
                          show-count
                          maxlength="500"
                        />
                      </n-form-item>

                      <n-form-item label="研究兴趣">
                        <n-input
                          v-model:value="contact_form.research_interest"
                          type="textarea"
                          placeholder="请简述您的研究兴趣和方向（选填）"
                          :rows="4"
                          show-count
                          maxlength="300"
                        />
                      </n-form-item>

                      <n-form-item label="自我介绍">
                        <n-input
                          v-model:value="contact_form.self_intro"
                          type="textarea"
                          placeholder="请简单介绍一下自己，包括学习经历、技能特长等（选填）"
                          :rows="4"
                          show-count
                          maxlength="300"
                        />
                      </n-form-item>
                    </div>
                  </n-gi>
                </n-grid>
              </n-form>

              <!-- 底部按钮（可选） -->
              <div class="form_footer">
                <n-button @click="show_contact_modal = false">取消</n-button>
                <n-button type="primary" style="margin-left: 12px" @click="submit_contact">提交申请</n-button>
              </div>
            </div>
        </n-modal>
      </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { 
  IconUser as User,
  IconArrowLeft as ArrowLeft,
  IconStar as Star,
  IconStarFilled as StarFilled,
  IconMail as Mail,
  IconPhone as Phone,
  IconMapPin as MapPin,
  IconClock as Clock,
  IconAward as Award,
  IconBuilding as Building,
  IconCompass as Compass,
  IconUsers as Users,
  IconTrophy as Trophy,
  IconThumbUp as ThumbUp
} from '@tabler/icons-vue'
import { getTeacherById, getFileUrl } from '@/api'
import axios from 'axios'
import request from '@/utils/request'

// 后端配置
const getBaseURL = () => (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')
const backendUrl = getBaseURL().replace('/api', '')
const http = request

// 获取头像URL
const getAvatarUrl = (teacher: any): string => {

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
};

// 路由和消息
const route = useRoute()
const router = useRouter()
const message = useMessage()

// 获取教师ID
const teacher_id = computed(() => route.params.id as string)

// 加载状态
const loading = ref<boolean>(true)

// 教师数据
const teacher_data = ref<any>(null)

// 收藏状态
const is_favorite = ref<boolean>(false)

// 职称映射表 - 将英文职称转换为中文
const title_map: Record<string, string> = {
  'Lecturer': '讲师',
  'Professor': '教授',
  'associate professor': '副教授',
  'assistant professor': '助理教授',
  'associate': '副教授',
  'assistant': '助教'
}



// 工作经历
const work_experience = ref([
  { title: '教授', content: '计算机学院', time: '2015年至今' },
  { title: '副教授', content: '计算机学院', time: '2010年-2015年' },
  { title: '讲师', content: '计算机学院', time: '2005年-2010年' }
])

// 教育背景
const education_background = ref([
  { title: '博士', content: '计算机科学与技术', time: '2000年-2005年' },
  { title: '硕士', content: '软件工程', time: '1997年-2000年' },
  { title: '学士', content: '计算机科学与技术', time: '1993年-1997年' }
])

// 最新动态
const latest_news = ref([
  { title: '获得优秀教师奖', time: '2023-05-20', content: '在2023年教师评选中获得优秀教师称号' },
  { title: '发表SCI论文', time: '2023-03-15', content: '在国际期刊发表题为《人工智能在教育中的应用》的论文' },
  { title: '主持新项目', time: '2023-01-10', content: '获批国家自然科学基金项目' }
])

// 荣誉奖项
const honors_list = ref([
  { title: '优秀教师', time: '2023年', description: '校级优秀教师称号' },
  { title: '教学成果奖', time: '2022年', description: '省级教学成果一等奖' },
  { title: '科研创新奖', time: '2021年', description: '国家级科研创新奖' }
])

// 论文列表
const papers_list = ref([
  { title: '人工智能在教育中的应用研究', authors: '李明华, 张三, 王五', journal: 'IEEE Transactions on Education', year: '2023' },
  { title: '机器学习算法在学生行为分析中的应用', authors: '李明华, 赵六', journal: 'Journal of Educational Data Mining', year: '2022' },
  { title: '深度学习在智能教育系统中的实践', authors: '李明华, 刘七, 孙八', journal: 'AI in Education', year: '2021' }
])

// 论文统计
const paper_stats = ref({
  sci: 15,
  ei: 20,
  core: 10,
  conference: 25,
  citations: 500
})

// 项目列表
const projects_list = ref([
  {
    title: '智能教育平台开发',
    description: '基于人工智能的智能教育平台开发与应用',
    research_content: '研究人工智能技术在教育领域的应用，开发智能教学系统',
    funding: '100万元',
    role: '项目负责人',
    status: '进行中'
  },
  {
    title: '学生行为分析系统',
    description: '基于大数据的学生行为分析与预测系统',
    research_content: '利用大数据技术分析学生学习行为，预测学习成果',
    funding: '80万元',
    role: '主要研究员',
    status: '已完成'
  },
  {
    title: '智能评分系统',
    description: '基于自然语言处理的智能作业评分系统',
    research_content: '研究自然语言处理技术在自动评分中的应用',
    funding: '50万元',
    role: '项目负责人',
    status: '筹备中'
  }
])

// 课程列表
const courses_list = ref([
  {
    title: '人工智能导论',
    category: '本科生必修课',
    students: '120人',
    rating: 4.8,
    description: '本课程介绍人工智能的基本概念、方法和应用，包括搜索算法、知识表示、机器学习等内容'
  },
  {
    title: '机器学习',
    category: '研究生必修课',
    students: '60人',
    rating: 4.7,
    description: '本课程深入讲解机器学习的理论基础和算法实现，包括监督学习、无监督学习、强化学习等内容'
  },
  {
    title: '深度学习',
    category: '研究生选修课',
    students: '45人',
    rating: 4.9,
    description: '本课程介绍深度学习的基本原理和前沿进展，包括卷积神经网络、循环神经网络、生成对抗网络等内容'
  }
])

// 学生统计
const student_stats = ref({
  phd: 5,
  master: 15,
  bachelor: 30,
  graduated: 50
})

// 招生要求
const recruitment_requirements = ref([
  {
    title: '博士生招生要求',
    content: '具有扎实的计算机科学基础，熟悉人工智能、机器学习相关理论，有较强的编程能力和研究潜力'
  },
  {
    title: '硕士生招生要求',
    content: '本科为计算机相关专业，有良好的数学基础，对人工智能或数据科学有浓厚兴趣'
  },
  {
    title: '本科生科研要求',
    content: '学习成绩优秀，对科研有热情，有一定的编程基础，愿意投入时间参与科研项目'
  }
])

// 学生评价
const student_reviews = ref([
  {
    course: '人工智能导论',
    time: '2023-06-15',
    content: '老师讲课非常清晰，案例丰富，理论与实践结合得很好，是我上过的最好的课程之一',
    likes: 35
  },
  {
    course: '机器学习',
    time: '2023-05-20',
    content: '课程内容充实，老师讲解深入浅出，作业设计合理，对我的研究有很大帮助',
    likes: 28
  },
  {
    course: '深度学习',
    time: '2023-04-10',
    content: '老师对前沿知识把握准确，课堂互动性强，项目实践很有挑战性，收获很大',
    likes: 42
  }
])

// 获取项目状态对应的标签类型
const getProjectStatusType = (status: string): string => {
  const statusMap: Record<string, string> = {
    '筹备中': 'info',
    '进行中': 'success',
    '已完成': 'default'
  }
  return statusMap[status] || 'default'
}

// 安全获取环境变量
const getEnvVar = (key: string, defaultValue: string = '') => {
  try {
    if (typeof import.meta !== 'undefined' && import.meta.env) {
      return import.meta.env[key] || defaultValue
    }
    return defaultValue
  } catch (error) {
    console.warn(`无法获取环境变量 ${key}:`, error)
    return defaultValue
  }
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

// 从缓存获取教师数据
const get_cached_teacher = (id: string): any => {
  try {
    // 尝试从sessionStorage获取缓存的教师数据
    const cachedData = sessionStorage.getItem(`teacher_${id}`)
    if (cachedData) {
      console.log('从缓存获取教师详情:', id)
      return JSON.parse(cachedData)
    }
    
    // 尝试从路由state获取数据
    if (router.currentRoute.value.params.teacherData) {
      const routeData = router.currentRoute.value.params.teacherData as any
      return routeData
    }
    
    return null
  } catch (error) {
    console.warn('获取缓存数据失败:', error)
    return null
  }
}

// 使用默认数据（当API调用失败或无数据时）
const use_default_data = () => {
  teacher_data.value = {
    id: teacher_id.value,
    name: '模拟教师',
    title: '教授',
    college: '计算机学院',
    research_direction: '人工智能、机器学习',
    student_type: '本科生、研究生',
    rating: 4.5,
    current_courses: '人工智能导论',
    office_location: '计算机楼A301',
    office_hours: '周一、周三 14:00-16:00',
    avatar: '',
    email: 'teacher@example.com',
    phone: '138-0000-0000',
    honors: '优秀教师奖'
  }
  message.warning('当前显示的是模拟数据，请检查后端服务')
}

// 处理教师数据
const process_teacher_data = (teacherData: any) => {
  // 输出原始数据，帮助调试
  console.log('原始教师数据:', JSON.stringify(teacherData, null, 2))
  console.log('研究方向相关字段:', {
    researchContent: teacherData.researchContent,
    research_direction: teacherData.research_direction,
    researchDirections: teacherData.researchDirections,
    research_directions: teacherData.research_directions
  })
  
  // 处理教师详情数据
  teacher_data.value = {
    id: teacherData.id || '',
    name: teacherData.name || '',
    title: teacherData.title || '',
    college: teacherData.department || teacherData.college || '',
    research_direction: teacherData.researchContent || teacherData.research_direction || teacherData.researchDirections || teacherData.research_directions || '',
    student_type: teacherData.studentCount?.toString() || teacherData.student_type || '',
    rating: Number(teacherData.rating) || 0,
    current_courses: teacherData.classname || teacherData.current_courses || '',
    office_location: teacherData.officeLocation || teacherData.office_location || '',
    office_hours: teacherData.officeHours || teacherData.office_hours || '',
    avatar: teacherData.attributes?.avatar?.data?.attributes?.url || teacherData.avatar || '',
    email: teacherData.email || '',
    phone: teacherData.phone || '',
    honors: teacherData.honors || ''
  }
  
  // 输出处理后的数据，帮助调试
  console.log('处理后的教师数据:', teacher_data.value)
  
  // 如果有更多详细数据，可以在这里处理
  if (teacherData.workExperience) {
    work_experience.value = teacherData.workExperience
  }
  
  if (teacherData.education) {
    education_background.value = teacherData.education
  }
  
  if (teacherData.news) {
    latest_news.value = teacherData.news
  }
  
  if (teacherData.honorsList) {
    honors_list.value = teacherData.honorsList
  }
  
  if (teacherData.papers) {
    papers_list.value = teacherData.papers
  }
  
  if (teacherData.paperStats) {
    paper_stats.value = teacherData.paperStats
  }
  
  if (teacherData.projects) {
    projects_list.value = teacherData.projects
  }
  
  if (teacherData.courses) {
    courses_list.value = teacherData.courses
  }
  
  if (teacherData.studentStats) {
    student_stats.value = teacherData.studentStats
  }
  
  if (teacherData.recruitmentRequirements) {
    recruitment_requirements.value = teacherData.recruitmentRequirements
  }
  
  if (teacherData.studentReviews) {
    student_reviews.value = teacherData.studentReviews
  }
  
  console.log('处理后的教师详情数据:', teacher_data.value)
  
  // 缓存数据到sessionStorage
   try {
     sessionStorage.setItem(`teacher_${teacher_id.value}`, JSON.stringify(teacherData))
   } catch (e) {
     console.warn('缓存教师数据失败:', e)
   }
}

// 获取教师详情数据
const fetchTeacherDetail = async (): Promise<void> => {
  loading.value = true
  
  // 校验教师ID是否为有效数字
  const teacherId = teacher_id.value
  if (!teacherId || isNaN(Number(teacherId))) {
    console.error('无效的教师ID:', teacherId)
    message.error('教师ID无效，请检查链接')
    loading.value = false
    return
  }
  
  try {
    console.log('正在获取教师详情，ID:', teacherId)
    
    try {
      console.log('尝试从API获取教师详情...')
      console.log('请求URL:', `${getEnvVar('VITE_API_BASE_URL', 'http://localhost:1337/api')}/teachers/${teacherId}`)
      
      const response = await getTeacherById(teacherId)

      console.log('教师详情API响应:', response)
      
      // 输出详细的响应结构，便于调试
      console.log('响应完整结构:', JSON.stringify(response))
      
      // 更灵活地处理不同的数据结构
      let teacherData = null
      
      // 检查响应结构，适应不同的后端返回格式
      if (response.data) {
        if (response.data.data) {
          teacherData = response.data.data
          console.log('使用 response.data.data 结构')
        } else if (Array.isArray(response.data) && response.data.length > 0) {
          teacherData = response.data[0]
          console.log('使用 response.data[0] 结构（数组格式）')
        } else {
          teacherData = response.data
          console.log('使用 response.data 结构')
        }
        
        // 检查是否获取到有效数据
        if (!teacherData || (typeof teacherData === 'object' && Object.keys(teacherData).length === 0)) {
          console.error('未获取到有效的教师数据')
          throw new Error('未找到该教师的详细信息')
        }
        
        // 处理并保存教师数据
        process_teacher_data(teacherData)
        return
      } else {
        console.error('响应中没有 data 字段')
        throw new Error('获取教师详情失败：响应格式错误')
      }
    } catch (apiError: any) {
      console.warn('详情API调用失败，尝试其他方式:', apiError.message)
      
      // 策略3: 从教师列表API获取所有数据，然后筛选
       try {
         console.log('尝试从教师列表API获取数据...')
         const listResponse = await http.get('/teachers')
         console.log('教师列表API响应:', listResponse)
        
        if (listResponse.data) {
          let teachers: any[] = []
          
          // 处理不同的响应格式
          if (Array.isArray(listResponse.data)) {
            teachers = listResponse.data
          } else if (listResponse.data.data && Array.isArray(listResponse.data.data)) {
            teachers = listResponse.data.data
          }
          
          // 查找匹配的教师
          const targetTeacher = teachers.find((item: any) => 
            String(item.id) === String(teacher_id.value)
          )
          
          if (targetTeacher) {
            console.log('从列表API找到教师数据:', targetTeacher)
            process_teacher_data(targetTeacher)
            return
          }
        }
        
        console.warn('⚠️ 列表API中未找到教师数据')
        throw new Error('未在教师列表中找到该教师')
      } catch (listError) {
        console.warn('⚠️ 教师列表API也失败了:', listError)
        throw apiError // 重新抛出原始错误
      }
    }
    
  } catch (error: any) {
    console.error('获取教师详情失败:', error)
    
    // 详细的错误处理
    if (error.response) {
      const status = error.response.status
      const statusText = error.response.statusText
      console.error(`HTTP错误 ${status}: ${statusText}`)
      
      switch (status) {
        case 404:
          message.error(`教师信息不存在 (ID: ${teacherId})`)
          console.error('可能的原因：')
          console.error('1. 教师ID不存在于数据库中')
          console.error('2. 后端API路径不正确')
          console.error('3. 数据库连接问题')
          
          // 404错误时，延迟跳转回教师列表页
          setTimeout(() => {
            router.push('/student/teachers')
          }, 2000)
          break
        case 500:
          message.error('服务器内部错误，请稍后重试')
          break
        case 403:
          message.error('没有权限访问该教师信息')
          break
        default:
          message.error(`获取教师详情失败 (${status}: ${statusText})`)
      }
    } else if (error.request) {
      console.error('网络请求失败:', error.request)
      message.error('网络连接失败，请检查网络连接')
    } else {
      console.error('请求配置错误:', error.message)
      message.error('请求配置错误，请联系管理员')
    }
    
    // 仅在开发环境下提供模拟数据
    if (isDevelopment()) {
      console.log('开发环境：使用模拟教师数据')
      use_default_data()
    }
  } finally {
    loading.value = false
  }
}

// 返回上一页
const goBack = (): void => {
  router.back()
}

// 切换收藏状态
const toggleFavorite = (): void => {
  // 从本地存储获取收藏列表
  const saved_favorites = localStorage.getItem('favorite_teachers')
  let favorite_ids: string[] = []
  
  if (saved_favorites) {
    try {
      favorite_ids = JSON.parse(saved_favorites)
    } catch (e) {
      console.error('解析收藏数据失败:', e)
      favorite_ids = []
    }
  }
  
  const index = favorite_ids.indexOf(teacher_id.value)
  if (index === -1) {
    // 添加收藏
    favorite_ids.push(teacher_id.value)
    is_favorite.value = true
    message.success('已添加到收藏')
  } else {
    // 取消收藏
    favorite_ids.splice(index, 1)
    is_favorite.value = false
    message.success('已取消收藏')
  }
  
  // 保存到本地存储
  localStorage.setItem('favorite_teachers', JSON.stringify(favorite_ids))
}

// 联系教师表单相关状态
const show_contact_modal = ref<boolean>(false)
const contact_form = ref({
  student_name: '',
  student_id: '',
  student_email: '',
  student_phone: '',
  student_major: '',
  student_grade: '',
  apply_reason: '',
  research_interest: '',
  self_intro: ''
})

// 表单验证规则
const contact_rules = {
  student_name: {
    required: true,
    message: '请输入您的姓名',
    trigger: ['input', 'blur']
  },
  student_id: {
    required: true,
    message: '请输入您的学号',
    trigger: ['input', 'blur']
  },
  student_email: {
    required: true,
    message: '请输入您的邮箱',
    trigger: ['input', 'blur'],
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  },
  student_phone: {
    required: true,
    message: '请输入您的手机号',
    trigger: ['input', 'blur'],
    pattern: /^1[3-9]\d{9}$/
  },
  student_major: {
    required: true,
    message: '请输入您的专业',
    trigger: ['input', 'blur']
  },
  student_grade: {
    required: true,
    message: '请选择您的年级',
    trigger: ['change', 'blur']
  },
  apply_reason: {
    required: true,
    message: '请填写申请理由',
    trigger: ['input', 'blur'],
    min: 20
  }
}

// 联系教师
const contactTeacher = (): void => {
  show_contact_modal.value = true
}

// 提交联系申请
const submit_contact = async (): Promise<void> => {
  try {
    // 这里可以添加实际的API调用
    console.log('提交联系申请:', contact_form.value)
    
    message.success('申请已提交，教师将会尽快回复您！')
    show_contact_modal.value = false
    
    // 重置表单
    contact_form.value = {
      student_name: '',
      student_id: '',
      student_email: '',
      student_phone: '',
      student_major: '',
      student_grade: '',
      apply_reason: '',
      research_interest: '',
      self_intro: ''
    }
  } catch (error) {
    console.error('提交申请失败:', error)
    message.error('提交申请失败，请稍后重试')
  }
}

// 取消联系申请
const cancel_contact = (): void => {
  show_contact_modal.value = false
}

// 检查是否已收藏
const checkFavoriteStatus = (): void => {
  const saved_favorites = localStorage.getItem('favorite_teachers')
  if (saved_favorites) {
    try {
      const favorite_ids = JSON.parse(saved_favorites)
      is_favorite.value = favorite_ids.includes(teacher_id.value)
    } catch (e) {
      console.error('解析收藏数据失败:', e)
      is_favorite.value = false
    }
  }
}

// 组件挂载时获取数据
onMounted(() => {
  // 检查收藏状态
  checkFavoriteStatus()
  
  // 获取教师详情数据
  fetchTeacherDetail()
})
</script>

<style scoped>
.teacher_detail_page {
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
}

.back_btn {
  margin-right: 16px;
}

.title_info {
  flex: 1;
}

.title_row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.title_info h2 {
  margin: 0 10px;
  font-size: 20px;
}

.teacher_title {
  font-size: 16px;
  color: #666;
  margin-left: 8px;
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

.detail_content {
  margin-top: 24px;
}

.info_card,
.contact_card {
  margin-bottom: 24px;
}

.basic_info {
  display: flex;
  margin-bottom: 16px;
}

.avatar_area {
  margin-right: 24px;
}

.info_list {
  flex: 1;
}

.info_item,
.contact_item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: #333;
  font-size: 14px;
}

.info_item svg,
.contact_item svg {
  margin-right: 8px;
  color: #2080f0;
}

.info_label,
.contact_label {
  font-weight: bold;
  margin-right: 4px;
  width: 80px;
}

.rating_value {
  margin-left: 8px;
  color: #f0a020;
  font-weight: bold;
}

.contact_btn_area {
  margin-top: 24px;
}

.tabs_card {
  margin-top: 24px;
}

.tab_content {
  padding: 16px 0;
}

.collapse_content {
  padding: 16px;
}

.news_item,
.honor_item,
.paper_item,
.req_item {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.news_item:last-child,
.honor_item:last-child,
.paper_item:last-child,
.req_item:last-child {
  border-bottom: none;
}

.news_title,
.honor_title,
.paper_title,
.req_title {
  font-weight: bold;
  font-size: 16px;
  margin-bottom: 8px;
}

.news_time,
.honor_time,
.paper_year {
  color: #999;
  font-size: 12px;
  margin-bottom: 8px;
}

.news_content,
.honor_desc,
.paper_journal,
.paper_authors,
.req_content {
  color: #666;
  font-size: 14px;
}

.research_dir_content {
  font-size: 14px;
  line-height: 1.6;
}

.stats_item {
  display: flex;
  margin-bottom: 12px;
}

.stats_label {
  font-weight: bold;
  width: 100px;
}

.stats_value {
  color: #2080f0;
  font-weight: bold;
}

.project_item,
.course_item {
  margin-bottom: 24px;
}

.project_card,
.course_card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.project_content,
.course_content {
  padding: 8px 0;
}

.project_desc,
.project_research,
.course_desc {
  margin-bottom: 16px;
}

.project_label,
.course_label {
  font-weight: bold;
  margin-bottom: 8px;
}

.project_text,
.course_text {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
}

.project_info_row,
.course_info_row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.project_info_item,
.course_info_item {
  display: flex;
  align-items: center;
}

.project_info_label,
.course_info_label {
  font-weight: bold;
  margin-right: 8px;
}

.course_rating_value {
  margin-left: 8px;
  color: #f0a020;
}

.students_card,
.requirements_card {
  margin-bottom: 24px;
}

.students_stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.review_item {
  margin-bottom: 16px;
}

.review_card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.review_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.review_course {
  font-weight: bold;
}

.review_time {
  color: #999;
  font-size: 12px;
}

.review_content {
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
}

.review_footer {
  display: flex;
  justify-content: flex-end;
}

.review_likes {
  display: flex;
  align-items: center;
  color: #2080f0;
}

.review_likes svg {
  margin-right: 4px;
}

.no_data {
  color: #999;
  text-align: center;
  padding: 24px 0;
}

/* 联系教师表单样式 - 横向窗口设计 */
.contact_modal {
  max-width: 1400px;
  width: 95vw;
  min-width: 800px;
}

.modal_header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #2080f0;
}

.contact_form_container {
  padding: 20px 0;
  max-height: 70vh;
  overflow-y: auto;
}

.form_section {
  margin-bottom: 20px;
}

.section_title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  padding-bottom: 6px;
  border-bottom: 2px solid #f0f0f0;
}

.modal_actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.cancel_btn {
  min-width: 80px;
}

.submit_btn {
  min-width: 100px;
  background-color: #2080f0;
}

.submit_btn:hover {
  background-color: #1c7ed6;
}

/* 表单项样式优化 */
.contact_form_container .n-form-item {
  margin-bottom: 16px;
}

.contact_form_container .n-form-item-label {
  font-weight: 500;
  color: #333;
}

.contact_form_container .n-input,
.contact_form_container .n-select {
  border-radius: 6px;
}

.contact_form_container .n-input:focus-within,
.contact_form_container .n-select:focus-within {
  border-color: #2080f0;
  box-shadow: 0 0 0 2px rgba(32, 128, 240, 0.1);
}

/* 横向布局分栏样式 */
.contact_form_container .n-grid > .n-grid-item:first-child {
  border-right: 1px solid #f0f0f0;
  padding-right: 20px;
}

.contact_form_container .n-grid > .n-grid-item:last-child {
  padding-left: 20px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .contact_modal {
    max-width: 95vw;
  }
  
  .contact_form_container .n-grid > .n-grid-item:first-child {
    border-right: none;
    padding-right: 0;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 20px;
    margin-bottom: 20px;
  }
  
  .contact_form_container .n-grid > .n-grid-item:last-child {
    padding-left: 0;
  }
}

@media (max-width: 768px) {
  .contact_modal {
    max-width: 95vw;
    margin: 10px;
  }
}

.contact_form_container {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.form_header {
  padding: 20px 32px 0;
  font-size: 18px;
  font-weight: 600;
}

.form_section {
  padding: 8px 0;
}

.section_title {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.form_footer {
  display: flex;
  justify-content: flex-end;
  padding: 0 32px 24px;
}

</style>