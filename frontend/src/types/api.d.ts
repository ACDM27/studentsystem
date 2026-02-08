/**
 * API接口类型声明文件
 * 按REST风格命名：I{Method}{Path|ResourceName}{Resp|Req|Params}
 */

// 通用类型
export type ID = string | number

// 认证相关接口
export interface IPostAuthLocalReq {
  identifier: string
  password: string
}

export interface IPostAuthLocalResp {
  jwt: string
  user: {
    id: number
    username: string
    email: string
    // TODO: 补充更多用户信息字段
  }
}

export interface IPostAuthLogoutResp {
  success: boolean
}

export interface IPostAuthRefreshResp {
  jwt: string
}

// 学生相关接口
export interface IGetStudentsMeResp {
  id: number
  username: string
  email: string
  confirmed: boolean
  blocked: boolean
  role?: {
    id: number
    name: string
    description?: string
    type?: string
  }
  createdAt?: string
  updatedAt?: string
}

export interface IGetStudentsByIdParams {
  id: ID
}

export interface IGetStudentsByIdResp {
  id: number
  username: string
  email: string
  confirmed: boolean
  blocked: boolean
  role?: {
    id: number
    name: string
    description?: string
    type?: string
  }
  createdAt?: string
  updatedAt?: string
}

export interface IGetStudentsProfileResp {
  profile: {
    name?: string
    studentId?: string
    major?: string
    grade?: string
    college?: string
    phone?: string
    avatar?: string
    // 其他档案信息
  }
}

export interface IGetStudentsStatisticsResp {
  // TODO: 补充统计信息字段
  statistics: {
    coursesCount: number
    assignmentsCount: number
    completedAssignments: number
    // 其他统计信息
  }
}

// 课程相关接口
export interface ICourseItem {
  id: number
  code: string
  name: string
  credit: number
  teacherName: string
  teacherId?: number
  semester: 'Spring' | 'Summer' | 'Fall' | 'Winter'
  classTime: string
  classroom: string
  students?: number
  type: 'CompulsoryCourse_必修' | 'ElectiveCourse_ 选修'
  class_week: string
  coursecontent: string
  createdAt?: string
  updatedAt?: string
  publishedAt?: string
}

