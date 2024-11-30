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
            player = cols[1].text.strip()
            country = cols[2].text.strip()
            member_id = cols[3].text.strip()  # 新增 Member ID 欄位
            points = cols[4].text.strip()
            tournaments = cols[5].text.strip()
            confederation = cols[6].text.strip()  # 新增 Confederation 欄位
            country_2 = cols[7].text.strip()  # 假設有兩個 Country 欄位
            
            # 每一行的資料
            data.append([rank, player, country, member_id, points, tournaments, confederation, country_2])

    # 設定欄位名稱
    columns = ["Rank", "Player", "Country", "Member ID", "Points", "Tournaments", "Confederation", "Country"]
    df = pd.DataFrame(data, columns=columns)
    
    return df


