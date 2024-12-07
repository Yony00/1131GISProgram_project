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

# 创建一个 Leafmap 映射组件
m = leafmap.Map(locate_control=True)

# 显示地图
m.to_streamlit()

# 获取当前视角边界框
def get_bounds(m):
    bounds = m.get_bounds()  # 获取视角边界
    if bounds:  # 如果 bounds 不为 None
        south, west, north, east = bounds
        return {
            'south': south,
            'west': west,
            'north': north,
            'east': east
        }
    else:
        return None

# 显示当前视角的边界框
bounds = get_bounds(m)
if bounds:
    st.write(f"南边界: {bounds['south']}, 北边界: {bounds['north']}, 西边界: {bounds['west']}, 东边界: {bounds['east']}")
else:
    st.write("无法获取地图的视角边界")


