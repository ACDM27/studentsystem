# OCR字段未填充问题修复方案

## 问题现状

根据实际OCR返回数据：
```json
{
    "award_level": "优秀奖",    // ❌ AI把具体奖项放这里了
    "award": null,              // ❌ 应该在这里
    "advisors": ["潘卫华"],     // ✅ 数据正确
    "team_members": ["吴东泽", "潘思翰", "朱锋", "李奕锋", "覃浩源"]  // ✅ 数据正确
}
```

前端代码问题：
```javascript
// 第447行：award字段处理正确，但OCR返回的award为null
if (raw.award) item.data.award = raw.award  // ✅ 代码正确，但数据为null

// 第450行：错误的字段名！
if (raw.advisor_name && ...) {  // ❌ 应该是 raw.advisors
    const advisorName = raw.advisor_name  // ❌ 字段不存在
```

## 修复方案

### 方案1：前端容错处理（立即生效，推荐）

**文件**：`frontend/src/components/student/honors/CertificateOcr.vue`

**位置1**：第447行附近，增加容错逻辑

```javascript
// === 修复1：处理award字段，添加容错 ===
// 优先使用award字段，如果为空则尝试从award_level提取
if (raw.award) {
  item.data.award = raw.award
} else if (raw.award_level) {
  // 容错：如果award_level包含"奖"字，可能是AI误放，也填充到award
  const levelText = String(raw.award_level)
  if (levelText.includes('奖')) {
    item.data.award = levelText  // 将"优秀奖"等填充到award
  }
}
```

**位置2**：第450-459行，修复advisors字段处理

```javascript
// === 修复2：正确处理advisors数组 ===
// 🔥 修复：从 raw.advisor_name 改为 raw.advisors
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

**位置3**：第460行后，增加team_members显示

```javascript
// === 修复3：更好地展示参赛学生信息 ===
if (raw.team_members && Array.isArray(raw.team_members) && raw.team_members.length > 0) {
  // 在additional_info中显示完整团队信息
  const teamInfo = `团队成员：${raw.team_members.join('、')}`
  if (item.data.additional_info) {
    item.data.additional_info += `\n${teamInfo}`
  } else {
    item.data.additional_info = teamInfo
  }
}
```

### 方案2：后端Prompt修复（根本解决）

**文件**：`backend/services/certificate_recognition_openai.py`

**位置**：第75-78行，修改说明

**当前（错误）**：
```python
**奖项详情：**
6. 奖项等级（如：一等奖、二等奖、三等奖、优秀奖等）
7. 获奖类别/竞赛类型...
```

**应改为（正确）**：
```python
**奖项详情（请仔细区分）：**
6. **具体奖项**（award字段）：识别证书上写的"一等奖"、"二等奖"、"三等奖"、"优秀奖"等
   - 这是证书上明确标注的奖项名称
   - 示例："一等奖"、"二等奖"、"优秀奖"、"特等奖"、"铜奖"
   
7. **奖项级别**（award_level字段）：识别或推断"国家级"、"省部级"、"校级"、"院级"
   - 从颁发单位推断：如"教育部"→国家级，"XX省"→省部级，"XX大学"→校级
   - 示例："国家级"、"省部级"、"校级"、"院级"
   
8. 获奖类别/竞赛类型...
```

**位置**：第99-115行，修改JSON格式

**当前（缺少award）**：
```json
{
    "award_level": "奖项等级",
    ...
}
```

**应改为（增加award）**：
```json
{
    "certificate_name": "证书名称",
    "award": "具体奖项（如：一等奖、二等奖、优秀奖等）",
    "award_level": "奖项级别（如：国家级、省部级、校级等）",
    "team_members": ["参赛学生1", "参赛学生2"],
    "advisors": ["指导老师1", "指导老师2"],
    ...
}
```

## 完整的修复代码（前端）

**替换 CertificateOcr.vue 第447-470行**：

```javascript
      // 🔥 修复1：处理award字段，添加容错逻辑
      if (raw.award) {
        item.data.award = raw.award
      } else if (raw.award_level) {
        // 容错：如果award_level包含"奖"字，可能是AI误放
        const levelText = String(raw.award_level)
        if (levelText.includes('奖')) {
          item.data.award = levelText
        }
      }
      
      // 模糊匹配逻辑 - 使用优化后的规则（处理award_level为奖项级别）
      if (raw.award_level) {
        let text = String(raw.award_level)
        
        // 1. 定义关键词
        const nationalKeywords = ['全国', '教育部', '国家级', '中国', '中华', '国务院', '中央']
        const provincialKeywords = ['省', '厅', '自治区', '直辖市', '市', '省部'] 
        
        const collegeKeywords = [' 系', '分院']

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

      // 🔥 修复3：处理参赛学生（team_members）
      if (raw.team_members && Array.isArray(raw.team_members) && raw.team_members.length > 0) {
        const teamInfo = `团队成员：${raw.team_members.join('、')}`
        if (item.data.additional_info) {
          item.data.additional_info += `\n${teamInfo}`
        } else {
          item.data.additional_info = teamInfo
        }
      }

      if (raw.suggested_type) {
        const found = category_opts.find(c => c.value === raw.suggested_type)
        if (found) item.data.category = raw.suggested_type
      }

      // 提取并保存补充信息（用于管理端详尽展示）
      if (raw.issuer) item.data.issuer = raw.issuer
      if (raw.certificate_number) item.data.certificate_number = raw.certificate_number
      if (raw.project_name) item.data.project_name = raw.project_name
      if (raw.team_members) item.data.team_members = raw.team_members
      if (raw.additional_info) item.data.additional_info = (item.data.additional_info || '') + '\n' + raw.additional_info
```

## 测试验证

修复后，对于您的证书数据：
```json
{
    "award_level": "优秀奖",
    "advisors": ["潘卫华"],
    "team_members": ["吴东泽", "潘思翰", "朱锋", "李奕锋", "覃浩源"]
}
```

应该能正确填充：
- ✅ **具体奖项**：显示"优秀奖"（从award_level容错获取）
- ✅ **指导教师**：自动选中"潘卫华"（修复advisors处理）
- ✅ **参赛学生**：在补充信息中显示"团队成员：吴东泽、潘思翰、朱锋、李奕锋、覃浩源"

## 立即执行的修复步骤

请手动修改 `frontend/src/components/student/honors/CertificateOcr.vue`：

**第450行**，将：
```javascript
if (raw.advisor_name && teacher_opts.value.length > 0) {
  const advisorName = raw.advisor_name
```

**改为**：
```javascript
if (raw.advisors && Array.isArray(raw.advisors) && raw.advisors.length > 0 && teacher_opts.value.length > 0) {
  const advisorName = raw.advisors[0]
```

这是最关键的修复！改完后刷新浏览器，指导老师就能正确填充了。✅
