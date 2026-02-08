# Execute Database Migration
# 执行数据库迁移，添加飞书所需的字段和表

Write-Host "开始执行数据库迁移..." -ForegroundColor Green

# 1. 设置数据库连接配置
$DB_USER = "root"
$DB_PASS = "123456" # 根据你的配置，通常是这个或空
$DB_NAME = "student_system"
$MIGRATION_FILE = "backend/migrations/001_add_feishu_tables.sql"

# 2. 检查mysql命令是否可用
if (-not (Get-Command "mysql" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未找到mysql命令，请确保MySQL已安装并添加到PATH环境变量" -ForegroundColor Red
    Write-Host "或者尝试手动执行：" -ForegroundColor Yellow
    Write-Host "打开MySQL Workbench -> 选择student_system数据库 -> 运行 $MIGRATION_FILE"
    exit 1
}

# 3. 执行迁移
Write-Host "正在执行SQL脚本: $MIGRATION_FILE" -ForegroundColor Cyan
Get-Content $MIGRATION_FILE | mysql -u $DB_USER -p$DB_PASS $DB_NAME

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 数据库迁移执行成功！" -ForegroundColor Green
    Write-Host "字段 feishu_attachment_token 已添加到表 biz_achievements"
}
else {
    Write-Host "❌ 迁移执行失败" -ForegroundColor Red
    Write-Host "请检查数据库密码是否正确，或者尝试手动执行"
}
