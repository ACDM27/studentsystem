# Fix UTF-8 Encoding for All Python Files
# 修复所有Python文件的UTF-8编码问题

Write-Host "开始修复Python文件编码..." -ForegroundColor Green

# 修复所有飞书相关的Python文件
$files = @(
    "backend/models.py",
    "backend/config.py", 
    "backend/schemas_feishu.py",
    "backend/routers/feishu.py",
    "backend/services/feishu/feishu_client.py",
    "backend/services/feishu/data_mapper.py",
    "backend/services/feishu/attachment_downloader.py",
    "backend/main.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "处理: $file" -ForegroundColor Yellow
        
        # 读取并重新保存为UTF-8
        $content = Get-Content $file -Encoding UTF8 -Raw
        [System.IO.File]::WriteAllText((Resolve-Path $file), $content, [System.Text.UTF8Encoding]::new($false))
        
        Write-Host "✓ 完成: $file" -ForegroundColor Green
    }
    else {
        Write-Host "✗ 文件不存在: $file" -ForegroundColor Red
    }
}

Write-Host "`n所有文件编码已修复为UTF-8（无BOM）" -ForegroundColor Green
Write-Host "现在可以重启后端服务了" -ForegroundColor Cyan
