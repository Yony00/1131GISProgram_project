#!/bin/bash

# 安裝 Python 依賴
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 安裝 Playwright 和瀏覽器
echo "Installing Playwright browsers..."
playwright install --with-deps

# 顯示安裝後的狀況
echo "Playwright browsers installed successfully."
