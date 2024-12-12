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



# 設定頁面配置為寬屏模式
st.set_page_config(page_title="Men's Singles", layout="wide", page_icon=":🏸")

# 設定頁面標題
st.title("Men's Singles 男子單打")


st.write(
    """
    此頁面提供單一選手的搜尋\n
    先選擇項目、再輸入選手名
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

st.json(date_id_dict)
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


row1_1, row1_2 = st.columns((1,2))
with row1_1:
    options_event = ["男子單打", "男子雙打", "女子單打", "女子雙打", "混合雙打"]
    # 預設選中第二項 "男子雙打"
    index = 0  # 索引從 0 開始
    # 顯示下拉選單
    search_event = st.selectbox(
        "選擇欲查詢的項目",  # 顯示的標題
        options_event,  # 選項列表
        index=index,  # 預設選中的索引
        key="search_event",  # 唯一的 key
    )
with row1_2:
    player_name = st.text_input("請輸入欲查詢的選手名(組合名)，格式參考上表：", "", key="player_name")
st.markdown(f"<h4>以下是關於 {search_event} 項目， {player_name} 選手的歷年排名變化</h2>", unsafe_allow_html=True)

if player_name:
    df=scrape_bwf_ranking_by_name(date_id_dict,search_event,player_name)
st.write(df)
