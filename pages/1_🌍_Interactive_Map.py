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



# 建立地圖
m=leafmap.Map(center=[40, -100], zoom=4)
 m.to_streamlit(height=700)
# 獲取地圖的顯示邊界
bounds = m.st_map_bounds(st)

# 顯示地圖和邊界
st.write("地圖範圍:", bounds)

