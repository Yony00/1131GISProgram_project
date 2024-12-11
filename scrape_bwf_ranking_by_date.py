# scrape_bwf_ranking_by_date.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_bwf_ranking_by_date(selected_id):
    # 使用選擇的日期 ID 設定對應的 URL
    url = f"https://bwf.tournamentsoftware.com/ranking/category.aspx?id={selected_id}&category=472&C472FOC=&p=1&ps=100"

    # 設置 User-Agent 防止被封鎖
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 發送請求並解析 HTML
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找表格，這是存放選手排名的地方
    table = soup.find('table', {'class': 'ruler'})

    if not table:
        print("Error: No table found")
        return None

    # 提取表格中的行
    rows = table.find_all('tr')[1:]  # 跳過表頭
    data = []
    
    for row in rows:
        cols = row.find_all('td')
        
        # 確保每行包含足夠的列數（根據需要提取的欄位數量）
        if len(cols) >= 8:  # 假設表格至少有8列數據
            rank = cols[0].text.strip()
            player = cols[4].text.strip()
            player = player[5:]  # 去除多餘的空白或特殊字元
            country = cols[10].text.strip()
            points = cols[7].text.strip()
            confederation = cols[9].text.strip()  # 新增 Confederation 欄位
            
            # 每一行的資料
            data.append([rank, player, country, points, confederation])

    # 設定欄位名稱
    columns = ["Rank", "Player", "Country", "Points", "Confederation"]
    df = pd.DataFrame(data, columns=columns)
    
    return df

def WSscrape_bwf_ranking_by_date(selected_id):
    # 使用選擇的日期 ID 設定對應的 URL
    url = f"https://bwf.tournamentsoftware.com/ranking/category.aspx?id={selected_id}&category=473&C473FOC=&p=1&ps=100"

    # 設置 User-Agent 防止被封鎖
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 發送請求並解析 HTML
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找表格，這是存放選手排名的地方
    table = soup.find('table', {'class': 'ruler'})

    if not table:
        print("Error: No table found")
        return None

    # 提取表格中的行
    rows = table.find_all('tr')[1:]  # 跳過表頭
    data = []
    
    for row in rows:
        cols = row.find_all('td')
        
        # 確保每行包含足夠的列數（根據需要提取的欄位數量）
        if len(cols) >= 8:  # 假設表格至少有8列數據
            rank = cols[0].text.strip()
            player = cols[4].text.strip()
            player = player[5:]  # 去除多餘的空白或特殊字元
            country = cols[10].text.strip()
            points = cols[7].text.strip()
            confederation = cols[9].text.strip()  # 新增 Confederation 欄位
            
            # 每一行的資料
            data.append([rank, player, country, points, confederation])

    # 設定欄位名稱
    columns = ["Rank", "Player", "Country", "Points", "Confederation"]
    df = pd.DataFrame(data, columns=columns)
    
    return df


def MDscrape_bwf_ranking_by_date(selected_id):
    # 使用選擇的日期 ID 設定對應的 URL
    url = f"https://bwf.tournamentsoftware.com/ranking/category.aspx?id={selected_id}&category=474&C474FOC=&p=1&ps=100"

    # 設置 User-Agent 防止被封鎖
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 發送請求並解析 HTML
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找表格，這是存放選手排名的地方
    table = soup.find('table', {'class': 'ruler'})

    if not table:
        print("Error: No table found")
        return None

    # 提取表格中的行
    rows = table.find_all('tr')[1:]  # 跳過表頭
    data = []
    
    for row in rows:
        cols = row.find_all('td')
        
        # 確保每行包含足夠的列數（根據需要提取的欄位數量）
        if len(cols) >= 8:  # 假設表格至少有8列數據
            rank = cols[0].text.strip()
            player = cols[4].text.strip()
            player = player[5:]  # 去除多餘的空白或特殊字元
            country = cols[10].text.strip()
            points = cols[7].text.strip()
            confederation = cols[9].text.strip()  # 新增 Confederation 欄位
            
            # 每一行的資料
            data.append([rank, player, country, points, confederation])

    # 設定欄位名稱
    columns = ["Rank", "Player", "Country", "Points", "Confederation"]
    df = pd.DataFrame(data, columns=columns)
    
    return df
    
def WDscrape_bwf_ranking_by_date(selected_id):
    # 使用選擇的日期 ID 設定對應的 URL
    url = f"https://bwf.tournamentsoftware.com/ranking/category.aspx?id={selected_id}category=475&C475FOC=&p=1&ps=100"

    # 設置 User-Agent 防止被封鎖
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 發送請求並解析 HTML
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找表格，這是存放選手排名的地方
    table = soup.find('table', {'class': 'ruler'})

    if not table:
        print("Error: No table found")
        return None

    # 提取表格中的行
    rows = table.find_all('tr')[1:]  # 跳過表頭
    data = []
    
    for row in rows:
        cols = row.find_all('td')
        
        # 確保每行包含足夠的列數（根據需要提取的欄位數量）
        if len(cols) >= 8:  # 假設表格至少有8列數據
            rank = cols[0].text.strip()
            player = cols[4].text.strip()
            player = player[5:]  # 去除多餘的空白或特殊字元
            country = cols[10].text.strip()
            points = cols[7].text.strip()
            confederation = cols[9].text.strip()  # 新增 Confederation 欄位
            
            # 每一行的資料
            data.append([rank, player, country, points, confederation])

    # 設定欄位名稱
    columns = ["Rank", "Player", "Country", "Points", "Confederation"]
    df = pd.DataFrame(data, columns=columns)
    
    return df


def MXDscrape_bwf_ranking_by_date(selected_id):
    # 使用選擇的日期 ID 設定對應的 URL
    url = f"https://bwf.tournamentsoftware.com/ranking/category.aspx?id={selected_id}&category=476&C476FOC=&p=1&ps=100"

    # 設置 User-Agent 防止被封鎖
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 發送請求並解析 HTML
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找表格，這是存放選手排名的地方
    table = soup.find('table', {'class': 'ruler'})

    if not table:
        print("Error: No table found")
        return None

    # 提取表格中的行
    rows = table.find_all('tr')[1:]  # 跳過表頭
    data = []
    
    for row in rows:
        cols = row.find_all('td')
        
        # 確保每行包含足夠的列數（根據需要提取的欄位數量）
        if len(cols) >= 8:  # 假設表格至少有8列數據
            rank = cols[0].text.strip()
            player = cols[4].text.strip()
            player = player[5:]  # 去除多餘的空白或特殊字元
            country = cols[10].text.strip()
            points = cols[7].text.strip()
            confederation = cols[9].text.strip()  # 新增 Confederation 欄位
            
            # 每一行的資料
            data.append([rank, player, country, points, confederation])

    # 設定欄位名稱
    columns = ["Rank", "Player", "Country", "Points", "Confederation"]
    df = pd.DataFrame(data, columns=columns)
    
    return df
