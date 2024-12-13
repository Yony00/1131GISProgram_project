import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

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
    內建爬蟲程式，抓取BWF世界羽聯有紀錄開始至今所有週次的世界排名資料，取前100名 \n
    此專案提供單項的排名資料視覺化、互動地圖呈現，並且可選擇與其他週次比較\n
    由於BWF的排名紀錄網頁顯示日期的格式是 ：月/日/年 (m/d/y)，因此以下顯示也依此格式   \n
    此程式ChatGPT出了90%力，感謝哆啦GPT夢    
    """
)

st.header("請根據左側其他分頁選擇欲查詢的單項")

markdown = """


"""

st.markdown(markdown)


