# Achievement 枚举值对照表

## 后端验证规则

根据后端返回的错误信息，以下是 Achievement 模型支持的枚举值：

### 1. category (成果类型) - 必填
```
允许的值：
- competition    (竞赛类)
- patent         (专利类)
- paper          (论文类)
- project        (项目类)
- certificate    (证书类)
- other          (其他)
```

### 2. level (成果级别) - 必填
```
允许的值：
- international  (国际级)
- national       (国家级)
- provincial     (省级)
- university     (校级)
- college        (院级)
- other          (其他)
```

### 3. award (奖项等级) - 可选
```
允许的值：
- grandprize         (特等奖)
- firstprize         (一等奖)
- secondprize        (二等奖)
- thirdprize         (三等奖)
- honorablemention   (优秀奖)
- other              (其他)
- ""                 (空字符串，表示未设置)
```

## 前端表单选项

### 成果类型下拉框
```vue
<el-option label="竞赛类" value="competition" />
<el-option label="专利类" value="patent" />
<el-option label="论文类" value="paper" />
<el-option label="项目类" value="project" />
<el-option label="证书类" value="certificate" />
<el-option label="其他" value="other" />
```

### 成果级别下拉框
```vue
<el-option label="国际级" value="international" />
<el-option label="国家级" value="national" />
<el-option label="省级" value="provincial" />
<el-option label="校级" value="university" />
<el-option label="院级" value="college" />
<el-option label="其他" value="other" />
```

### 奖项等级下拉框（可清空）
```vue
<el-option label="特等奖" value="grandprize" />
<el-option label="一等奖" value="firstprize" />
<el-option label="二等奖" value="secondprize" />
<el-option label="三等奖" value="thirdprize" />
<el-option label="优秀奖" value="honorablemention" />
<el-option label="其他" value="other" />
```

## OCR识别映射规则

### 奖项等级识别
```javascript
if (/特等|grand|特/.test(prizeStr)) {
  extractedInfo.prize = 'grandprize'
} else if (/一等|first|1st/.test(prizeStr)) {
  extractedInfo.prize = 'firstprize'
} else if (/二等|second|2nd/.test(prizeStr)) {
  extractedInfo.prize = 'secondprize'
} else if (/三等|third|3rd/.test(prizeStr)) {
  extractedInfo.prize = 'thirdprize'
} else if (/优秀|honorable|excellence/.test(prizeStr)) {
  extractedInfo.prize = 'honorablemention'
}
```

### 成果级别识别
```javascript
if (/国际|世界/.test(s)) return 'international'
if (/全国|国家|中国/.test(s)) return 'national'
if (/省|市/.test(s)) return 'provincial'
if (/院/.test(s)) return 'college'
return 'university' // 默认校级
```

### 成果类型识别
```javascript
if (/竞赛|比赛|contest|competition/.test(typeStr)) {
  extractedInfo.type = 'competition'
} else if (/专利|patent/.test(typeStr)) {
  extractedInfo.type = 'patent'
} else if (/论文|paper/.test(typeStr)) {
  extractedInfo.type = 'paper'
} else if (/项目|project/.test(typeStr)) {
  extractedInfo.type = 'project'
} else if (/证书|certificate/.test(typeStr)) {
  extractedInfo.type = 'certificate'
} else {
  extractedInfo.type = 'competition' // 默认竞赛类
}
```

## 常见错误

### ❌ 错误示例
```json
{
  "award": "excellence"  // 后端不支持此值
}
```

### ✅ 正确示例
```json
{
  "award": "honorablemention"  // 使用正确的枚举值
}
```

或者

```json
{
  "award": ""  // 空字符串表示未设置
}
```

## 提交数据示例

### 完整示例
```json
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
```

### 最小示例（仅必填字段）
```json
{
  "data": {
    "title": "某某证书",
    "name": "张三",
    "date": "2024-01-01",
    "category": "certificate",
    "level": "university",
    "tutor_name": "",
    "award": "",
    "issuer": "",
    "notes": ""
  }
}
```

## 验证规则总结

| 字段 | 是否必填 | 类型 | 验证规则 |
|------|---------|------|---------|
| title | ✅ 必填 | string | 非空字符串 |
| name | ✅ 必填 | string | 非空字符串 |
| date | ✅ 必填 | string | YYYY-MM-DD 格式 |
| category | ✅ 必填 | enum | 必须是允许的枚举值之一 |
| level | ✅ 必填 | enum | 必须是允许的枚举值之一 |
| award | ❌ 可选 | enum | 必须是允许的枚举值之一或空字符串 |
| tutor_name | ❌ 可选 | string | 任意字符串 |
| issuer | ❌ 可选 | string | 任意字符串 |
| notes | ❌ 可选 | string | 任意字符串 |
| student | ❌ 可选 | number | 学生ID（关联） |
| student_id | ❌ 可选 | string | 学生ID（字符串） |
