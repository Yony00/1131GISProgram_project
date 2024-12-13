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
import plotly.graph_objects as go




# 設定頁面配置為寬屏模式
st.set_page_config(page_title="Player Search", layout="wide", page_icon=":🏸")
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

# 設定頁面標題
st.title("特定選手/組合搜尋")
logo = "https://media.istockphoto.com/id/1055106830/zh/%E5%90%91%E9%87%8F/%E6%90%9C%E7%B4%A2%E6%AC%84%E5%90%91%E9%87%8F%E5%9C%96%E7%A4%BA.jpg?s=612x612&w=0&k=20&c=DtqxRNbysSBV6reBfJyxPw209o6K67RT7PX1jQN9KTs="
st.sidebar.image(logo)
highlight_word = " LEE Yang/ WANG Chi-Lin"

st.write(
    f"""
    此頁面提供單一選手的搜尋\n
    先選擇項目、再輸入選手名\n
    以組為單位執行搜尋，以雙打為例，要輸入： <mark style="background-color: yellow; padding: 0 2px;">{highlight_word}</mark> \n
    注意開頭有空一格\n
    建議參考下方表格，直接複製選手名欄位\n
    呈現部分包括積分排名變化，以及與該國同時期其他選手之比較
    ##
    """,
    unsafe_allow_html=True
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
    new_date=st.session_state.new_date
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


row1_1, row1_2 ,row1_3= st.columns((2,1,1))
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
with row1_3:
    st.write("若要更改查詢，請在左側資料調整好後，按下方按鈕即可")
    if st.button("清除暫存資料並重新查詢"):   
        st.session_state.clear()

st.markdown(f"<h4>以下是關於 {search_event} 項目， {player_name} 選手的歷年排名、積分變化</h2>", unsafe_allow_html=True)
st.write("執行結果以季度(三個月)為單位呈現，取該月最後一週的排名紀錄")

row2_1, row2_2, row2_3 = st.columns((1,1,1))


# 確保網頁重跑後仍保留爬取的數據
if "df" not in st.session_state:
    st.session_state.df = None

if st.session_state.df is None:
    st.session_state.df = scrape_bwf_ranking_by_name(date_id_dict, search_event, player_name)


if st.session_state.df is not None:
    df = st.session_state.df

    with row2_1:
        # 顯示原始數據
        st.write("所有日期:")
        st.write(df)

    # 下拉選擇日期範圍
    with row2_2:
        dateoptions = df['Date']
        data_end = st.selectbox("結束日期範圍", dateoptions, key="data_end")
        data_start = st.selectbox("開始日期範圍", dateoptions, key="data_start")

    # 篩選操作
    with row2_3:
        if data_end and data_start:
            # 篩選並顯示篩選後的數據
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
            data_start = pd.to_datetime(data_start, format='%m/%d/%Y')
            data_end = pd.to_datetime(data_end, format='%m/%d/%Y')

            # 篩選日期範圍內的數據
            df2 = df[(df['Date'] >= data_start) & (df['Date'] <= data_end)]
            df2['Date'] = df2['Date'].dt.strftime('%m/%d/%Y')  # 恢復日期格式
            df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')  # 恢復日期格式
            st.write("日期已篩選:")
            st.write(df2)
    row3_1, row3_2 = st.columns((1,2))

    with row3_1:
        user_choice = st.radio("使用哪張表格繪圖：", ("左表", "右表"))
    with row3_2:
        if user_choice == "左表":
            plt_df=df.copy()
            plt_df['Date'] = pd.to_datetime(plt_df['Date'], format='%m/%d/%Y')
             # 將 'Points' 列轉換為整數，處理 nodata 與 float64 型別
            plt_df['Points'] = plt_df['Points'].replace('nodata', np.nan).astype(float)  # 替換 'nodata' 為 np.nan 並轉換為浮點數
            plt_df['Rank'] = plt_df['Rank'].replace('nodata', 105).astype(float)  # 替換 'nodata' 為 np.nan 並轉換為浮點數

            # 若仍有 'NaN'，再轉換為整數，這時候應該會成功
            plt_df['Points'] = plt_df['Points'].fillna(0).astype(int)  # 如果還有 'NaN'，填充為 0 並轉換為整數
            plt_df['Rank'] = plt_df['Rank'].fillna(0).astype(int)  # 如果還有 'NaN'，填充為 0 並轉換為整數

            fig, ax1 = plt.subplots(figsize=(10, 6))

            # 左Y軸（積分）折線圖
            sns.lineplot(data=plt_df, x=plt_df['Date'].dt.year, y='Points', ax=ax1, color='blue')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Points', color='blue')
            plt.xticks(rotation=45)  # 繪製 x 軸文字旋轉
            
            # 添加一條紅色水平線在 y=0 處
            ax1.axhline(y=0, color='red', linestyle='--')
            # 右Y軸（Rank）折線圖
            ax2 = ax1.twinx()  # 共享 x 軸
            sns.lineplot(data=plt_df, x=plt_df['Date'].dt.year, y='Rank', ax=ax2, color='green')
            y_ticks2 = range(0, plt_df['Rank'].max() + 10, 10)  # 自動生成連續刻度
            ax2.set_ylabel('Rank', color='green')
            ax2.axhline(y=105, color='brown', linestyle='--')

            ax2.set_yticks(y_ticks2)
            
            # 繪製 Y 軸的連續變數刻度
            y_ticks = range(20000, plt_df['Points'].max() + 10000, 10000)  # 自動生成連續刻度
            ax1.set_yticks(y_ticks)
            
            # 使用線作為 handles 並顯示圖例
            red_line = ax1.axhline(y=0, color='red', linestyle='--')
            brown_line = ax2.axhline(y=105, color='brown', linestyle='--')
            ax1.legend(handles=[red_line], labels=['Points nodata'], fontsize=20, loc='lower left', bbox_to_anchor=(0, 0.1))
            ax2.legend(handles=[brown_line], labels=['Rank nodata'], fontsize=20, loc='upper left', bbox_to_anchor=(0, 0.9))
            st.pyplot(fig)
            
        if user_choice == "右表":
            plt_df=df2.copy()
            if 'nodata' in plt_df['Points'].astype(str).unique():
                legend1 = True
            else:
                legend1 = False
            if 'nodata' in plt_df['Rank'].astype(str).unique():
                legend2 = True
            else:
                legend2 = False            
            plt_df['Date'] = pd.to_datetime(plt_df['Date'], format='%m/%d/%Y')
             # 將 'Points' 列轉換為整數，處理 nodata 與 float64 型別
            plt_df['Points'] = plt_df['Points'].replace('nodata', np.nan).astype(float)  # 替換 'nodata' 為 np.nan 並轉換為浮點數
            plt_df['Rank'] = plt_df['Rank'].replace('nodata', 105).astype(float)  # 替換 'nodata' 為 np.nan 並轉換為浮點數

            # 若仍有 'NaN'，再轉換為整數，這時候應該會成功
            plt_df['Points'] = plt_df['Points'].fillna(0).astype(int)  # 如果還有 'NaN'，填充為 0 並轉換為整數
            plt_df['Rank'] = plt_df['Rank'].fillna(0).astype(int)  # 如果還有 'NaN'，填充為 0 並轉換為整數

            fig, ax1 = plt.subplots(figsize=(10, 6))

            # 左Y軸（積分）折線圖
            sns.lineplot(data=plt_df, x=plt_df['Date'], y='Points', ax=ax1, color='blue')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Points', color='blue')
            plt.xticks(rotation=45)  # 繪製 x 軸文字旋轉
            # 添加一條紅色水平線在 y=0 處
            if legend1:
                ax1.axhline(y=0, color='red', linestyle='--')
                red_line = ax1.axhline(y=0, color='red', linestyle='--')
                ax1.legend(handles=[red_line], labels=['Points nodata'], fontsize=20, loc='lower left', bbox_to_anchor=(0, 0.1))


            # 右Y軸（Rank）折線圖
            ax2 = ax1.twinx()  # 共享 x 軸
            sns.lineplot(data=plt_df, x=plt_df['Date'], y='Rank', ax=ax2, color='green')
            y_ticks2 = range(0, plt_df['Rank'].max() + 10, 10)  # 自動生成連續刻度
            ax2.set_ylabel('Rank', color='green')
            if legend2:
                ax2.axhline(y=105, color='brown', linestyle='--')
                brown_line = ax2.axhline(y=105, color='brown', linestyle='--')   
                ax2.legend(handles=[brown_line], labels=['Rank nodata'], fontsize=20, loc='upper left', bbox_to_anchor=(0, 0.9))

            ax2.set_yticks(y_ticks2)

            # 繪製 Y 軸的連續變數刻度
            y_ticks = range(20000, plt_df['Points'].max() + 10000, 10000)  # 自動生成連續刻度
            ax1.set_yticks(y_ticks)
            
            
            st.pyplot(fig)

    row4_1, row4_2 = st.columns((2,1))

    with row4_1:
        st.markdown("### 與該國同時期其他選手/組合比較：")

    with row4_2:
        CP_dataoptions = list(date_id_dict.keys())
        index = CP_dataoptions.index(new_date)

        CP_data = st.selectbox(
            "選擇欲查詢的日期 (預設最新日期)",
            CP_dataoptions,
            index=index,
            key="CP_data",  # 添加唯一的 key
            )
    row5_1, row5_2 = st.columns((2,1))

    if CP_data  :
        CP_data_id1 = date_id_dict[CP_data]
        
        MS_df = scrape_bwf_ranking_by_date(CP_data_id1)
        MD_df = MDscrape_bwf_ranking_by_date(CP_data_id1)
        WS_df = WSscrape_bwf_ranking_by_date(CP_data_id1)
        WD_df = WDscrape_bwf_ranking_by_date(CP_data_id1)
        MXD_df = MXDscrape_bwf_ranking_by_date(CP_data_id1)        

        if search_event == "男子單打":
            country = MS_df.loc[MS_df['Player'] == player_name, 'Country'].values
            country=country[0]
            CP_df_event= MS_df[MS_df['Country'] == country]
            # 繪製 Pie 圖表
            with row5_1:
                # 指定需要凸顯的選手
                highlight_player = player_name
                
                # 根據指定選手生成 pull 數據（凸顯效果）
                CP_df_event['pull'] = CP_df_event['Player'].apply(lambda x: 0.2 if x == highlight_player else 0.0)

                fig = go.Figure(data=[go.Pie(labels= CP_df_event['Player'] + " (Rank: " + CP_df_event['Rank'].astype(str) + ")",
                                             values=CP_df_event["Points"],    pull=CP_df_event['pull'],  # 添加凸顯參數

                                            )],
                                

                                layout=go.Layout(
                                    title=go.layout.Title(text=f"該時期 {country}  {selected_event} 積分占比")
                                ))
                
                # 在 Streamlit 中顯示 Pie 圖表
                st.plotly_chart(fig)
        elif search_event == "男子雙打":
            country = MD_df.loc[MD_df['Player'] == player_name, 'Country'].values
            country=country[0]
            CP_df_event= MD_df[MD_df['Country'] == country]
            # 繪製 Pie 圖表
            with row5_1:
                # 指定需要凸顯的選手
                highlight_player = player_name
                
                # 根據指定選手生成 pull 數據（凸顯效果）
                CP_df_event['pull'] = CP_df_event['Player'].apply(lambda x: 0.2 if x == highlight_player else 0.0)

                fig = go.Figure(data=[go.Pie(labels= CP_df_event['Player'] + " (Rank: " + CP_df_event['Rank'].astype(str) + ")",
                                             values=CP_df_event["Points"],    pull=CP_df_event['pull'],  # 添加凸顯參數

                                            )],
                                

                                layout=go.Layout(
                                    title=go.layout.Title(text=f"該時期 {country}  {selected_event} 積分占比")
                                ))
                
                # 在 Streamlit 中顯示 Pie 圖表
                st.plotly_chart(fig)
        elif search_event == "女子單打":
            country = WS_df.loc[WS_df['Player'] == player_name, 'Country'].values
            country=country[0]
            CP_df_event= WS_df[WS_df['Country'] == country]
            # 繪製 Pie 圖表
            with row5_1:
                # 指定需要凸顯的選手
                highlight_player = player_name
                
                # 根據指定選手生成 pull 數據（凸顯效果）
                CP_df_event['pull'] = CP_df_event['Player'].apply(lambda x: 0.2 if x == highlight_player else 0.0)

                fig = go.Figure(data=[go.Pie(labels= CP_df_event['Player'] + " (Rank: " + CP_df_event['Rank'].astype(str) + ")",
                                             values=CP_df_event["Points"],    pull=CP_df_event['pull'],  # 添加凸顯參數

                                            )],
                                

                                layout=go.Layout(
                                    title=go.layout.Title(text=f"該時期 {country}  {selected_event} 積分占比")
                                ))
                
                # 在 Streamlit 中顯示 Pie 圖表
                st.plotly_chart(fig)
        elif search_event == "女子雙打":
            country = WD_df.loc[WD_df['Player'] == player_name, 'Country'].values
            country=country[0]
            CP_df_event= WD_df[WD_df['Country'] == country]
            # 繪製 Pie 圖表
            with row5_1:
                # 指定需要凸顯的選手
                highlight_player = player_name
                
                # 根據指定選手生成 pull 數據（凸顯效果）
                CP_df_event['pull'] = CP_df_event['Player'].apply(lambda x: 0.2 if x == highlight_player else 0.0)

                fig = go.Figure(data=[go.Pie(labels= CP_df_event['Player'] + " (Rank: " + CP_df_event['Rank'].astype(str) + ")",
                                             values=CP_df_event["Points"],    pull=CP_df_event['pull'],  # 添加凸顯參數

                                            )],
                                

                                layout=go.Layout(
                                    title=go.layout.Title(text=f"該時期 {country}  {selected_event} 積分占比")
                                ))
                
                # 在 Streamlit 中顯示 Pie 圖表
                st.plotly_chart(fig)
        elif search_event == "混合雙打":
            country = MXD_df.loc[MXD_df['Player'] == player_name, 'Country'].values
            country=country[0]
            CP_df_event= MXD_df[MXD_df['Country'] == country]
            # 繪製 Pie 圖表
            with row5_1:
                # 指定需要凸顯的選手
                highlight_player = player_name
                
                # 根據指定選手生成 pull 數據（凸顯效果）
                CP_df_event['pull'] = CP_df_event['Player'].apply(lambda x: 0.2 if x == highlight_player else 0.0)

                fig = go.Figure(data=[go.Pie(labels= CP_df_event['Player'] + " (Rank: " + CP_df_event['Rank'].astype(str) + ")",
                                             values=CP_df_event["Points"],    pull=CP_df_event['pull'],  # 添加凸顯參數

                                            )],
                                

                                layout=go.Layout(
                                    title=go.layout.Title(text=f"該時期 {country}  {selected_event} 積分占比")
                                ))
                
                # 在 Streamlit 中顯示 Pie 圖表
                st.plotly_chart(fig)
        
            


        CP_df_event_MS= MS_df[MS_df['Country'] == country]
        CP_df_event_MD= MD_df[MD_df['Country'] == country]
        CP_df_event_WS= WS_df[WS_df['Country'] == country]
        CP_df_event_WD= WD_df[WD_df['Country'] == country]
        CP_df_event_MXD= MXD_df[MXD_df['Country'] == country]

        # 項目名稱列表
        events =["男子單打", "男子雙打", "女子單打", "女子雙打", "混合雙打"]
        # 建立圖表
        fig = go.Figure()
        
        # 添加每個項目的長條圖
        fig.add_trace(go.Bar(
            name="男子單打",
            x=CP_df_event_MS['Player'],  # X 軸：選手名字
            y=CP_df_event_MS['Points']    ,    # Y 軸：積分
            text=CP_df_event_MS['Rank'],      # 在長條圖上顯示排名
            textposition='inside',  # 設置文字顯示位置
            textfont=dict(size=18),
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name="女子單打",
            x=CP_df_event_WS['Player'], 
            y=CP_df_event_WS['Points'],
            text=CP_df_event_WS['Rank'],      # 在長條圖上顯示排名
            textposition='inside',  # 設置文字顯示位置
            textfont=dict(size=18),
            marker_color='pink'
        ))
        
        fig.add_trace(go.Bar(
            name="男子雙打",
            x=CP_df_event_MD['Player'], 
            y=CP_df_event_MD['Points'],
            text=CP_df_event_MD['Rank'],      # 在長條圖上顯示排名
            textposition='inside',  # 設置文字顯示位置
            textfont=dict(size=18),
            marker_color='blue'
        ))
        
        fig.add_trace(go.Bar(
            name="女子雙打",
            x=CP_df_event_WD['Player'], 
            y=CP_df_event_WD['Points'],
            text=CP_df_event_WD['Rank'],      # 在長條圖上顯示排名
            textposition='inside',  # 設置文字顯示位置
            textfont=dict(size=18),
            marker_color='red'
        ))
        
        fig.add_trace(go.Bar(
            name="混合雙打",
            x=CP_df_event_MXD['Player'], 
            y=CP_df_event_MXD['Points'],
            text=CP_df_event_MXD['Rank'],      # 在長條圖上顯示排名
            textposition='inside',  # 設置文字顯示位置
            textfont=dict(size=18),
            marker_color='green'
        ))
        
        # 更新圖表標題與布局
        fig.update_layout(
            barmode='group',  # 以群組形式顯示柱狀圖
            title=f"該時期 {country} 不同項目中，不同選手的積分、排名，圖中數字為世界排名(Rank)",
            xaxis_title="Players",
            yaxis=dict(
                        title='Points',          # Y 軸的標題
                        range=[0, 120000],        # Y 軸的範圍
                        ),
            legend_title="Event",
            height=700,  # 調整圖表高度
            width=1500    # 可根據需要設置寬度

        )
   
        
        # 顯示圖表
        st.plotly_chart(fig)
    
                
  



