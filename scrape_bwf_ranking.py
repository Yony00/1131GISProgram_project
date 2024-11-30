from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_bwf_ranking():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 進入目標網站
            url = "https://bwf.tournamentsoftware.com/ranking/ranking.aspx?rid=70"
            page.goto(url)

            # 點擊 "Men's Singles" 分頁
            page.click("text=Men's Singles")

            # 點擊 "More" 按鈕以加載更多選手
            while True:
                try:
                    page.click("text=More", timeout=3000)
                except:
                    break  # 沒有 "More" 按鈕時退出

            # 提取表格數據
            rows = page.query_selector_all("table.ruler tbody tr")
            data = []
            for row in rows:
                cols = row.query_selector_all("td")
                data.append([col.inner_text().strip() for col in cols])

            browser.close()

        # 將數據存為 DataFrame 並返回
        columns = ["Rank", "Player", "Country", "Points", "Tournaments"]
        df = pd.DataFrame(data, columns=columns)
        # 保存為 CSV
        df.to_csv("bwf_ranking.csv", index=False)
        print("爬蟲成功，數據已保存為 bwf_ranking.csv")
        return df

    except Exception as e:
        print(f"爬蟲失敗：{e}")
        return pd.DataFrame()  # 返回空表
