import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_bwf_ranking_by_name(date_id_dict, search_event, player_name):

    from datetime import datetime
    # 轉換字典中的日期格式並按月分類
    monthly_latest = {}
    for date_str, id in date_id_dict.items():
        date = datetime.strptime(date_str, '%m/%d/%Y')
        month_year = date.strftime('%m/%Y')
        if month_year not in monthly_latest:
            monthly_latest[month_year] = (date, id)
        else:
            # 比較當前日期與已存在的日期，保持最晚日期
            if date > monthly_latest[month_year][0]:
                monthly_latest[month_year] = (date, id)
    
    # 提取每個月的最後一天的 ID，格式化為 MM/DD/YYYY
    monthly_latest_id = {date.strftime('%m/%d/%Y'): id for date, id in monthly_latest.values()}
    date_id_dict=monthly_latest_id
    # 設定 URL 模板
    url_templates = {
        "男子單打": "https://bwf.tournamentsoftware.com/ranking/category.aspx?id={id}&category=472&C472FOC=&p=1&ps=100",
        "男子雙打": "https://bwf.tournamentsoftware.com/ranking/category.aspx?id={id}&category=474&C474FOC=&p=1&ps=100",
        "女子單打": "https://bwf.tournamentsoftware.com/ranking/category.aspx?id={id}&category=473&C473FOC=&p=1&ps=100",
        "女子雙打": "https://bwf.tournamentsoftware.com/ranking/category.aspx?id={id}&category=475&C475FOC=&p=1&ps=100",
        "混合雙打": "https://bwf.tournamentsoftware.com/ranking/category.aspx?id={id}&category=476&C476FOC=&p=1&ps=100",
    }

    if search_event not in url_templates:
        raise ValueError("Invalid event type.")

    # 初始化結果列表
    results = []

    # 遍歷所有日期
    for date, id in date_id_dict.items():
        url = url_templates[search_event].format(id=id)

        # 設置 User-Agent 防止被封鎖
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            # 查找表格，這是存放選手排名的地方
            table = soup.find('table', {'class': 'ruler'})
        
            if not table:
                print("Error: No table found")
                return None
        
            # 提取表格中的行
            rows = table.find_all('tr')[1:]  # 跳過表頭

            found = False
            for row in rows:
                cols = row.find_all('td')

                if len(cols) >= 8:
                    rank = cols[0].text.strip()
                    player = cols[4].text.strip()

                    # 根據項目類型處理選手名
                    if search_event in ["男子單打", "女子單打"]:
                        player = player[5:]  # 去除多餘字元
                    else:  # 雙打項目
                        flag = player[:5]
                        player = player.replace(flag, "", 1)
                        player = player.replace(flag, "/", 1)

                    points = cols[7].text.strip()

                    # 如果找到目標選手
                    if player_name == player:
                        results.append([date, rank, points])
                        found = True
                        break

            if not found:
                results.append([date, "nodata", "nodata"])

        except Exception as e:
            results.append([date, "error", str(e)])

    # 將結果轉換為 DataFrame
    df = pd.DataFrame(results, columns=["Date", "Rank", "Points"])
    return df

