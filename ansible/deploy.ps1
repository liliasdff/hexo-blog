# Hexo博客自动部署脚本 - Windows版本
param(
    [string]$ServerIP = "192.168.1.100",
    [string]$Username = "root",
    [string]$RepoUrl = "https://github.com/liliasdf/hexo-blog.git"
)

Write-Host "开始部署Hexo博客..." -ForegroundColor Green

# SSH连接并执行部署命令
$commands = @(
    "cd /var/www/hexo-blog",
    "git pull origin main",
    "npm install",
    "hexo clean",
    "hexo generate",
    "systemctl reload nginx"
)

foreach ($cmd in $commands) {
    Write-Host "执行: $cmd" -ForegroundColor Yellow
    ssh "$Username@$ServerIP" $cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "命令执行失败: $cmd" -ForegroundColor Red
        exit 1
    }
}

Write-Host "博客部署完成！" -ForegroundColor Green