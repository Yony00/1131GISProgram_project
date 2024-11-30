import streamlit as st
import pandas as pd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入第一次爬蟲的函數
from scrape_bwf_ranking_by_date import scrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數

# 設定頁面標題
st.title("BWF Men's Singles World Ranking")

# 用來儲存日期和ID對應字典
date_id_dict = {}

# 檢查是否已經存儲過第一次爬蟲的資料
if "df_initial" in st.session_state:
    df_initial = st.session_state.df_initial
    date_id_dict = st.session_state.date_id_dict  # 從 session_state 中獲取日期ID對應字典
    st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:")
    st.write(df_initial)

# 第一個按鈕：抓取固定日期11/26/2024資料並取得ID對應字典
if st.button("Get Ranking for 11/26/2024"):
    try:
        # 設定 URL
        url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43340&category=472&C472FOC=&p=1&ps=100"

        # 呼叫第一次爬蟲，獲取排名資料並抓取日期-ID對應字典
        df_initial, date_id_dict = scrape_bwf_ranking(url)

        # 顯示排名資料
        st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:", df_initial)

        # 儲存第一次爬蟲結果到 session_state 中
        st.session_state.df_initial = df_initial
        st.session_state.date_id_dict = date_id_dict  # 儲存日期-ID對應字典

        # 顯示日期選擇功能
        st.write("Select a different date to get the ranking:")
        date_options = list(date_id_dict.keys())  # 從爬蟲結果中獲取日期
        selected_date = st.selectbox("Select Date", date_options)

        # 儲存選擇的日期 ID
        if selected_date:
            selected_id = date_id_dict[selected_date]
            st.session_state.selected_date = selected_date  # 儲存選擇的日期
            st.session_state.selected_id = selected_id  # 儲存選擇的 ID

    except Exception as e:
        st.error(f"Error occurred: {e}")

# 確保選擇的日期仍然保存在 session_state 中，並且顯示選擇的日期
if 'selected_date' in st.session_state and st.session_state.selected_date:
    st.write(f"Selected Date: {st.session_state.selected_date}")

# 第二個按鈕：根據選擇的日期執行爬蟲
if 'selected_id' in st.session_state and st.session_state.selected_id:
    if st.button("Get Ranking for Selected Date"):
        try:
            # 取得選擇的日期 ID
            selected_id = st.session_state.selected_id

            # 呼叫第二個爬蟲，根據 ID 獲取該日期的資料
            df_selected = scrape_bwf_ranking_by_date(selected_id)

            # 顯示選擇日期的排名資料
            selected_date = st.session_state.selected_date  # 從 session_state 中讀取選擇的日期
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

        except Exception as e:
            st.error(f"Error occurred: {e}")
