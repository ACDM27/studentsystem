# consulting.vue 第484行错误修复

## 错误位置
**文件**: `frontend/src/components/student/consulting/consulting.vue`  
**行号**: 484

## 错误代码
```typescript
const response = await getConsultTeacherById({ id: consultantId })
```

## 错误原因
`getConsultTeacherById` 函数的参数类型不匹配：

**函数定义** (api/index.ts 第311行):
```typescript
export function getConsultTeacherById(id: ID): Promise<any> {
    return request.get(`/api/v1/consulting/teachers/${id}`)
}
```

**当前调用** (错误):
```typescript
await getConsultTeacherById({ id: consultantId })  // ❌ 传入了对象
```

函数期望接收一个 `ID` 类型的参数，但实际传入了一个对象 `{ id: consultantId }`

## 修复方案

**将第484行改为**:
```typescript
const response = await getConsultTeacherById(consultantId)  // ✅ 直接传入ID
```

## 完整的修复代码

**替换 consulting.vue 第481-493行**:

```typescript
// 方法
const viewDetails = async (consultantId: string | number) => {
  try {
    const response = await getConsultTeacherById(consultantId)  // ✅ 修复：直接传入ID
    if (response && response.data) {
      console.log('咨询师详情:', response.data)
      // 实现跳转到详情页的逻辑
      // router.push(`/student/consultant/${consultantId}`)
    }
  } catch (error) {
    console.error('获取咨询师详情失败:', error)
  }
}
```

## 对比

| 项目 | 错误代码 | 正确代码 |
|------|---------|---------|
| 参数类型 | `{ id: consultantId }` (对象) | `consultantId` (ID值) |
| 运行结果 | ❌ TypeScript类型错误 / 404错误 | ✅ 正常工作 |

## 测试验证

修复后，点击咨询师卡片的"详情"按钮应该能正常调用API获取详情数据。

## 类似的潜在问题

检查其他API调用是否也有类似问题，确保参数传递正确。

---

**立即修复步骤**:
1. 打开 `frontend/src/components/student/consulting/consulting.vue`
2. 找到第484行 `const response = await getConsultTeacherById({ id: consultantId })`
3. 将 `{ id: consultantId }` 改为 `consultantId`
4. 保存文件

修复后TypeScript错误应该消失！✅
