# 证书OCR识别组件使用说明

## 功能概述

`CertificateOcr.vue` 组件实现了证书图片的智能识别和数据保存功能，支持：

1. ✅ 上传证书图片
2. ✅ AI智能识别证书内容
3. ✅ 自动填充表单字段
4. ✅ 手动编辑和完善信息
5. ✅ 保存到后端数据库
6. ✅ 符合后端 Achievement 数据结构

## 字段映射关系

### OCR识别字段 → 前端表单字段 → 后端数据库字段

| OCR字段 (structuredData) | 前端表单字段 | 后端字段 | 说明 |
|------------------------|------------|---------|------|
| `certificateTitle` | `form.title` | `title` | 证书标题 |
| `studentNames` | `form.name` | `name` | 学生姓名（多个用逗号分隔） |
| `teacherNames` | `form.tutor_name` | `tutor_name` | 指导教师 |
| `awardDate` | `form.date` | `date` | 获奖日期 (YYYY-MM-DD) |
| `achievementType` | `form.category` | `category` | 成果类型（英文枚举） |
| `achievementLevel` | `form.level` | `level` | 成果级别（英文枚举） |
| `awardLevel` | `form.award` | `award` | 奖项等级（英文枚举） |
| `issuer` | `form.issuer` | `issuer` | 颁发机构 |
| `notes` | `form.notes` | `notes` | 备注信息 |

## 枚举值映射

### 成果类型 (category)
- `competition` - 竞赛类
- `patent` - 专利类
- `paper` - 论文类
- `project` - 项目类
- `certificate` - 证书类
- `other` - 其他

### 成果级别 (level)
- `international` - 国际级
- `national` - 国家级
- `provincial` - 省级
- `university` - 校级
- `college` - 院级
- `other` - 其他

### 奖项等级 (award) - 可选字段
- `grandprize` - 特等奖
- `firstprize` - 一等奖
- `secondprize` - 二等奖
- `thirdprize` - 三等奖
- `honorablemention` - 优秀奖
- `other` - 其他
- `""` - 空字符串（未设置）

## 使用流程

### 1. 上传证书图片
- 拖拽图片到上传区域，或点击上传
- 支持的格式：所有图片格式
- 文件大小限制：10MB
- 图片仅用于识别，不会保存

### 2. AI识别
- 点击"点击识别证书内容"按钮
- 系统调用后端 `/ocr/process` 接口
- AI模型自动识别证书信息
- 提取文字信息并填充表单

### 3. 查看和编辑
- 识别完成后，表单自动填充
- 可以手动修改任何字段
- 必填字段：证书标题、学生姓名、获奖日期、成果类型、成果级别
- 可选字段：奖项等级、指导教师、颁发机构、备注信息

### 4. 提交保存
- 点击"提交保存证书信息"按钮
- 仅保存文字信息到后端 Achievement 表
- 显示成功提示
- 表单自动重置，可继续添加

## 后端API要求

### OCR识别接口
```
POST /ocr/process
Content-Type: multipart/form-data

参数：
- image: File (证书图片文件)
- certificateType: string (可选，默认 'certificate')
- userId: string (可选，当前学生ID)

返回格式：
{
  "success": true,
  "structuredData": {
    "certificateTitle": "第六届智警杯大数据技能竞赛",
    "studentNames": "朱锋、潘思翰、吴东泽",
    "teacherNames": "秦振凯、李猛",
    "awardDate": "2024-06-01",
    "achievementLevel": "省级",
    "achievementType": "竞赛类",
    "awardLevel": "一等奖"
  },
  "tempFileUrl": "/uploads/temp/xxx.jpg"
}

或者嵌套格式：
{
  "success": true,
  "data": {
    "structuredData": {
      "certificateTitle": "第六届智警杯大数据技能竞赛",
      "studentNames": "朱锋、潘思翰、吴东泽",
      "teacherNames": "秦振凯、李猛",
      "awardDate": "2024-06-01",
      "achievementLevel": "省级",
      "achievementType": "竞赛类",
      "awardLevel": "一等奖"
    },
    "tempFileUrl": "/uploads/temp/xxx.jpg"
  }
}
```

