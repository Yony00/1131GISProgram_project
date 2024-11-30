# scrape_bwf_ranking.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_bwf_ranking_initial(url):
    # 發送請求並解析 HTML
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果請求失敗，會觸發錯誤
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None, {}

    # 打印頁面內容以確保我們獲取了正確的頁面
    print("Page content successfully fetched.")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找表格，這是存放選手排名的地方
    table = soup.find('table', {'class': 'ruler'})
    
    if not table:
        print("Error: No table found")
        return None, {}

    # 提取表格中的行
    rows = table.find_all('tr')[1:]  # 跳過表頭
    data = []

    # 解析網頁中的 ID-日期對應的選項
    date_id_dict = {}
    select = soup.find('select', {'id': 'cphPage_cphPage_cphPage_dlPublication'})
    if select:
        options = select.find_all('option')
        for option in options:
            date = option.text.strip()
            date_id_dict[date] = option['value']
    
    # 如果未找到日期- ID對應的選項
    if not date_id_dict:
        print("Error: No date-id mappings found.")
        return None, {}

    # 提取排名資料
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

    # 如果資料為空，返回錯誤
    if not data:
        print("Error: No player data found.")
        return None, date_id_dict

    # 設定欄位名稱
    columns = ["Rank", "Player", "Country", "Points", "Confederation"]
    df = pd.DataFrame(data, columns=columns)
    
    return df, date_id_dict
