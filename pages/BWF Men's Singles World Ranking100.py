import streamlit as st
import pandas as pd
from scrape_bwf_ranking import scrape_bwf_ranking_initial, scrape_bwf_ranking_by_date

# 設定頁面標題
st.title("BWF Men's Singles World Ranking")

# 用來儲存日期和ID對應字典
date_id_dict = {}

# 第一個按鈕：抓取固定日期11/26/2024資料並取得ID對應字典
if st.button("Get Ranking for 11/26/2024"):
    try:
        # 呼叫第一個爬蟲，獲取排名資料並取得日期- ID字典
        df, date_id_dict = scrape_bwf_ranking_initial()

        # 顯示排名資料
        st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:", df)

        # 顯示日期選擇功能
        st.write("Select a different date to get the ranking:")
        date_options = list(date_id_dict.keys())
        selected_date = st.selectbox("Select Date", date_options)

        # 第二個按鈕：根據選擇的日期執行爬蟲
        if selected_date:
            selected_id = date_id_dict[selected_date]
            df_selected = scrape_bwf_ranking_by_date(selected_id)

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


