import pymysql
import sys

# 数据库配置 (根据你的环境默认值)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",  # 如果不是这个密码，请在下方手动修改
    "database": "student_system",
    "charset": "utf8mb4"
}

def fix_database():
    print(f"🔌 正在连接数据库 {DB_CONFIG['database']}...")
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✅ 连接成功！")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("请检查 backend/config.py 中的密码是否正确")
        return

    try:
        # 1. 修复成果表 (核心错误来源)
        print("\n🔧 正在检查 biz_achievements 表...")
        cursor.execute("DESCRIBE biz_achievements")
        columns = [row[0] for row in cursor.fetchall()]
        
        if "feishu_attachment_token" not in columns:
            print("   -> 发现缺少 feishu_attachment_token 字段")
            sql = "ALTER TABLE biz_achievements ADD COLUMN feishu_attachment_token VARCHAR(200) DEFAULT NULL COMMENT '飞书附件临时token'"
            cursor.execute(sql)
            print("   ✅ 字段添加成功！")
        else:
            print("   ✅ 字段已存在，无需添加")

        # 2. 创建飞书相关新表
        print("\n🏗️ 正在创建飞书功能表...")
        
        # feishu_configs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feishu_configs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            app_id VARCHAR(100) NOT NULL,
            app_secret VARCHAR(500) NOT NULL,
            status ENUM('active', 'inactive') DEFAULT 'active',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("   ✅ feishu_configs 表检查完成")

        # feishu_field_mappings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feishu_field_mappings (
            id INT PRIMARY KEY AUTO_INCREMENT,
            config_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            feishu_field_name VARCHAR(100) NOT NULL,
            db_field_name VARCHAR(50) NOT NULL,
            transform_rule JSON,
            is_required TINYINT(1) DEFAULT 0,
            display_order INT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (config_id) REFERENCES feishu_configs(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("   ✅ feishu_field_mappings 表检查完成")

        # feishu_import_logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feishu_import_logs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            operator_id INT NOT NULL,
            operator_role ENUM('admin', 'student') NOT NULL,
            app_token VARCHAR(100),
            table_id VARCHAR(100),
            table_name VARCHAR(200),
            total_records INT DEFAULT 0,
            success_count INT DEFAULT 0,
            failed_count INT DEFAULT 0,
            error_details JSON,
            import_duration_seconds INT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("   ✅ feishu_import_logs 表检查完成")

        conn.commit()
        print("\n🎉 所有数据库修复已完成！")

    except Exception as e:
        print(f"\n❌ 执行出错: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()
