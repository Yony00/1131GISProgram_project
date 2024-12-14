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

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://img1.wallspic.com/previews/0/4/9/5/5/155940/155940-hei_se_he_bai_se_de-he_yin_ying_de_se_cai-xiang_shi_zhi_chu-x750.jpg'); /* 指定背景圖像的URL或路徑 */
                background-size: cover;  /* 讓背景圖像填滿整個視窗 */

        background-position: center;  /* 背景圖像居中 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

markdown = """
圖片來源：中華民國羽球協會
"""
st.sidebar.info(markdown)
logo = "https://s.yimg.com/ny/api/res/1.2/cbnZaTFzRQOhB1rmmqYqMQ--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTc4MjtjZj13ZWJw/https://media.zenfs.com/zh-tw/cna.com.tw/2e01b90a56b4e88a94e7e7c877ec4df3"
st.sidebar.image(logo)

# 設定頁面標題
st.title("Men's Singles 男子單打")

row0_1,XX, row0_2 = st.columns((3,1, 4))
with row0_1:
    st.write(
        """
        ##  
        此頁面提供男子單打的單項查詢  \n
        頁面由上至下分別呈現： \n
        1.選手排名資料表格\n
        2.可供選擇的日期欄位\n
        3.各國在前一百名中佔有的選手數量 長條圖\n
        4.各國在前一百名中佔有的選手數量 分層設色地圖\n
        注：可點選多邊形查看國名、選手數、選手名\n
        ##
        """
    )
with row0_2:
    st.write(
        """
        ##  
        注意，若沒有要比較兩個時間，則右側日期請保留空白\n
        (若誤觸，拉到最上為空白)\n
        若選擇，頁面會顯示左右兩個時間的資料，並且在底下顯示兩個圖台 \n
        當左側圖台移動視角，右側圖台也會跟進\n
        (但若移動右側，左側並不會跟著改變)\n
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
# if selected_date1:
#     try:
#         selected_id1 = date_id_dict[selected_date1]
#         df_selected1 = scrape_bwf_ranking_by_date(selected_id1)
#         df_selected1.set_index("Rank", inplace=True)

#         # 顯示選擇日期的排名資料於 row1_1
#         with row1_1:
#             st.write(f"下表為 {selected_date1}  時 男子單打排名資料")
#             st.write(df_selected1)
#     except Exception as e:
#         st.error(f"Error occurred while fetching data for {selected_date1}: {e}")

# 第二个 selectbox，选择其他日期
with row2_2:
    selected_date2 = st.selectbox(
        "選擇欲查詢的日期",
        [""] + list(date_id_dict.keys()),
        key="selectbox_date2",  # 添加唯一的 key
    )

# 如果選擇了日期
if selected_date2:
    try:
        selected_id2 = date_id_dict[selected_date2]
        df_selected2 = scrape_bwf_ranking_by_date(selected_id2)
        df_selected2.set_index("Rank", inplace=True)

        # 顯示選擇日期的排名資料於 row1_2
        with row1_2:
            st.write(f"下表為 {selected_date2}  時 男子單打排名資料")
            st.write(df_selected2)
    except Exception as e:
        st.error(f"Error occurred while fetching data for {selected_date2}: {e}")



########################################
#設定五個時間
dates=["12/10/2024","12/3/2024","8/2/2018","10/15/2009"]
world_country=gpd.read_file("https://github.com/RGT1143022/BWF_world_country/releases/download/v1.0.0/BWF_world_country_true.geojson")


m = folium.Map(location=[20, 0], zoom_start=2)

# 預先加入所有圖層
layers = {}
for date in dates:
    gdf = world_country.copy()
    gdf["value"] = gdf.index % 10  # 模擬數據
    feature_group = folium.FeatureGroup(name=f"Data for {date}")
    folium.GeoJson(
        data=gdf,
        style_function=lambda x: {
            "fillColor": "blue",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.5,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["Country", "value"],  # 修改為正確的字段名
            aliases=["Country", "Value"],  # 為提示框添加別名
        ),
    ).add_to(feature_group)
    feature_group.add_to(m)
    layers[date] = feature_group

# 添加圖層控制（用於初始化，但用滑動條進行顯示控制）
folium.LayerControl().add_to(m)

# 在 Streamlit 中創建滑動條
selected_date = st.select_slider("Select a date to display", options=dates, value=dates[0])

# 控制圖層顯示（用 JavaScript 控制）
for date, layer in layers.items():
    if date == selected_date:
        layer.control_show = True  # 顯示選中的圖層
    else:
        layer.control_show = False  # 隱藏未選中的圖層

# 在 Streamlit 中顯示地圖
st_folium(m, width=800, height=600)
# #########################################

# #按照國家分組-左邊表格
# GB_country= df_selected1.groupby(by=['Country']).agg(
#     player_count=('Player', len),
#     playername=('Player',';'.join)
#     )
# GB_country_TOP10=GB_country.nlargest(10,"player_count")

# with row3_1:
#     # 繪製條形圖
#     fig, ax = plt.subplots(figsize=(8, 6))
#     sns.barplot(data=GB_country_TOP10, x='player_count', y='Country', ax=ax)
#     # 在 Streamlit 中顯示
#     st.write("每個國家前一百名的選手數統計(取前十多的國家)")
#     st.pyplot(fig)

# if selected_date2:

#     #按照國家分組-右邊表格
#     GB_country2= df_selected2.groupby(by=['Country']).agg(
#         player_count=('Player', len),
#         playername=('Player',';'.join)
#         )
#     GB_country2_TOP10=GB_country2.nlargest(10,"player_count")
    
#     with row3_2:
#         # 繪製條形圖
#         fig, ax = plt.subplots(figsize=(8, 6))
#         sns.barplot(data=GB_country2_TOP10, x='player_count', y='Country', ax=ax)

    
#         # 在 Streamlit 中顯示
#         st.write("每個國家前一百名的選手數統計(取前十多的國家)")
#         st.pyplot(fig)
# ####################################################################################ˇ
# world_country=gpd.read_file("https://github.com/RGT1143022/BWF_world_country/releases/download/v1.0.0/BWF_world_country_true.geojson")

# #賦予geometry轉換為gdf-左
# GB_country_withGEO=pd.merge(GB_country,world_country,how='left',on='Country')
# GB_country_withGEO = gpd.GeoDataFrame(GB_country_withGEO,geometry=GB_country_withGEO['geometry'])

# if not selected_date2:

#     #畫地圖-左表格
    
#     # 讀取 GeoDataFrame
#     gdf1 = GB_country_withGEO
    
#     # 假設 gdf 中的數值欄位名為 'value'
#     value_column = 'player_count'
    
#     # 創建數值正規化範圍
#     norm = Normalize(vmin=gdf1[value_column].min(), vmax=gdf1[value_column].max())
    
#     # 定義樣式函數（固定藍色，透明度根據數值設置）
#     def style_function(feature):
#         value = feature["properties"][value_column]
#         opacity = norm(value)  # 將數值正規化到 [0, 1] 範圍
#         return {
#             "fillColor": "#0000FF",  # 固定藍色 (十六進制格式)
#             "color": "black",        # 邊框顏色
#             "weight": 1,             # 邊框寬度
#             "fillOpacity": opacity,  # 根據數值調整透明度
#         }
    
#     # 創建地圖並添加 GeoDataFrame
#     m = leafmap.Map(center=(0, 0), zoom=2)
#     m.add_gdf(
#         gdf1,
#         layer_name=f"BWF Men's Singles World Ranking for {selected_date1}:",
#         style_function=style_function,
#         info_mode='on_click'
#     )
    
#     # 顯示地圖
#     m.to_streamlit()
