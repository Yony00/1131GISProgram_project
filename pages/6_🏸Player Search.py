import streamlit as st
import pandas as pd
import geopandas as gpd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入第一次爬蟲的函數
from scrape_bwf_ranking_by_date import scrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數
from scrape_bwf_ranking_by_date import MDscrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數
from scrape_bwf_ranking_by_date import WSscrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數
from scrape_bwf_ranking_by_date import WDscrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數
from scrape_bwf_ranking_by_date import MXDscrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數
from scrape_bwf_ranking_by_name import scrape_bwf_ranking_by_name  # 引入名字爬蟲的函數


import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import leafmap.foliumap as leafmap
from matplotlib.colors import Normalize

from streamlit_folium import st_folium
import folium

from datetime import datetime



# 設定頁面配置為寬屏模式
st.set_page_config(page_title="Men's Singles", layout="wide", page_icon=":🏸")

# 設定頁面標題
st.title("Men's Singles 男子單打")


st.write(
    """
    此頁面提供單一選手的搜尋\n
    先選擇項目、再輸入選手名\n
    以組為單位執行搜尋，以雙打為例，要輸入： LEE Yang/ WANG Chi-Lin\n 
    注意開頭有空一格\n 
    建議參考下方表格，直接複製選手名欄位\n

    執行結果以季度(三個月)為單位呈現
    取該月最後一周的排名紀錄
    ##
    """
)
row0_1, row0_2 = st.columns((1,2))


# 用來顯示表格的區域
table_area = st.container()

# 檢查是否已經存儲過第一次爬蟲的資料
if "df_initial" not in st.session_state:  # 只有在第一次爬蟲未完成時才會執行
    try:
        url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43595&category=473&C473FOC=&p=1&ps=100"

        # 呼叫第一次爬蟲，獲取排名資料並抓取日期-ID對應字典
        df_initial, date_id_dict,new_date = scrape_bwf_ranking(url)

        # 儲存第一次爬蟲結果到 session_state 中
        df_initial.set_index("Rank", inplace=True)
        st.session_state.df_initial = df_initial
        st.session_state.date_id_dict = date_id_dict  # 儲存日期-ID對應字典
        st.session_state.first_scrape_done = True  # 設定標記，表示第一次爬蟲已經完成
        st.session_state.new_date=new_date # 儲存最新日期
    except Exception as e:
        st.error(f"Error occurred: {e}")

if "date_id_dict" in st.session_state:
    date_id_dict = st.session_state.date_id_dict
##################

##################
# 使用 selectbox1 讓使用者選擇日期(預設為 st.session_state.new_date)
options = list(date_id_dict.keys())
index = options.index(st.session_state.new_date)

with row0_1:
    options_event = ["男子單打", "男子雙打", "女子單打", "女子雙打", "混合雙打"]
    # 預設選中第二項 "男子雙打"
    index = 0  # 索引從 0 開始
    # 顯示下拉選單
    selected_event = st.selectbox(
        "選擇欲查詢的項目",  # 顯示的標題
        options_event,  # 選項列表
        index=index,  # 預設選中的索引
        key="selectbox_event",  # 唯一的 key
    )
with row0_2:
    selected_date1 = st.selectbox(
        "選擇欲查詢的日期 (預設最新日期)",
        options,
        index=index,
        key="selectbox_date1",  # 添加唯一的 key
    )

# 如果選擇了日期
if selected_date1:
    try:
        selected_id1 = date_id_dict[selected_date1]
        if selected_event == "男子單打":
            df_selected1 = scrape_bwf_ranking_by_date(selected_id1)
        elif selected_event == "男子雙打":
            df_selected1 = MDscrape_bwf_ranking_by_date(selected_id1)
        elif selected_event == "女子單打":
            df_selected1 = WSscrape_bwf_ranking_by_date(selected_id1)
        elif selected_event == "女子雙打":
            df_selected1 = WDscrape_bwf_ranking_by_date(selected_id1)
        elif selected_event == "混合雙打":
            df_selected1 = MXDscrape_bwf_ranking_by_date(selected_id1)
        df_selected1.set_index("Rank", inplace=True)

        # 顯示選擇日期的排名資料於 row1_1
        with table_area:
            st.write(f"下表為 {selected_date1}  時 {selected_event} 排名資料")
            st.write(df_selected1)
    except Exception as e:
        st.error(f"Error occurred while fetching data for {selected_date1}: {e}")


row1_1, row1_2 = st.columns((2,1))
with row1_2:
    options_event = ["男子單打", "男子雙打", "女子單打", "女子雙打", "混合雙打"]
    # 預設選中第二項 "男子雙打"
    index = 0  # 索引從 0 開始
    # 顯示下拉選單
    search_event = st.selectbox(
        "該選手(組合)的項目",  # 顯示的標題
        options_event,  # 選項列表
        index=index,  # 預設選中的索引
        key="search_event",  # 唯一的 key
    )
