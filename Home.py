import streamlit as st
import leafmap.foliumap as leafmap
st.set_page_config(page_title="BWF World Ranking", layout="wide")
# 設置為暗模式
# 自訂暗模式樣式
dark_mode_css = """
<style>
:root {
    --primary-color: #1DB954; /* 主色 */
    --background-color: #121212; /* 背景色 */
    --secondary-background-color: #1E1E1E; /* 側邊欄背景色 */
    --text-color: #FFFFFF; /* 文字顏色 */
}
body {
    background-color: var(--background-color);
    color: var(--text-color);
}
</style>
"""

st.markdown(dark_mode_css, unsafe_allow_html=True)
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


# Customize the sidebar
markdown = """
資料來源：BWF世界羽球聯盟
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/2012_BWF_logo.svg/1200px-2012_BWF_logo.svg.png"
st.sidebar.image(logo)

# Customize page title
st.title("BWF世界羽球聯盟排名資料視覺化與互動地圖")

st.markdown(
    """
    內建爬蟲程式，抓取BWF世界羽聯網頁(https://bwf.tournamentsoftware.com/ranking/) \n
    可查詢的最早的排名紀錄開始，至今所有週次的世界排名資料，取前100名 \n
    此專案提供單項的排名資料視覺化、互動地圖呈現，並且可選擇與其他週次比較\n
    另外也提供特定選手(組別)的搜尋與比較   \n
    由於BWF的排名紀錄網頁顯示日期的格式是 ：月/日/年 (m/d/y)，因此以下顯示也依此格式   \n
    此程式ChatGPT出了90%力，感謝哆啦GPT夢    
    """
)

st.header("請根據左側其他分頁選擇欲查詢的單項")

markdown = """


"""

st.markdown(markdown)


