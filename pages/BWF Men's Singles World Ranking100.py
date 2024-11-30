import streamlit as st
import pandas as pd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入第一次爬蟲的函數
from scrape_bwf_ranking_by_date import scrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數

# 設定頁面標題
st.title("BWF Men's Singles World Ranking")

# 用來顯示表格的區域
table_area = st.container()

# 按鈕區域
button_area = st.container()

# 檢查是否已經存儲過第一次爬蟲的資料
if "df_initial" in st.session_state:
    df_initial = st.session_state.df_initial
    date_id_dict = st.session_state.date_id_dict  # 從 session_state 中獲取日期ID對應字典
    
    with table_area:
        st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:")
        st.write(df_initial)

# 第一個按鈕：抓取固定日期11/26/2024資料並取得ID對應字典
if "first_scrape_done" not in st.session_state or not st.session_state.first_scrape_done:
    with button_area:
        if st.button("Get Ranking for 11/26/2024"):
            try:
                # 設定 URL
                url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43340&category=472&C472FOC=&p=1&ps=100"

                # 呼叫第一次爬蟲，獲取排名資料並抓取日期-ID對應字典
                df_initial, date_id_dict = scrape_bwf_ranking(url)

                # 儲存第一次爬蟲結果到 session_state 中
                st.session_state.df_initial = df_initial
                st.session_state.date_id_dict = date_id_dict  # 儲存日期-ID對應字典
                st.session_state.first_scrape_done = True  # 設定標記，表示第一次爬蟲已經完成

                # 顯示排名資料
                with table_area:
                    st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:")
                    st.write(df_initial)

            except Exception as e:
                st.error(f"Error occurred: {e}")

# 顯示所有日期的按鈕
if "date_id_dict" in st.session_state:
    date_id_dict = st.session_state.date_id_dict

    with button_area:
        # 每行顯示五個按鈕
        columns = st.columns(5)  # 分成 5 列
        for idx, (date, date_id) in enumerate(date_id_dict.items()):
            # 確保每 5 個按鈕放在同一行
            col_idx = idx % 5  # 計算該按鈕應該顯示在第幾列
            with columns[col_idx]:
                if st.button(f"Get Ranking for {date}", key=f"button_{date}"):  # 使用 `key` 來確保每個按鈕有唯一 ID
                    try:
                        # 確保字典中有對應的日期
                        selected_id = date_id  # 根據選擇的日期，獲取對應的 ID

                        # 呼叫第二個爬蟲，根據 ID 獲取該日期的資料
                        df_selected = scrape_bwf_ranking_by_date(selected_id)

                        # 顯示選擇日期的排名資料
                        with table_area:
                            st.write(f"Below is the BWF Men's Singles World Ranking for {date}:")
                            st.write(df_selected)

                    except Exception as e:
                        st.error(f"Error occurred: {e}")
