#!/bin/bash

# 安装 Python 依赖
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 安装 Playwright 浏览器
echo "Installing Playwright browsers..."
playwright install
