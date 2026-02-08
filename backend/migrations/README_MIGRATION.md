# 飞书集成功能 - 数据库迁移指南

## ⚠️ 重要提示

在执行数据库迁移前，请务必先备份数据库！

## 步骤1：备份当前数据库

```powershell
# Windows PowerShell 执行
mysqldump -u root -p student_system > backup_before_feishu_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql
```

## 步骤2：执行迁移脚本

```powershell
# 方法1：使用MySQL命令行
mysql -u root -p student_system < migrations/001_add_feishu_tables.sql

# 方法2：直接在MySQL客户端中执行
# 打开MySQL Workbench或其他客户端
# 打开文件：backend/migrations/001_add_feishu_tables.sql
# 执行整个脚本
```

## 步骤3：验证迁移结果

```sql
-- 检查新表是否创建成功
SHOW TABLES LIKE 'feishu%';

-- 应该看到3个新表：
-- feishu_configs
-- feishu_field_mappings
-- feishu_import_logs

-- 检查成果表的新字段
DESCRIBE biz_achievements;

-- 应该看到新增字段：feishu_attachment_token
```

## 步骤4：验证现有数据完整性

```sql
-- 确认现有数据没有丢失
SELECT COUNT(*) FROM biz_achievements;
SELECT COUNT(*) FROM sys_students;
SELECT COUNT(*) FROM sys_teachers;
```

## 迁移内容说明

### 新增表（3个）
1. **feishu_configs** - 存储飞书应用配置
2. **feishu_field_mappings** - 存储字段映射规则
3. **feishu_import_logs** - 记录导入历史

### 修改表（1个）
- **biz_achievements** - 添加字段 `feishu_attachment_token`（可选字段，不影响现有数据）

## 回滚方案

如果需要回滚迁移：

```sql
-- 删除飞书功能相关表
DROP TABLE IF EXISTS feishu_import_logs;
DROP TABLE IF EXISTS feishu_field_mappings;
DROP TABLE IF EXISTS feishu_configs;

-- 删除添加的字段
ALTER TABLE biz_achievements DROP COLUMN feishu_attachment_token;
```

## 下一步

迁移成功后，可以：
1. 启动后端服务
2. 在管理端配置飞书应用凭证
3. 开始使用飞书导入功能

---

**创建时间**: 2026-02-06
**版本**: 001
