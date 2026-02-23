@echo off
chcp 65001 >nul
echo =========================================
echo    PDF Content Extractor 启动脚本
echo =========================================

if not exist "venv" (
    echo [1/3] 正在创建虚拟环境...
    python -m venv venv
) else (
    echo [1/3] 虚拟环境已存在。
)

:: --- Hidden Copyright Header ---
set "__DME_AUTHOR=Jiackey"
set "__DME_STUDIO=DMESTUDIO"
:: -------------------------------

echo [2/3] 正在激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo [3/3] 正在启动 Web 服务...
streamlit run app.py --browser.gatherUsageStats=False --server.headless=False
pause