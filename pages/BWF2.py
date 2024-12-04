import streamlit as st
import pandas as pd
from scrape_bwf_ranking import scrape_bwf_ranking  # 引入第一次爬蟲的函數
from scrape_bwf_ranking_by_date import scrape_bwf_ranking_by_date  # 引入第二次爬蟲的函數

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

# 按鈕區域
button_area = st.container()

# 檢查是否已經存儲過第一次爬蟲的資料
if "df_initial" not in st.session_state:  # 只有在第一次爬蟲未完成時才會執行
    try:
        url = "https://bwf.tournamentsoftware.com/ranking/category.aspx?id=43340&category=472&C472FOC=&p=1&ps=100"

        # 呼叫第一次爬蟲，獲取排名資料並抓取日期-ID對應字典
        df_initial, date_id_dict = scrape_bwf_ranking(url)

        # 儲存第一次爬蟲結果到 session_state 中
        df_initial.set_index("Rank", inplace=True)
        st.session_state.df_initial = df_initial
        st.session_state.date_id_dict = date_id_dict  # 儲存日期-ID對應字典
        st.session_state.first_scrape_done = True  # 設定標記，表示第一次爬蟲已經完成

    except Exception as e:
        st.error(f"Error occurred: {e}")

# 顯示排名資料
if "df_initial" in st.session_state:
    with row1_1:
        st.write("Below is the BWF Men's Singles World Ranking for 11/26/2024:")
        st.write(st.session_state.df_initial)

# 顯示所有日期的按鈕
if "date_id_dict" in st.session_state:
    date_id_dict = st.session_state.date_id_dict

    with button_area:
        # 添加滾動樣式
        st.markdown(
            """
            <style>
            .scrollable-buttons {
                height: 200px;  /* 調整區域高度 */
                overflow-y: auto;  /* 垂直滾動 */
                border: 1px solid #ccc;
                padding: 10px;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # 滾動區域容器
        st.markdown('<div class="scrollable-buttons">', unsafe_allow_html=True)
        columns = st.columns(7)  # 分成多列按鈕
        for idx, (date, date_id) in enumerate(date_id_dict.items()):
            col_idx = idx % 7  # 計算按鈕應該顯示在哪一列
            with columns[col_idx]:
                if st.button(f"{date}", key=f"button_{date}"):
                    try:
                        # 呼叫第二次爬蟲
                        df_selected = scrape_bwf_ranking_by_date(date_id)
                        df_selected.set_index("Rank", inplace=True)
                        with row1_2:
                            st.write(f"Below is the BWF Men's Singles World Ranking for {date}:")
                            st.write(df_selected)
                    except Exception as e:
                        st.error(f"Error occurred: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
