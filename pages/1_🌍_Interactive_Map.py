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
from leafmap.foliumap import st_map, st_map_bounds
import folium

# 建立 Folium 地圖
m = folium.Map(location=[20, 0], zoom_start=2)

# 在 Streamlit 中顯示地圖
st_map(m)

# 檢測地圖邊界
bounds = st_map_bounds()
if bounds:
    st.write("當前地圖邊界範圍為：")
    st.write(bounds)
