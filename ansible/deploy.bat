@echo off
echo ====================================
echo     Hexo博客自动部署脚本
echo ====================================

set SERVER_IP=192.168.1.100
set USERNAME=root
set BLOG_PATH=/var/www/hexo-blog

echo 正在连接服务器 %SERVER_IP%...
echo 开始部署博客...

ssh %USERNAME%@%SERVER_IP% "cd %BLOG_PATH% && git pull origin main && npm install && hexo clean && hexo generate && systemctl reload nginx"

if %errorlevel% equ 0 (
    echo ====================================
    echo     博客部署成功完成！
    echo     访问地址: http://%SERVER_IP%
    echo ====================================
) else (
    echo ====================================
    echo     部署失败，请检查错误信息
    echo ====================================
)

pause