-- =====================================================
-- 飞书多维表格集成 - 数据库迁移脚本
-- 版本: 001
-- 日期: 2026-02-06
-- 说明: 添加飞书相关表和字段
-- =====================================================

-- 检查数据库
USE student_system;

-- =====================================================
-- 步骤1: 修改现有表 - 添加飞书附件token字段
-- =====================================================

-- 在成果表中添加飞书附件临时token字段（用于失败重试）
ALTER TABLE biz_achievements 
ADD COLUMN feishu_attachment_token VARCHAR(200) DEFAULT NULL 
COMMENT '飞书附件临时token，用于下载失败后的重试机制';

-- =====================================================
-- 步骤2: 创建飞书配置表
-- =====================================================

CREATE TABLE IF NOT EXISTS feishu_configs (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '配置ID',
    app_id VARCHAR(100) NOT NULL COMMENT '飞书应用ID',
    app_secret VARCHAR(500) NOT NULL COMMENT '飞书应用密钥（加密存储）',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态：启用/禁用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='飞书应用配置表';

-- =====================================================
-- 步骤3: 创建字段映射配置表
-- =====================================================

CREATE TABLE IF NOT EXISTS feishu_field_mappings (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '映射ID',
    config_id INT NOT NULL COMMENT '关联的飞书配置ID',
    name VARCHAR(100) NOT NULL COMMENT '映射模板名称',
    feishu_field_name VARCHAR(100) NOT NULL COMMENT '飞书字段名（如：学生姓名）',
    db_field_name VARCHAR(50) NOT NULL COMMENT '数据库字段名（如：student_id）',
    transform_rule JSON DEFAULT NULL COMMENT '转换规则（JSON格式）',
    is_required TINYINT(1) DEFAULT 0 COMMENT '是否必填字段',
    display_order INT DEFAULT 0 COMMENT '显示顺序',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (config_id) REFERENCES feishu_configs(id) ON DELETE CASCADE,
    INDEX idx_config (config_id),
    INDEX idx_display_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='飞书字段映射配置表';

-- =====================================================
-- 步骤4: 创建导入历史日志表
-- =====================================================

CREATE TABLE IF NOT EXISTS feishu_import_logs (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
    operator_id INT NOT NULL COMMENT '操作者ID（sys_users.id）',
    operator_role ENUM('admin', 'student') NOT NULL COMMENT '操作者角色',
    app_token VARCHAR(100) DEFAULT NULL COMMENT '多维表格app_token',
    table_id VARCHAR(100) DEFAULT NULL COMMENT '数据表table_id',
    table_name VARCHAR(200) DEFAULT NULL COMMENT '表格名称',
    total_records INT DEFAULT 0 COMMENT '总记录数',
    success_count INT DEFAULT 0 COMMENT '成功导入数',
    failed_count INT DEFAULT 0 COMMENT '失败数',
    error_details JSON DEFAULT NULL COMMENT '错误详情（JSON数组）',
    import_duration_seconds INT DEFAULT 0 COMMENT '导入耗时（秒）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '导入时间',
    INDEX idx_operator (operator_id, operator_role),
    INDEX idx_created_at (created_at),
    INDEX idx_success_rate ((success_count / NULLIF(total_records, 0)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='飞书导入历史记录表';

-- =====================================================
-- 步骤5: 验证迁移结果
-- =====================================================

-- 显示新创建的表
SHOW TABLES LIKE 'feishu%';

-- 显示成果表的新字段
DESCRIBE biz_achievements;

-- 统计现有数据（确保无损）
SELECT 
    '现有成果数' AS item,
    COUNT(*) AS count
FROM biz_achievements
UNION ALL
SELECT 
    '现有学生数' AS item,
    COUNT(*) AS count
FROM sys_students
UNION ALL
SELECT 
    '现有教师数' AS item,
    COUNT(*) AS count
FROM sys_teachers;

-- =====================================================
-- 迁移完成提示
-- =====================================================

SELECT 
    '✅ 数据库迁移成功完成！' AS status,
    '已创建3个飞书功能表，添加1个可选字段' AS details,
    NOW() AS completed_at;
