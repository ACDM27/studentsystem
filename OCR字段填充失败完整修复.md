# OCR字段填充失败完整修复方案

## 问题现状（根据截图）

| 字段 | 状态 | 问题 |
|------|------|------|
| 参赛学生 | "加载中..." | ❌ getStudentMe() API调用问题 |
| 成果标题 | "荣誉证书" | ✅ 正常 |
| 获奖日期 | "2024-06-01" | ✅ 正常 |
| 成果类别 | "竞赛类" | ✅ 正常 |
| 具体奖项 | 红色错误"奖项必填" | ❌ OCR返回award:null |
| 奖项等级 | "校级" | ✅ 正常 |
| 指导教师 | placeholder | ❌ 字段名错误advisor_name |

## 三个核心问题及修复

### 问题1：参赛学生显示"加载中..."

**原因**：`getStudentMe()` API可能失败或数据结构不匹配

**检查步骤**：
1. 打开浏览器控制台（F12）
2. 查看Network标签，找到`/api/student/me`请求
3. 检查返回数据结构

**可能的返回格式**：
```json
// 格式A expect
{
  "username": "student001",
  "name": "张三"
}

// 格式B（嵌套在data中）
{
  "code": 200,
  "data": {
    "username": "student001",
    "name": "张三"
  }
}
```

**修复代码**（CertificateOcr.vue 第632-638行）：

```javascript
// 修复后的代码 - 兼容多种返回格式
try {
    const response = await getStudentMe()
    console.log('获取学生信息:', response)  // 🔍 调试日志
    
    // 兼容性处理
    const u = response?.data || response
    
    if (u) {
        // 优先使用name，其次username
        current_user_name.value = u.name || u.username || '未知用户'
        console.log('当前用户名:', current_user_name.value)  // 🔍 调试日志
    } else {
        console.error('用户数据为空')
        current_user_name.value = '未知用户'
    }
} catch(e) { 
    console.error('获取用户信息失败', e) 
    current_user_name.value = '未知用户'  // 🔑 失败时设置默认值
}
```

---

### 问题2：具体奖项未填充

**原因**：OCR返回`award: null`，AI把"优秀奖"错误地放到了`award_level`

**OCR实际返回**：
```json
{
  "award": null,
  "award_level": "优秀奖"
}
```

**修复代码**（CertificateOcr.vue 第447行）：

```javascript
// ===  修复：处理award字段，添加容错逻辑 ===
// 优先使用award字段，如果为空则从award_level提取
if (raw.award) {
  item.data.award = raw.award
} else if (raw.award_level) {
  // 🔑 容错：如果award_level包含"奖"字，可能是AI误放
  const levelText = String(raw.award_level)
  // 检查是否包含具体奖项关键词
  const awardKeywords = ['一等奖', '二等奖', '三等奖', '优秀奖', '特等奖', '铜奖', '银奖', '金奖']
  const hasAwardKeyword = awardKeywords.some(keyword => levelText.includes(keyword))
  
  if (hasAwardKeyword) {
    item.data.award = levelText  // 将"优秀奖"等填充到award
    console.log('🔧 容错：从award_level提取具体奖项:', levelText)
  }
}
```

---

### 问题3：指导教师未填充

**原因**：前端代码使用了错误的字段名`advisor_name`，应该是`advisors`数组

**OCR返回**：
```json
{
  "advisors": ["潘卫华"]  // ✅ 正确格式
}
```

**前端错误代码**（第450行）：
```javascript
// ❌ 错误代码
if (raw.advisor_name && teacher_opts.value.length > 0) {
  const advisorName = raw.advisor_name
```

**修复代码**（CertificateOcr.vue 第449-459行）：

```javascript
// 🔥 修复：正确处理advisors数组（指导老师）
if (raw.advisors && Array.isArray(raw.advisors) && raw.advisors.length > 0 && teacher_opts.value.length > 0) {
  const advisorName = raw.advisors[0]  // ✅ 使用数组的第一个元素
  console.log('🔍 识别到指导老师:', advisorName)
  
  const match = teacher_opts.value.find(t => {
      const name = t.label.split('(')[0].trim()
      const isMatch = advisorName.includes(name) || name.includes(advisorName)
      console.log(`匹配教师 "${name}" vs "${advisorName}":`, isMatch)
      return isMatch
  })
  
  if (match) {
      item.data.teacher_id = match.value
      console.log('✅ 成功匹配指导老师:', match.label)
  } else {
      console.warn('⚠️ 未找到匹配的指导老师:', advisorName)
  }
}
```

---

## 完整修复代码（可直接替换）

**文件**：`frontend/src/components/student/honors/CertificateOcr.vue`

**替换第447-471行**：

