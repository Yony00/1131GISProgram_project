import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("BWF世界羽球聯盟排名資料視覺化與互動地圖")

st.markdown(
    """
    內建爬蟲程式，抓取BWF世界羽聯有紀錄開始至今所有週次的世界排名資料，取前100名 \n
    此專案提供單項的排名資料視覺化、互動地圖呈現，並且可選擇與其他週次比較\n
    此程式ChatGPT出了90%力，感謝哆啦GPT夢    
    """
)

st.header("    內建爬蟲程式，抓取BWF世界羽聯有紀錄開始至今所有週次的世界排名資料，取前100名 \n
    此專案提供單項的排名資料視覺化、互動地圖呈現，並且可選擇與其他週次比較\n
    此程式ChatGPT出了90%力，感謝哆啦GPT夢    ")

markdown = """
7777777
1. For the [GitHub repository](https://github.com/opengeos/streamlit-map-template) or [use it as a template](https://github.com/opengeos/streamlit-map-template/generate) for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python files.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)


