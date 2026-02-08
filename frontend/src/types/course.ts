export interface CourseItem {
  id: string | number;
  name: string; // 课程名称
  code: string; // 课程编号
  teacher: string; // 授课教师
  description: string; // 课程描述
  time: string; // 上课时间
  location: string; // 上课地点
  students_count: number; // 选课人数
  type: 'major' | 'required' | 'elective'; // 课程类型：专业课、必修课、选修课
  credits?: number; // 学分
  type_text?: string; // 课程类型显示文本
  day?: number; // 课程安排的星期几
  slot?: number; // 课程安排的时间段
}