export interface IGetCoursesResp {
  data: Array<ICourseItem>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetCoursesByIdParams {
  id: ID
}

export interface IGetCoursesByIdResp {
  data: ICourseItem
}

export interface IPostCourseReq {
  code: string
  name: string
  credit: number
  teacherName: string
  teacherId?: number
  semester: 'Spring' | 'Summer' | 'Fall' | 'Winter'
  classTime: string
  classroom: string
  students?: number
  type: 'CompulsoryCourse_必修' | 'ElectiveCourse_ 选修'
  class_week: string
  coursecontent: string
}

export interface IPostCourseResp {
  data: ICourseItem
}

export interface IPutCourseReq {
  code?: string
  name?: string
  credit?: number
  teacherName?: string
  teacherId?: number
  semester?: 'Spring' | 'Summer' | 'Fall' | 'Winter'
  classTime?: string
  classroom?: string
  students?: number
  type?: 'CompulsoryCourse_必修' | 'ElectiveCourse_ 选修'
  class_week?: string
  coursecontent?: string
}

export interface IPutCourseResp {
  data: ICourseItem
}

export interface IDeleteCourseParams {
  id: ID
}

export interface IDeleteCourseResp {
  data: ICourseItem
}

// 作业相关接口
export interface IGetAssignmentsResp {
  data: Array<{
    id: number
    title: string
    description: string
    deadline: string
    teachers_name?: string
    assignmentcontent?: string
    createdAt?: string
    assignmentStatus?: string
    // 其他可能的字段
  }>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetAssignmentsByIdParams {
  id: ID
}

export interface IGetAssignmentsByIdResp {
  id: number
  title: string
  description: string
  deadline: string
  // TODO: 补充更多作业详情字段
}

export interface IPostAssignmentsSubmitReq {
  assignmentId: number
  content: string
  attachments?: Array<{
    name: string
    file: File
  }>
  // TODO: 补充更多提交字段
}

export interface IPostAssignmentsSubmitResp {
  id: number
  status: string
  submittedAt: string
  // TODO: 补充更多提交响应字段
}

// 咨询相关接口
export interface IGetConsultantsResp {
  data: Array<{
    id: number
    name: string
    title: string
    specialization: string
    // TODO: 补充更多咨询师字段
  }>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetConsultantsByIdParams {
  id: ID
}

export interface IGetConsultantsByIdResp {
  id: number
  name: string
  title: string
  specialization: string
  // TODO: 补充更多咨询师详情字段
}

export interface IPostConsultationsBookReq {
  consultantId: number
  date: string
  timeSlot: string
  topic: string
  // TODO: 补充更多预约字段
}

export interface IPostConsultationsBookResp {
  id: number
  status: string
  scheduledAt: string
  // TODO: 补充更多预约响应字段
}

// 咨询师相关接口
export interface IConsultTeacherItem {
  id: number
  name: string
  rating: number
  experience_years: number
  persitonal: string
  next_available_time: string
  is_online: boolean
  avatar?: any
  title: 'Lecturer' | 'Professor'
  type: 'counseling' | 'career'
  createdAt?: string
  updatedAt?: string
  publishedAt?: string
}

export interface IGetConsultTeachersResp {
  data: Array<IConsultTeacherItem>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetConsultTeacherByIdParams {
  id: ID
}

export interface IGetConsultTeacherByIdResp {
  data: IConsultTeacherItem
}

export interface IPostConsultTeacherReq {
  name: string
  rating: number
  experience_years: number
  persitonal: string
  next_available_time: string
  is_online: boolean
  avatar?: any
  title: 'Lecturer' | 'Professor'
  type: 'counseling' | 'career'
}

export interface IPostConsultTeacherResp {
  data: IConsultTeacherItem
}

export interface IPutConsultTeacherReq {
  name?: string
  rating?: number
  experience_years?: number
  persitonal?: string
  next_available_time?: string
  is_online?: boolean
  avatar?: any
  title?: 'Lecturer' | 'Professor'
  type?: 'counseling' | 'career'
}

export interface IPutConsultTeacherResp {
  data: IConsultTeacherItem
}

export interface IDeleteConsultTeacherParams {
  id: ID
}

export interface IDeleteConsultTeacherResp {
  data: IConsultTeacherItem
}

// 荣誉相关接口
export interface IGetAchievementsResp {
  data: Array<{
    id: number
    title: string
    description: string
    awardedAt: string
    type_id: string
    year: string
    level: string
    status: number
    // 其他可能的字段
  }>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetAchievementByIdParams {
  id: ID
}

export interface IGetAchievementByIdResp {
  data: {
    id: number
    title: string
    description: string
    awardedAt: string
    type_id: string
    year: string
    level: string
    status: number
    // 其他详情字段
  }
  meta?: any
}

export interface IPostAchievementReq {
  title: string
  description: string
  type_id: string
  year: string
  level: string
  awardedAt?: string
  file?: Array<{
    name: string
    file: File
  }>
}

export interface IPostAchievementResp {
  id: number
  title: string
  type_id: string
  status: number
  createdAt: string
}

export interface IPutAchievementReq {
  title?: string
  description?: string
  type_id?: string
  year?: string
  level?: string
  awardedAt?: string
  file?: Array<{
    name: string
    file: File
  }>
}

export interface IPutAchievementResp {
  id: number
  title: string
  type_id: string
  status: number
  updatedAt: string
}

export interface IDeleteAchievementResp {
  success: boolean
}

export interface IGetAchievementTypesResp {
  data: Array<{
    id: string
    name: string
    description?: string
  }>
}

// 反馈相关接口
export interface IFeedbackItem {
  id: number
  name: string
  student_id: string
  email: string
  phone: string
  date: string
  category: 'Suggestion_建议' | 'Appeal_申诉' | 'Issue_问题' | 'Other_其他'
  attachments?: any
  feedbackstatus: 'pending_待处理' | 'processing_处理中' | 'resolved_已处理'
  content?: string
  createdAt?: string
  updatedAt?: string
  publishedAt?: string
}

export interface IGetFeedbacksResp {
  data: Array<IFeedbackItem>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetFeedbackByIdParams {
  id: ID
}

export interface IGetFeedbackByIdResp {
  data: IFeedbackItem
}

export interface IPostFeedbackReq {
  name?: string
  student_id?: string
  email?: string
  phone?: string
  date?: string
  category: 'Suggestion_建议' | 'Appeal_申诉' | 'Issue_问题' | 'Other_其他'
  attachments?: any
  content: string
}

export interface IPostFeedbackResp {
  data: IFeedbackItem
}

export interface IPutFeedbackReq {
  name?: string
  student_id?: string
  email?: string
  phone?: string
  date?: string
  category?: 'Suggestion_建议' | 'Appeal_申诉' | 'Issue_问题' | 'Other_其他'
  attachments?: any
  feedbackstatus?: 'pending_待处理' | 'processing_处理中' | 'resolved_已处理'
  content?: string
}

export interface IPutFeedbackResp {
  data: IFeedbackItem
}

export interface IDeleteFeedbackParams {
  id: ID
}

export interface IDeleteFeedbackResp {
  data: IFeedbackItem
}

// 简历相关接口
export interface IGetResumeResp {
  education: Array<{
    institution: string
    degree: string
    major: string
    startDate: string
    endDate: string
  }>
  experience: Array<{
    company: string
    position: string
    description: string
    startDate: string
    endDate: string
  }>
  skills: Array<string>
  // TODO: 补充更多简历字段
}

export interface IPutResumeReq {
  education?: Array<{
    institution: string
    degree: string
    major: string
    startDate: string
    endDate: string
  }>
  experience?: Array<{
    company: string
    position: string
    description: string
    startDate: string
    endDate: string
  }>
  skills?: Array<string>
  // TODO: 补充更多简历更新字段
}

export interface IPutResumeResp {
  success: boolean
  updatedAt: string
}

// 教师相关接口
export interface IGetTeachersResp {
  data: Array<{
    id: number
    name: string
    title: 'Lecturer' | 'Professor'
    department: string
    avatar?: string | Array<string>
    researchcontent: string
    research_direction?: string
    studentCount?: number
    student_type?: string
    rating?: number
    classname?: string
    className?: string
    current_courses?: string
    officeLocation?: string
    office_location?: string
    officeHours?: string
    office_hours?: string
    recruiting?: boolean
    contactEmail?: string
    contactPhone?: string
  }>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetTeachersByIdParams {
  id: ID
}

export interface IGetTeachersByIdResp {
  id: number
  name: string
  title: 'Lecturer' | 'Professor'
  department: string
  avatar?: string | Array<string>
  researchcontent?: string
  researchContent?: string
  research_direction?: string
  studentCount?: number
  student_type?: string
  rating?: number
  classname?: string
  className?: string
  current_courses?: string
  officeLocation?: string
  office_location?: string
  officeHours?: string
  office_hours?: string
  recruiting?: boolean
  contactEmail?: string
  contactPhone?: string
}

// 新闻相关接口
export interface IGetNewsResp {
  data: Array<{
    id: number
    title: string
    content: any // blocks类型
    category: 'ExamNotice_考试通知' | 'ActivateNotice_活动通知' | 'CompetitionNotice_竞赛通知'
    publisheddate: string
  }>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetNewsByIdParams {
  id: ID
}

export interface IGetNewsByIdResp {
  id: number
  title: string
  content: any // blocks类型
  category: 'ExamNotice_考试通知' | 'ActivateNotice_活动通知' | 'CompetitionNotice_竞赛通知'
  publisheddate: string
}

export interface IPostNewsReq {
  title: string
  content: any // blocks类型
  category: 'ExamNotice_考试通知' | 'ActivateNotice_活动通知' | 'CompetitionNotice_竞赛通知'
  publisheddate: string
}

export interface IPostNewsResp {
  id: number
  title: string
  content: any // blocks类型
  category: 'ExamNotice_考试通知' | 'ActivateNotice_活动通知' | 'CompetitionNotice_竞赛通知'
  publisheddate: string
}

export interface IPutNewsReq {
  title?: string
  content?: any // blocks类型
  category?: 'ExamNotice_考试通知' | 'ActivateNotice_活动通知' | 'CompetitionNotice_竞赛通知'
  publisheddate?: string
}

export interface IPutNewsResp {
  id: number
  title: string
  content: any // blocks类型
  category: 'ExamNotice_考试通知' | 'ActivateNotice_活动通知' | 'CompetitionNotice_竞赛通知'
  publisheddate: string
}

export interface IDeleteNewsResp {
  data?: any
  meta?: any
}

// 人才市场相关接口
export interface ICompanyItem {
  id: number
  name: string
  logo?: string
  industry: string
  size: string
  location: string
  description: string
  full_desc: string
  update_time: string
  rating: number
  found_date: string
  capital: string
  nature: string
  address: string
  contact_name: string
  contact_phone: string
  contact_email: string
  website: string
  positions: Array<IPositionItem>
}

export interface IPositionItem {
  id: number
  title: string
  salary: string
  location: string
  exp_req: string
  edu_req: string
  count: string
  description: string
  full_desc: string
  skills: Array<string>
  benefits: Array<string>
}

export interface IGetCompaniesResp {
  data: Array<ICompanyItem>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetCompanyByIdParams {
  id: ID
}

export interface IGetCompanyByIdResp {
  data: ICompanyItem
}

export interface IGetPositionsResp {
  data: Array<IPositionItem>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetPositionByIdParams {
  id: ID
}

export interface IGetPositionByIdResp {
  data: IPositionItem
}

export interface IPostContactCompanyReq {
  company_id: number
  subject: string
  content: string
  contact_info: string
}

export interface IPostContactCompanyResp {
  id: number
  status: string
  submitted_at: string
}

export interface IPostApplyPositionReq {
  position_id: number
  resume_id?: number
  cover_letter?: string
}

export interface IPostApplyPositionResp {
  id: number
  status: string
  applied_at: string
}

export interface IGetMarketStatsResp {
  total_comp: number
  total_pos: number
  new_pos: number
  match_pos: number
}

// 活动相关接口
export interface IActivityItem {
  id: number
  name: string
  registration_start_time: string
  registration_end_time: string
  max_participants: number
  credits: number
  activity_type: 'collegeActivities' | 'campusActivities' | 'associationActivities' | 'youthLeagueCommitteeActivities'
  activitystatus: 'ongoing' | 'completed' | 'not_started'
  collegename?: string
  associationname?: string
  youthLeaguename?: string
  createdAt?: string
  updatedAt?: string
  publishedAt?: string
}

export interface IGetActivitiesResp {
  data: Array<IActivityItem>
  meta: {
    pagination: {
      page: number
      pageSize: number
      pageCount: number
      total: number
    }
  }
}

export interface IGetActivityByIdParams {
  id: ID
}

export interface IGetActivityByIdResp {
  data: IActivityItem
}

export interface IPostActivityReq {
  name: string
  registration_start_time: string
  registration_end_time: string
  max_participants: number
  credits: number
  activity_type: 'collegeActivities' | 'campusActivities' | 'associationActivities' | 'youthLeagueCommitteeActivities'
  activitystatus: 'ongoing' | 'completed' | 'not_started'
  collegename?: string
  associationname?: string
  youthLeaguename?: string
}

export interface IPostActivityResp {
  data: IActivityItem
}

export interface IPutActivityReq {
  name?: string
  registration_start_time?: string
  registration_end_time?: string
  max_participants?: number
  credits?: number
  activity_type?: 'collegeActivities' | 'campusActivities' | 'associationActivities' | 'youthLeagueCommitteeActivities'
  activitystatus?: 'ongoing' | 'completed' | 'not_started'
  collegename?: string
  associationname?: string
  youthLeaguename?: string
}

export interface IPutActivityResp {
  data: IActivityItem
}

export interface IDeleteActivityParams {
  id: ID
}

export interface IDeleteActivityResp {
  data: IActivityItem
}

// AI聊天相关接口
export interface IPostStudentPortraitsChatReq {
  question: string
  student_id: string
  context?: string
}

export interface IPostStudentPortraitsChatResp {
  data: {
    response: string
    timestamp: string
    student_id: string
    error?: boolean
  }
}

// 查询学生信息接口
export interface IPostQueryStudentInfoReq {
  question: string
  student_id?: string
}

export interface IPostQueryStudentInfoResp {
  data: {
    response: string
    timestamp?: string
    error?: boolean
  }
}