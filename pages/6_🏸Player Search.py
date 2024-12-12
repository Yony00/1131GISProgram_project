import streamlit as st
import pandas as pd
import geopandas as gpd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入第一次爬蟲的函數
from scrape_bwf_ranking_by_date import scrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數
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

row0_1,XX, row0_2 = st.columns((3,1, 4))
with row0_1:
    st.write(
        """
        ##  
        此頁面提供單一選手的搜尋\n
        先選擇項目、再輸入選手名
        ##
        """
    )
with row0_2:
    st.write(
        """
        ##  
        注意，若沒有要比較兩個時間，則右側日期請保留空白(若誤觸，拉到最上為空白)\n
        若選擇，頁面會顯示左右兩個時間的資料，並且在底下顯示兩個圖台 \n
        當左側圖台移動視角，右側圖台也會跟進(但若移動右側，左側並不會跟著改變)\n
        然而由於技術力的限制，只要有對左側圖台進行操作(如點選、移動)\n
        整個頁面都會進入重run的狀態，圖台會暫時暗掉，但還是可操作狀態\n
        若不喜歡忽亮忽暗的頁面呈現，可於下方 "是否左右圖台聯動"選擇"否"
        """
    )
    user_choice = st.radio("是否左右圖台聯動：", ("是", "否"))
    st.write(
        """
        ##  
        """
    )

# 用來顯示表格的區域
table_area = st.container()

# 表格的左右分區
row1_1, row1_2 = table_area.columns((1, 1))
row2_1, row2_2 = table_area.columns((1, 1))
row3_1, row3_2 = table_area.columns((1, 1))

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







# 使用 selectbox1 讓使用者選擇項目
options = ["男子單打","男子雙打","女子單打","女子雙打","混合單打",]
index = options[1]

options = list(("男子單打","男子雙打","女子單打","女子雙打","混合單打"))
index = options.index(st.session_state.new_date)

with row2_1:
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
        df_selected1 = scrape_bwf_ranking_by_date(selected_id1)
        df_selected1.set_index("Rank", inplace=True)

        # 顯示選擇日期的排名資料於 row1_1
        with row1_1:
            st.write(f"下表為 {selected_date1}  時 男子單打排名資料")
            st.write(df_selected1)
    except Exception as e:
        st.error(f"Error occurred while fetching data for {selected_date1}: {e}")

