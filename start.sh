#!/bin/bash
echo "========================================="
echo "   PDF Content Extractor 启动脚本"
echo "========================================="

if [ ! -d "venv" ]; then
    echo "[1/3] 正在创建虚拟环境..."
    python3 -m venv venv
else
    echo "[1/3] 虚拟环境已存在。"
fi

# --- Hidden Copyright Header ---
__DME_AUTHOR="Jiackey"
__DME_STUDIO="DMESTUDIO"
# -------------------------------

echo "[2/3] 正在激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install -r requirements.txt

echo "[3/3] 正在启动 Web 服务..."
streamlit run app.py --browser.gatherUsageStats=False --server.headless=False
