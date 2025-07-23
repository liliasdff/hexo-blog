@echo off
echo ================================
echo     Hexo博客一键发布脚本
echo ================================

echo [1/4] 清理缓存...
call hexo clean

echo [2/4] 本地生成静态文件...
call hexo generate

echo [3/4] 启动本地预览服务器（可选）
set /p preview="是否要本地预览？(y/n): "
if /i "%preview%"=="y" (
    echo 启动本地服务器: http://localhost:4000
    echo 按 Ctrl+C 停止预览，然后继续发布
    call hexo server
)

echo [4/4] 推送到GitHub...
git add .

set /p commit_msg="请输入提交信息: "
if "%commit_msg%"=="" set commit_msg=Update blog content

git commit -m "%commit_msg%"
git push origin main

echo ================================
echo   发布完成！请等待1-2分钟
echo   访问: https://liliasdff.github.io/hexo-blog/
echo ================================

pause