import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_bwf_ranking():
    # 設置目標 URL
    url = "https://bwf.tournamentsoftware.com/ranking/ranking.aspx?rid=70"

    # 發送請求獲取網頁內容
    response = requests.get(url)

    # 解析 HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 找到排名表格
    table = soup.find('table', {'class': 'ruler'})

    # 提取表格中的行
    rows = table.find_all('tr')[1:]  # 跳過表頭

    data = []
    for row in rows:
        cols = row.find_all('td')
        # 提取每一列的資料
        data.append([col.text.strip() for col in cols])

    # 將數據轉換為 DataFrame 並返回
    columns = ["Rank", "Player", "Country", "Points", "Tournaments"]
    df = pd.DataFrame(data, columns=columns)
    return df

