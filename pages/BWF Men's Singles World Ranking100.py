import streamlit as st
import pandas as pd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入爬蟲腳本

# 設定頁面標題
st.title("BWF Men's Singles World Ranking")

# 當按下按鈕時，抓取資料並顯示
if st.button("Get Ranking"):
    try:
        # 設定URL，並執行爬蟲
        url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43340&category=472&C472FOC=&p=1&ps=100"
        df = scrape_bwf_ranking(url)

        # 顯示排名資料
        st.write("Below is the BWF Men's Singles World Ranking:", df)

        # 如果需要，還可以提供下載 CSV 檔案的功能
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="bwf_ranking.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error occurred: {e}")
