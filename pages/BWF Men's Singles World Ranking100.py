import streamlit as st
import pandas as pd
import geopandas as gpd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入第一次爬蟲的函數
from scrape_bwf_ranking_by_date import scrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

# 設定頁面配置為寬屏模式
st.set_page_config(page_title="BWF Men's Singles World Ranking", layout="wide")

# 設定頁面標題
st.title("BWF Men's Singles World Ranking")
st.write(
    """
    ##  
    此爬蟲程式，抓取2024/11/26時BWF世界羽聯當週紀錄的世界排名資料，取前100名 \n
    此頁面顯示為男子單打項目 \n
    可選擇過去其他週次的紀錄進行比對\n
    期末大概就是透過爬蟲抓資料，繪製統計圖表、leafmap(期中有的，再加上一些年份的變化比較吧)\n
    有想法歡迎提供，例如想看什麼的統計、地圖\n      
    此程式ChatGPT出了90%力，感謝哆啦GPT夢
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
        url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43340&category=472&C472FOC=&p=1&ps=100"

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


# 如果已經成功取得日期-ID 對應字典，生成 selectbox
if "date_id_dict" in st.session_state:
    date_id_dict = st.session_state.date_id_dict

##################
# 使用 selectbox1 讓使用者選擇日期(預設為 st.session_state.new_date)
options = list(date_id_dict.keys())
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
            st.write(f"Below is the BWF Men's Singles World Ranking for {selected_date1}:")
            st.write(df_selected1)
    except Exception as e:
        st.error(f"Error occurred while fetching data for {selected_date1}: {e}")

# 第二个 selectbox，选择其他日期
with row2_2:
    selected_date = st.selectbox(
        "選擇欲查詢的日期",
        [""] + list(date_id_dict.keys()),
        key="selectbox_date2",  # 添加唯一的 key
    )

# 如果選擇了日期
if selected_date:
    try:
        selected_id = date_id_dict[selected_date]
        df_selected = scrape_bwf_ranking_by_date(selected_id)
        df_selected.set_index("Rank", inplace=True)

        # 顯示選擇日期的排名資料於 row1_2
        with row1_2:
            st.write(f"Below is the BWF Men's Singles World Ranking for {selected_date}:")
            st.write(df_selected)
    except Exception as e:
        st.error(f"Error occurred while fetching data for {selected_date}: {e}")



world_country=gpd.read_file("https://github.com/RGT1143022/BWF_world_country/releases/download/v1.0.0/BWF_world_country_true.geojson")

#按照國家分組-左邊表格
GB_country= df_selected1.groupby(by=['Country']).agg(
    player_count=('Player', len),
    playername=('Player',';'.join)
    )
GB_country_TOP10=GB_country.nlargest(10,"player_count")

with row3_1:
    # 繪製條形圖
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=GB_country_TOP10, x='player_count', y='Country', ax=ax)
    ax.set_title("Example Bar Chart")

    # 在 Streamlit 中顯示
    st.pyplot(fig)


#按照國家分組-右邊表格
GB_country= df_selected.groupby(by=['Country']).agg(
    player_count=('Player', len),
    playername=('Player',';'.join)
    )
GB_country_TOP10=GB_country.nlargest(10,"player_count")

with row3_2:
    # 繪製條形圖
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=GB_country_TOP10, x='player_count', y='Country', ax=ax)
    ax.set_title("Example Bar Chart")

    # 在 Streamlit 中顯示
    st.pyplot(fig)
