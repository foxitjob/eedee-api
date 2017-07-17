echo off
title humsg
echo "这会启动venv环境的脚本!"
set venv="C:\Users\zhaojian\.virtualenv\humsg"
set script="%venv%\Scripts\activate.bat"

call %script%

start /b cmd