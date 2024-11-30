import streamlit as st
import pandas as pd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入爬蟲腳本

# 設定頁面標題
st.title("BWF Men's Singles World Ranking")

# 用來儲存日期和ID對應字典
date_id_dict = {}

# 當按下按鈕時，抓取資料並顯示
if st.button("Get Ranking for 11/26/2024"):
    try:
        # 設定固定的 URL 並執行爬蟲
        url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43340&category=472&C472FOC=&p=1&ps=100"
        df, date_id_dict = scrape_bwf_ranking(url)

        # 顯示排名資料
        st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:", df)

        # 顯示日期選擇功能
        st.write("Select a different date to get the ranking:")
        date_options = list(date_id_dict.keys())
        selected_date = st.selectbox("Select Date", date_options)

        # 當使用者選擇日期後，再次執行爬蟲並顯示選擇日期的資料
        if selected_date:
            selected_id = date_id_dict[selected_date]
            selected_url = f"https://bwf.tournamentsoftware.com/ranking/category.aspx?id={selected_id}&category=472&C472FOC=&p=1&ps=100"

            # 執行爬蟲抓取所選日期的資料
            df_selected, _ = scrape_bwf_ranking(selected_url)

            # 顯示選擇日期的排名資料
            st.write(f"Below is the BWF Men's Singles World Ranking for {selected_date}:", df_selected)

            # 提供下載 CSV 檔案的功能
            st.download_button(
                label="Download CSV for Selected Date",
                data=df_selected.to_csv(index=False),
                file_name=f"bwf_ranking_{selected_date}.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error occurred: {e}")


