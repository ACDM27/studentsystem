/**
 * AI聊天接口使用示例
 * 展示如何使用增强的AI聊天功能和学生信息查询功能
 */

import { chatWithAI, queryStudentInfo } from '@/api'

// 示例1: 使用增强的AI聊天接口（包含学生数据分析）
export const exampleChatWithStudentData = async () => {
  try {
    const response = await chatWithAI({
      session_id: null,
      message: '请分析我的学习成果和表现'
    })

    console.log('AI分析结果:', response.message)
    return response
  } catch (error) {
    console.error('AI聊天失败:', error)
    throw error
  }
}

// 示例2: 使用AI聊天接口（通用知识问答）
export const exampleChatWithoutStudentData = async () => {
  try {
    const response = await chatWithAI({
      session_id: null,
      message: '什么是机器学习？'
    })

    console.log('AI回答:', response.message)
    return response
  } catch (error) {
    console.error('AI聊天失败:', error)
    throw error
  }
}

// 示例3: 查询当前登录学生的信息
export const exampleQueryCurrentStudentInfo = async () => {
  try {
    // 不需要提供student_id，会自动获取当前登录用户的信息
    const response = await queryStudentInfo({
      question: '我的课程成绩如何？有哪些需要改进的地方？'
    })

    console.log('学生信息分析:', response.data.response)
    return response
  } catch (error) {
    console.error('查询学生信息失败:', error)
    throw error
  }
}

// 示例4: 查询指定学生的信息（需要权限）
export const exampleQuerySpecificStudentInfo = async (studentId: string) => {
  try {
    const response = await queryStudentInfo({
      question: '这个学生的学习画像是什么样的？',
      student_id: studentId
    })

    console.log('指定学生信息分析:', response.data.response)
    return response
  } catch (error) {
    console.error('查询指定学生信息失败:', error)
    throw error
  }
}

// 示例5: 综合学习分析
export const exampleComprehensiveAnalysis = async () => {
  try {
    const response = await queryStudentInfo({
      question: `请为我提供一份综合的学习分析报告，包括：
      1. 我的学习成果和优势领域
      2. 需要改进的方面
      3. 个性化的学习建议
      4. 职业发展规划建议`
    })

    console.log('综合学习分析报告:', response.data.response)
    return response
  } catch (error) {
    console.error('综合分析失败:', error)
    throw error
  }
}

// 示例6: 错误处理和降级方案
export const exampleWithErrorHandling = async () => {
  try {
    const response = await queryStudentInfo({
      question: '我的学习情况怎么样？'
    })

    if (response.data.error) {
      console.warn('AI服务不可用，显示错误信息:', response.data.response)
      // 可以在这里实现降级方案，比如显示静态建议
      return {
        data: {
          response: '当前AI服务暂时不可用，建议您查看学习统计页面了解详细信息。',
          error: true
        }
      }
    }

    return response
  } catch (error) {
    console.error('请求失败:', error)
    // 实现本地降级方案
    return {
      data: {
        response: '网络连接异常，请检查网络后重试。',
        error: true
      }
    }
  }
}

// 导出所有示例函数
export default {
  exampleChatWithStudentData,
  exampleChatWithoutStudentData,
  exampleQueryCurrentStudentInfo,
  exampleQuerySpecificStudentInfo,
  exampleComprehensiveAnalysis,
  exampleWithErrorHandling
}