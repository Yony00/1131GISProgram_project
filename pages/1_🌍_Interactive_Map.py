import streamlit as st
import leafmap.foliumap as leafmap

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:

    basemap = st.selectbox("Select a basemap:", options, index)


with col1:

    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )
    m.add_basemap(basemap)
    m.to_streamlit(height=700)


import streamlit as st
import leafmap.foliumap as leafmap

# 创建交互式地图
m = leafmap.Map(
    locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
)
m.add_basemap("OpenTopoMap")

# 显示地图
m.to_streamlit(height=700)

# 获取和显示当前缩放级别
def display_zoom(m):
    st.write(f"当前缩放级别: {m.zoom}")

# 为地图添加缩放事件监听
m.on_zoom_changed(lambda e: display_zoom(m))  # Ensure m is correctly passed to the lambda function

