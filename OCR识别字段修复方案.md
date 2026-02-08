# OCR识别字段修复方案

## 问题分析

根据用户反馈和代码检查，发现以下问题：

### 1. 具体奖项（award字段）未识别
**问题**：前端显示"如：一等奖"的placeholder，说明`award`字段为空

**原因**：
- 后端OCR prompt中缺少明确的`award`字段定义
- 只有`award_level`字段，但这个字段被用于识别"奖项等级"（如一等奖、二等奖）
- 应该区分两个字段：
  - `award`: 具体奖项（如"一等奖"、"二等奖"、"优秀奖"）
  - `award_level`: 奖项级别（如"国家级"、"省部级"、"校级"）

### 2. 指导老师（advisors字段）未识别
**问题**：前端显示"搜索导师姓名"的placeholder，说明`teacher_id`未填充

**原因**：
- 后端返回`advisors`字段是数组：`["老师1", "老师2"]`
- 前端代码错误地使用了`raw.advisor_name`（单个名字，不存在）
- 应该使用`raw.advisors[0]`来获取第一个指导老师

### 3. 参赛学生识别支持不足
**问题**：虽然后端返回了`team_members`字段，但前端没有充分利用

**改进方案**：
- 后端返回的`team_members`数组包含所有参赛学生
- 可以在`additional_info`中显示完整的团队成员信息
- 或者提示用户核对当前学生是否在团队名单中

## 修复方案

### 方案1：后端Prompt修改（推荐）

修改文件：`backend/services/certificate_recognition_openai.py` (行56-121)

**修改prompt，明确区分两个字段**：

```python
**奖项详情（重要！请仔细区分这两个字段）：**
6. **具体奖项**（award）：识别证书上明确写的"一等奖"、"二等奖"、"三等奖"、"优秀奖"、"特等奖"等
   - 示例："一等奖"、"二等奖"、"优秀奖"、"铜奖"
   
7. **奖项级别**（award_level）：识别或推断"国家级"、"省部级"、"校级"、"院级"等行政级别
   - 从颁发单位推断：如"教育部"→国家级，"XX省XX厅"→省部级，"XX大学"→校级
   - 示例："国家级"、"省部级"、"校级"、"院级"
```

**JSON返回格式**：

```json
{
    "cert

ificate_name": "证书名称",
    "award": "一等奖",  // 🔥 新增：具体奖项
    "award_level": "校级",  // 奖项级别
    "team_members": ["学生1", "学生2"],  // 🔥 参赛学生
    "advisors": ["老师1", "老师2"]  // 🔥 指导老师
}
```

### 方案2：后端API修改（已完成✅）

修改文件：`backend/routers/student.py` (行54-76)

**已添加award字段映射**：

```python
"recognized_data": {
    "award_level": data.get("award_level"),  # 奖项级别（国家级、省部级等）
    "award": data.get("award"),  # ✅ 具体奖项（一等奖、二等奖等）
    ...
}
```

### 方案3：前端数据处理修改（需要修改）

修改文件：`frontend/src/components/student/honors/CertificateOcr.vue` (行377-487)

**需要修改的地方**：

#### 修改1：处理award字段
```javascript
// 当前代码（行447）：
if (raw.award) item.data.award = raw.award

// ✅ 正确，不需要修改
```

#### 修改2：修复advisors处理（重要！）
```javascript
// ❌ 错误代码（行450-459）：
if (raw.advisor_name && teacher_opts.value.length > 0) {
  const advisorName = raw.advisor_name  // ❌ 字段名错误
  ...
}

// ✅ 应该改为：
if (raw.advisors && Array.isArray(raw.advisors) && raw.advisors.length > 0 && teacher_opts.value.length > 0) {
  const advisorName = raw.advisors[0]  // ✅ 使用数组的第一个元素
  const match = teacher_opts.value.find(t => {
      const name = t.label.split('(')[0].trim()
      return advisorName.includes(name) || name.includes(advisorName)
  })
  if (match) {
      item.data.teacher_id = match.value
  }
}
```

