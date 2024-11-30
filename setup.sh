#!/bin/bash

# 確保 pip 是最新版本
echo "Upgrading pip..."
pip install --upgrade pip

# 安裝 Python 依賴
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 安裝 Playwright 瀏覽器
echo "Installing Playwright browsers..."
playwright install

# 確保 Playwright 安裝完成，測試是否可以成功啟動
echo "Verifying Playwright installation..."
playwright --version
