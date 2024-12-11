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
st.set_page_config(page_title="BWF Men's Singles World Ranking", layout="wide")

# 設定頁面標題
st.title("BWF Men's Singles World Ranking")
st.write(
    """
    ##  
    此爬蟲程式，抓取最新時BWF世界羽聯當週紀錄的世界排名資料，取前100名 \n
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
            st.write(f"Below is the BWF Men's Singles World Ranking for {selected_date2}:")
            st.write(df_selected2)
    except Exception as e:
        st.error(f"Error occurred while fetching data for {selected_date2}: {e}")




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
    # 在 Streamlit 中顯示
    st.write("每個國家前一百名的選手數統計(取前十多的國家)")
    st.pyplot(fig)

if selected_date2:

    #按照國家分組-右邊表格
    GB_country2= df_selected2.groupby(by=['Country']).agg(
        player_count=('Player', len),
        playername=('Player',';'.join)
        )
    GB_country2_TOP10=GB_country2.nlargest(10,"player_count")
    
    with row3_2:
        # 繪製條形圖
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=GB_country2_TOP10, x='player_count', y='Country', ax=ax)

    
        # 在 Streamlit 中顯示
        st.write("每個國家前一百名的選手數統計(取前十多的國家)")
        st.pyplot(fig)
####################################################################################ˇ
world_country=gpd.read_file("https://github.com/RGT1143022/BWF_world_country/releases/download/v1.0.0/BWF_world_country_true.geojson")

#賦予geometry轉換為gdf-左
GB_country_withGEO=pd.merge(GB_country,world_country,how='left',on='Country')
GB_country_withGEO = gpd.GeoDataFrame(GB_country_withGEO,geometry=GB_country_withGEO['geometry'])

if not selected_date2:

    #畫地圖-左表格
    
    # 讀取 GeoDataFrame
    gdf1 = GB_country_withGEO
    
    # 假設 gdf 中的數值欄位名為 'value'
    value_column = 'player_count'
    
    # 創建數值正規化範圍
    norm = Normalize(vmin=gdf1[value_column].min(), vmax=gdf1[value_column].max())
    
    # 定義樣式函數（固定藍色，透明度根據數值設置）
    def style_function(feature):
        value = feature["properties"][value_column]
        opacity = norm(value)  # 將數值正規化到 [0, 1] 範圍
        return {
            "fillColor": "#0000FF",  # 固定藍色 (十六進制格式)
            "color": "black",        # 邊框顏色
            "weight": 1,             # 邊框寬度
            "fillOpacity": opacity,  # 根據數值調整透明度
        }
    
    # 創建地圖並添加 GeoDataFrame
    m = leafmap.Map(center=(0, 0), zoom=2)
    m.add_gdf(
        gdf1,
        layer_name=f"BWF Men's Singles World Ranking for {selected_date1}:",
        style_function=style_function,
        info_mode='on_click'
    )
    
    # 顯示地圖
    m.to_streamlit()

##畫地圖-左+右表格
if selected_date2:
    row4_1, row4_2 = table_area.columns((1, 1))
    with row4_1:
        


         #畫地圖-左表格
        # 讀取 GeoDataFrame
        gdf1 = GB_country_withGEO
        
        # 假設 gdf 中的數值欄位名為 'value'
        value_column = 'player_count'
        
        # 創建數值正規化範圍
        norm = Normalize(vmin=gdf1[value_column].min(), vmax=gdf1[value_column].max())
        
        # 定義樣式函數（固定藍色，透明度根據數值設置）
        def style_function(feature):
            value = feature["properties"][value_column]
            opacity = norm(value)  # 將數值正規化到 [0, 1] 範圍
            return {
                "fillColor": "#0000FF",  # 固定藍色 (十六進制格式)
                "color": "black",        # 邊框顏色
                "weight": 1,             # 邊框寬度
                "fillOpacity": opacity,  # 根據數值調整透明度
            }
        
        # 創建地圖並添加 GeoDataFrame
        m = leafmap.Map(location=[0, 0], zoom_start=2)
    
        m.add_gdf(
            gdf1,
            layer_name=f"BWF Men's Singles World Ranking for {selected_date1}:",
            style_function=style_function,
            info_mode='on_click',
            to_left=True
        )      
        #顯示地圖

        #m.to_streamlit()
        output = st_folium(m, height=500, key="map")

    with row4_2:

        #賦予geometry轉換為gdf-右
        GB_country2_withGEO=pd.merge(GB_country2,world_country,how='left',on='Country')
        GB_country2_withGEO = gpd.GeoDataFrame(GB_country2_withGEO,geometry=GB_country2_withGEO['geometry'])
        
        #畫地圖-右表格
        
        # 讀取 GeoDataFrame
        gdf2 = GB_country2_withGEO
        
        # 假設 gdf 中的數值欄位名為 'value'
        value_column = 'player_count'
        
        # 創建數值正規化範圍
        norm = Normalize(vmin=gdf2[value_column].min(), vmax=gdf2[value_column].max())
        
        # 定義樣式函數（固定藍色，透明度根據數值設置）
        def style_function(feature):
            value = feature["properties"][value_column]
            opacity = norm(value)  # 將數值正規化到 [0, 1] 範圍
            return {
                "fillColor": "#ff0000",  # 固定紅色 (十六進制格式)
                "color": "black",        # 邊框顏色
                "weight": 1,             # 邊框寬度
                "fillOpacity": opacity,  # 根據數值調整透明度
            }
        if output:
            center = (output["center"]["lat"],output["center"]["lng"])
            zoom = output["zoom"]
        # 加入之前地圖
        
        m2 = leafmap.Map(location=center, zoom_start=zoom)
        m2.add_gdf(
            gdf2,
            layer_name=f"BWF Men's Singles World Ranking for {selected_date2}:",
            style_function=style_function,
            info_mode='on_click',
             to_right=True
        )
       #m2.to_streamlit()
        output2 = st_folium(m2, height=500, key="map2")
        

    #      #顯示地圖
    #     def sync_view(e):
    #         bounds = m.get_bounds()
    #         m2.fit_bounds(bounds)
    #     m2.on_move(sync_view)
    #     m2.to_streamlit()

# # 设置右图台的视角与左图台同步
# def sync_view(e):
#     bounds = 1.get_bounds()
#     m2.fit_bounds(bounds)

# def sync_view2(e):
#     bounds = m2.get_bounds()
#     m.fit_bounds(bounds)

# # 为左图台添加事件监听，监视视角变化
# m.on_move(sync_view2)

# # 为右图台添加事件监听，监视视角变化
# m2.on_move(sync_view)