with row1_1:
    player_name = st.text_input("請輸入欲查詢的選手名(組合名)，格式參考上表：", "", key="player_name")
st.markdown(f"<h4>以下是關於 {search_event} 項目， {player_name} 選手的歷年排名變化</h2>", unsafe_allow_html=True)

row2_1, row2_2, row2_3 = st.columns((1,1,1))



# if player_name:
#     df=scrape_bwf_ranking_by_name(date_id_dict,search_event,player_name)
#     st.session_state.df = df
#     with row2_1:
#         st.write(df)
#     with row2_2:
#         dateoptions = df['Date']
#         index = 0  # 索引從 0 開始
#         # 顯示下拉選單
#         data_end = st.selectbox(
#             "結束日期範圍",  # 顯示的標題
#             dateoptions,  # 選項列表
#             index=index,  # 預設選中的索引
#             key="data_end",  # 唯一的 key
#         )    
#         data_start = st.selectbox(
#             "開始日期範圍",  # 顯示的標題
#             dateoptions,  # 選項列表
#             index=df.index.max(),  # 預設選中的索引
#             key="data_start",  # 唯一的 key
#         )
#     with row2_3:
#         if data_end and data_start:
#             df=st.session_state.df
#             df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')  # 將日期轉換為 datetime 格式
#             data_start = pd.to_datetime(data_start, format='%m/%d/%Y')
#             data_end = pd.to_datetime(data_end, format='%m/%d/%Y')
            
#             # 篩選符合日期區間的資料
#             df2 = df[(df['Date'] >= data_start) & (df['Date'] <= data_end)]
            
#             # 將結果轉換回原來的日期格式
#             df2['Date'] = df2['Date'].dt.strftime('%m/%d/%Y')
#             st.write(df2)
            


##############
# # 確保網頁重跑後仍保留爬取的數據
# if "df" not in st.session_state:
#     st.session_state.df = None

# if player_name and st.session_state.df is None:
#     # 只在初次輸入名稱時爬取資料
#     st.session_state.df = scrape_bwf_ranking_by_name(date_id_dict, search_event, player_name)

# if st.session_state.df is not None:
#     df = st.session_state.df

#     with row2_1:
#         # 顯示原始數據
#         st.write("Original DataFrame:")
#         st.write(df)

#     # 下拉選擇日期範圍
#     with row2_2:
#         dateoptions = df['Date']
#         data_end = st.selectbox("結束日期範圍", dateoptions, index=0, key="data_end")
#         data_start = st.selectbox("開始日期範圍", dateoptions, index=len(dateoptions) - 1, key="data_start")

#     # 篩選操作
#     with row2_3:
#         if data_end and data_start:
#             # 篩選並顯示篩選後的數據
#             df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
#             data_start = pd.to_datetime(data_start, format='%m/%d/%Y')
#             data_end = pd.to_datetime(data_end, format='%m/%d/%Y')

#             # 篩選日期範圍內的數據
#             df2 = df[(df['Date'] >= data_start) & (df['Date'] <= data_end)]
#             df2['Date'] = df2['Date'].dt.strftime('%m/%d/%Y')  # 恢復日期格式
#             st.write("Filtered DataFrame:")
#             st.write(df2)

# 初始化狀態
if "df" not in st.session_state:
    st.session_state.df = scrape_bwf_ranking_by_name(date_id_dict, search_event, player_name)
    # 確保 Date 欄位轉換為 datetime
    st.session_state.df['Date'] = pd.to_datetime(st.session_state.df['Date'], format='%m/%d/%Y')
    st.session_state.filtered_df = st.session_state.df.copy()

# 顯示原始數據
st.write("Original DataFrame:")
st.write(st.session_state.df)

# 日期選擇器
dateoptions = st.session_state.df['Date'].dt.strftime('%m/%d/%Y').tolist()  # 確保是字串列表
data_end = st.selectbox("結束日期範圍", dateoptions, index=0, key="data_end")
data_start = st.selectbox("開始日期範圍", dateoptions, index=len(dateoptions) - 1, key="data_start")

# 確保選擇的日期是 datetime 格式
data_start_dt = datetime.strptime(data_start, '%m/%d/%Y')
data_end_dt = datetime.strptime(data_end, '%m/%d/%Y')

# 篩選數據
if data_start_dt <= data_end_dt:
    st.session_state.filtered_df = st.session_state.df[
        (st.session_state.df['Date'] >= data_start_dt) &
        (st.session_state.df['Date'] <= data_end_dt)
    ]

# 顯示篩選後的結果
st.write("Filtered DataFrame:")
filtered_df = st.session_state.filtered_df.copy()
filtered_df['Date'] = filtered_df['Date'].dt.strftime('%m/%d/%Y')  # 恢復日期格式顯示
st.write(filtered_df)
filtered_df['Date'] = filtered_df['Date'].dt.strftime('%m/%d/%Y')  # 恢復日期格式顯示
st.write(filtered_df)