#### 修改3：处理参赛学生（可选增强）
```javascript
// 在行460后添加：
// 处理参赛学生（team_members）
if (raw.team_members && Array.isArray(raw.team_members) && raw.team_members.length > 0) {
  // 显示完整的团队成员信息
  if (!item.data.additional_info) {
    item.data.additional_info = ''
  }
  item.data.additional_info += `\n团队成员：${raw.team_members.join('、')}`
}
```

## 具体修改步骤

### 步骤1：修改前端CertificateOcr.vue

找到 `process_ocr` 函数中的第450-459行：

```javascript
// 尝试匹配导师
if (raw.advisor_name && teacher_opts.value.length > 0) {
  const advisorName = raw.advisor_name
```

**替换为**：

```javascript
// 🔥 修复：正确处理advisors数组（指导老师）
if (raw.advisors && Array.isArray(raw.advisors) && raw.advisors.length > 0 && teacher_opts.value.length > 0) {
  const advisorName = raw.advisors[0]
```

### 步骤2：修改后端OCR Prompt

由于文件编辑工具暂时无法修改，请手动编辑 `backend/services/certificate_recognition_openai.py`：

在行75-76的"**奖项详情：**"部分，修改为：

```python
**奖项详情（重要！请仔细区分这两个字段）：**
6. **具体奖项**（award）：识别证书上明确写的"一等奖"、"二等奖"、"三等奖"、"优秀奖"、"特等奖"等
   - 在证书上通常标注为："获得XX奖"、"荣获XX"
   - 示例："一等奖"、"二等奖"、"优秀奖"、"特等奖"
   
7. **奖项级别**（award_level）：识别或推断"国家级"、"省部级"、"校级"、"院级"等行政级别
   - 从颁发单位推断：如"教育部"→国家级，"XX省XX厅"→省部级，"XX大学"→校级
   - 或从证书描述推断：如"全国大学生XX"→国家级
   - 示例："国家级"、"省部级"、"校级"、"院级"
```

并在JSON返回格式（行99-115）中确保有：

```json
{
    "award": "具体奖项（如：一等奖、二等奖、三等奖、优秀奖等）",
    "award_level": "奖项级别（如：国家级、省部级、校级、院级等）",
    "team_members": ["参赛学生1", "参赛学生2", "参赛学生3"],
    "advisors": ["指导老师1", "指导老师2"],
}
```

## 测试验证

修改完成后，请进行以下测试：

1. **上传一张证书**
2. **检查OCR识别结果**：
   - ✅ "具体奖项"字段应显示"一等奖"、"二等奖"等
   - ✅ "奖项等级"字段应显示"国家级"、"省部级"等
   - ✅ "指导教师"下拉框应自动选中匹配的老师
   - ✅ "参赛学生"应显示当前登录学生的用户名

## 常见问题

### Q1：为什么要区分award和award_level？
**A**：这是两个不同的概念：
- `award`: "一等奖"、"二等奖" - 具体的奖项名称
- `award_level`: "国家级"、"省部级" - 奖项的行政级别

### Q2：如果OCR模型返回的数据格式不对怎么办？
**A**：需要在后端的`validate_recognition_result`函数中添加容错逻辑，确保：
- 如果`award`字段为空，尝试从`award_level`中提取"X等奖"关键词
- 如果`advisors`是字符串而不是数组，转换为数组

### Q3：参赛学生姓名会覆盖当前登录学生吗？
**A**：不会。当前代码设计中：
- `student_name`字段自动填充为当前登录学生
- `team_members`数组保存所有参赛学生
- 可以在`additional_info`中显示完整团队信息

## 总结

修复的核心问题：
1. ✅ 后端API已添加`award`字段映射
2. ❌ **前端处理advisors字段错误** - 需要从`advisor_name`改为`advisors[0]`
3. ⚠️ 后端Prompt需要明确区分`award`和`award_level`两个字段
4. ✅ 参赛学生信息可以通过`team_members`字段获取

**立即需要修改**：
- 前端`CertificateOcr.vue`第450行的`raw.advisor_name`改为`raw.advisors`
