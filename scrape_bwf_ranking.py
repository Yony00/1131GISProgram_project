from playwright.sync_api import sync_playwright
import pandas as pd
import os

# 確保 Playwright 的瀏覽器已經安裝
if not os.path.exists('/home/appuser/.cache/ms-playwright'):
    from playwright.__main__ import install
    install()

def scrape_bwf_ranking():
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
    return df

