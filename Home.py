import streamlit as st
import leafmap.foliumap as leafmap
st.set_page_config(page_title="BWF World Ranking", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://github.com/RGT1143022/BWF_world_country/releases/download/v1.0.1/background.png'); /* 指定背景圖像的URL或路徑 */
        background-size: cover;  /* 讓背景圖像填滿整個視窗 */
        background-position: center;  /* 背景圖像居中 */
        filter: brightness(50%);  /* 使圖片亮度降低到 50% */
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
    由於BWF的排名紀錄網頁顯示日期的格式是 ：月/日/年 (m/d/y)，因此以下顯示也依此格式   \n
    此程式ChatGPT出了90%力，感謝哆啦GPT夢    
    """
)

st.header("請根據左側其他分頁選擇欲查詢的單項")

markdown = """


"""

st.markdown(markdown)