### 创建成果接口
```
POST /api/achievements
Content-Type: application/json

请求体：
{
  "data": {
    "title": "第六届智警杯大数据技能竞赛",
    "name": "朱锋、潘思翰、吴东泽",
    "tutor_name": "秦振凯、李猛",
    "date": "2024-06-01",
    "category": "competition",
    "level": "provincial",
    "award": "firstprize",
    "issuer": "智警杯大数据技能竞赛组委会",
    "notes": "第六届，作品名：六栋五幺六",
    "student": 123,
    "student_id": "2021001"
  }
}

返回格式：
{
  "data": {
    "id": 456,
    "attributes": { ... }
  }
}
```

**注意：** 
- 图片附件需要单独处理，不能直接在创建时传入 `image_url` 字段
- 如果后端支持附件，需要先上传文件获取文件ID，然后关联到成果记录
- 或者在创建成果后，通过更新接口添加附件

## 调试方法

组件内置了详细的控制台日志，打开浏览器开发者工具查看：

1. **OCR响应数据**
   ```
   console.log('OCR 响应数据:', ocrRes)
   console.log('structuredData 对象:', structuredData)
   console.log('structuredData 来源:', ...)
   ```

2. **数据提取过程**
   ```
   console.log('从 structuredData 提取的数据:', extractedInfo)
   console.log('writeToForm 执行后，form:', form)
   ```

3. **提交数据**
   ```
   console.log('提交到后端的数据：', submitData)
   console.log('保存成功，响应：', response)
   ```

## 图片处理说明

### 识别流程
1. **上传图片**：用户上传证书图片到前端
2. **AI识别**：图片发送到后端OCR服务进行识别
3. **提取信息**：从识别结果中提取文字信息
4. **自动填充**：将提取的信息填充到表单

### 图片存储策略
- ⚠️ **图片不保存**：识别完成后，图片仅用于预览，不会保存到数据库
- ✅ **仅保存文字**：只保存识别出的文字信息（标题、姓名、日期等）
- 💡 **手动上传**：如需保存证书图片，请在成果详情页面手动上传附件

### 为什么不自动保存图片？
1. 避免存储空间浪费
2. 减少上传失败的风险
3. 简化提交流程
4. 用户可以选择性地保存重要证书图片

## 常见问题

### Q1: 识别后表单没有自动填充？
**A:** 检查控制台日志，查看：
- OCR接口是否返回了 `structuredData` 对象
- `structuredData` 中的字段名是否正确
- `writeToForm` 函数是否被调用
- 代码会自动兼容旧的 `prefillFields` 格式

### Q2: 提交时报错 "ValidationError"？
**A:** 这说明字段值不符合后端验证规则：
- **枚举值错误**：检查 `category`、`level`、`award` 是否使用正确的英文枚举值
- **必填字段缺失**：确保 `title`、`name`、`date`、`category`、`level` 都已填写
- **日期格式错误**：确保日期格式为 `YYYY-MM-DD`
- 查看控制台的详细错误信息

**常见枚举值错误：**
- ❌ `excellence` → ✅ `honorablemention` (优秀奖)
- ❌ `participation` → ✅ 留空或选择 `other`
- ❌ 中文值 → ✅ 必须使用英文枚举值

### Q3: 证书图片保存在哪里？
**A:** 
- 图片不会自动保存到数据库
- 仅用于AI识别和前端预览
- 如需保存图片，请在成果详情页面手动上传附件

### Q4: 如何自定义字段映射？
**A:** 修改以下函数：
- `writeToForm()` - 控制如何将识别结果填充到表单
- 识别逻辑中的字段提取部分 - 控制如何从OCR结果中提取数据

## 扩展功能

### 添加跳转到成果列表
取消 `submitForm` 函数中的注释：
```javascript
setTimeout(() => {
  ElMessageBox.confirm('是否前往查看成果列表？', '保存成功', {
    confirmButtonText: '查看列表',
    cancelButtonText: '继续添加',
    type: 'success'
  }).then(() => {
    window.location.href = '/student/honors'
  })
}, 1000)
```

### 添加批量上传
参考 `batchOcr` API 接口，支持一次上传多张证书。

## 技术栈

- Vue 3 Composition API
- Element Plus UI组件库
- 后端OCR服务（通义千问视觉模型）
- Strapi v5 后端API
