import streamlit as st
import pandas as pd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入你的爬蟲腳本

# 標題
st.title("BWF Men's Singles World Ranking")

# 撰寫一個按鈕來觸發爬蟲
if st.button("Get Ranking"):
    # 爬取排名資料
    df = scrape_bwf_ranking()

    # 顯示表格
    st.dataframe(df)  # 顯示 DataFrame 作為表格

    # 下載排名資料 CSV
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="bwf_ranking.csv",
        mime="text/csv"
    )
