import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_bwf_ranking():
    url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43340&category=472&C472FOC=&p=1&ps=100"
    
    # 設置 User-Agent 防止被封鎖
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    # 解析 HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 打印 HTML 結構，檢查是否正確提取資料
    print(soup.prettify()[:500])  # 可以檢查前500個字符來理解頁面結構

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
        
        # 確保行中包含預期的數據
        if len(cols) >= 5:  # 根據表格結構，確保每一行至少有5列數據
            rank = cols[0].text.strip()
            player = cols[1].text.strip()
            country = cols[2].text.strip()
            points = cols[3].text.strip()
            tournaments = cols[4].text.strip()
            data.append([rank, player, country, points, tournaments])

    columns = ["Rank", "Player", "Country", "Points", "Tournaments"]
    df = pd.DataFrame(data, columns=columns)
    
    # 顯示 DataFrame 並返回
    return df