```javascript
// 🔥 修复1：处理award字段，添加容错逻辑
if (raw.award) {
  item.data.award = raw.award
} else if (raw.award_level) {
  const levelText = String(raw.award_level)
  const awardKeywords = ['一等奖', '二等奖', '三等奖', '优秀奖', '特等奖', '铜奖', '银奖', '金奖']
  const hasAwardKeyword = awardKeywords.some(keyword => levelText.includes(keyword))
  if (hasAwardKeyword) {
    item.data.award = levelText
  }
}

// 模糊匹配逻辑 - 使用优化后的规则（处理award_level为奖项级别）
if (raw.award_level) {
  let text = String(raw.award_level)
  
  // 1. 定义关键词
  const nationalKeywords = ['全国', '教育部', '国家级', '中国', '中华', '国务院', '中央']
  const provincialKeywords = ['省', '厅', '自治区', '直辖市', '市', '省部'] 
  
  const collegeKeywords = ['系', '分院']

  const isNational = nationalKeywords.some(key => text.includes(key))
  const isProvincial = provincialKeywords.some(key => text.includes(key))

  let identifiedLevel = 'university' // 默认兜底

  // --- 优先级判定逻辑 ---
  if (text.includes('部') && !text.includes('系部') && !text.includes('俱乐部') && !text.includes('省部')) {
     identifiedLevel = 'international'
  }
  else if (isNational) {
     identifiedLevel = 'international'
  }
  else if (isProvincial) {
     identifiedLevel = 'provincial'
  }
  else {
      if (text.includes('大学') && (text.includes('学院') || text.includes('系'))) {
          identifiedLevel = 'college'
      }
      else if (collegeKeywords.some(key => text.includes(key))) {
          identifiedLevel = 'college'
      }
      else {
          if (text.includes('院级')) {
              identifiedLevel = 'college'
          } else if (text.includes('校级') || text.includes('大学') || text.includes('校') || text.includes('学院')) {
              identifiedLevel = 'university'
          } else {
              identifiedLevel = 'university' // 最终兜底
          }
      }
  }
  
  item.data.level = identifiedLevel
}

// 🔥 修复2：正确处理advisors数组（指导老师）
if (raw.advisors && Array.isArray(raw.advisors) && raw.advisors.length > 0 && teacher_opts.value.length > 0) {
  const advisorName = raw.advisors[0]  // 使用数组的第一个元素
  const match = teacher_opts.value.find(t => {
      const name = t.label.split('(')[0].trim()
      return advisorName.includes(name) || name.includes(advisorName)
  })
  if (match) {
      item.data.teacher_id = match.value
  }
}
```

**替换第632-638行**：

```javascript
// 加载当前用户
try {
    const response = await getStudentMe()
    const u = response?.data || response
    
    if (u) {
        current_user_name.value = u.name || u.username || '未知用户'
    } else {
        current_user_name.value = '未知用户'
    }
} catch(e) { 
    console.error('获取用户信息失败', e) 
    current_user_name.value = '未知用户'
}
```

---

## 快速修复步骤

### 步骤1：修复指导教师（最重要，立即见效）

**第450行**，将：
```javascript
if (raw.advisor_name && teacher_opts.value.length > 0) {
```

**改为**：
```javascript
if (raw.advisors && Array.isArray(raw.advisors) && raw.advisors.length > 0 && teacher_opts.value.length > 0) {
```

**第451行**，将：
```javascript
const advisorName = raw.advisor_name
```

**改为**：
```javascript
const advisorName = raw.advisors[0]
```

### 步骤2：修复具体奖项

**在第447行后添加**：
```javascript
if (raw.award) {
  item.data.award = raw.award
} else if (raw.award_level && String(raw.award_level).includes('奖')) {
  item.data.award = raw.award_level  // 容错处理
}
```

### 步骤3：修复参赛学生

**第634-636行**，将：
```javascript
const u = await getStudentMe()
if (u) {
    current_user_name.value = u.username || u.name || '未知用户'
}
```

**改为**：
```javascript
const response = await getStudentMe()
const u = response?.data || response
if (u) {
    current_user_name.value = u.name || u.username || '未知用户'
} else {
    current_user_name.value = '未知用户'
}
```

---

## 测试验证

修复后，使用相同的证书重新上传，应该能正确填充：

- ✅ **参赛学生**：显示当前登录用户的真实姓名（如"张三"）
- ✅ **具体奖项**：显示"优秀奖"
- ✅ **指导教师**：自动选中"潘卫华 (信息技术学院)"

---

## 调试技巧

如果修复后仍有问题，打开浏览器控制台（F12），查看：

1. **Network标签**：
   - 检查`/api/student/me`请求的返回数据
   - 检查`/api/ocr/recognize`的返回数据

2. **Console标签**：
   - 查看`current_user_name`的值
   - 查看teacher_opts数组是否正确加载
   - 查看advisors匹配日志

## 总结

这三个问题都是字段映射不匹配导致的：
1. 参赛学生：API返回数据结构不确定
2. 具体奖项：AI把数据放错字段
3. 指导教师：前端使用错误的字段名

修复后应该能100%解决这些填充问题！🎯
