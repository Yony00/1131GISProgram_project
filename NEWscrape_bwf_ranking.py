from playwright.sync_api import sync_playwright
import pandas as pd
import subprocess

def install_playwright():
    try:
        # 嘗試執行 playwright install 來安裝瀏覽器
        subprocess.run(["python", "-m", "playwright", "install"], check=True)
    except subprocess.CalledProcessError as e:
        print("Playwright install failed:", e)

# 在腳本開頭調用 install_playwright 來確保安裝瀏覽器
install_playwright()

def scrape_bwf_ranking():
    # 使用 Playwright 爬取資料
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 進入目標網站
        url = "https://bwf.tournamentssoftware.com/ranking/ranking.aspx?rid=70"
        page.goto(url)

        # 點擊 "Men's Singles" 分頁
        page.click("text='Men's Singles'")

        # 點擊 "More" 按鈕來顯示更多選手
        while True:
            try:
                page.click("text='More'", timeout=3000)
            except:
                break

        # 抓取排名資料
        table = page.query_selector("table")
        rows = table.query_selector_all("tr")

        rankings = []
        for row in rows[1:]:  # Skip the header row
            cols = row.query_selector_all("td")
            ranking = [col.inner_text().strip() for col in cols]
            rankings.append(ranking)

        # 儲存為 DataFrame
        df = pd.DataFrame(rankings, columns=["Rank", "Name", "Country", "Points"])
        return df

# 執行爬蟲並顯示資料
if __name__ == "__main__":
    try:
        df = scrape_bwf_ranking()
        print(df.head())  # 顯示前五名
    except Exception as e:
        print(f"Error occurred: {e}")
