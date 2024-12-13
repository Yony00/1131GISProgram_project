import folium
from streamlit_folium import st_folium
import streamlit as st

# 創建第一個地圖 m1
m1 = folium.Map(location=[0, 0], zoom_start=5, control_scale=True)  # 使用控制縮放和比例尺
folium.TileLayer('Stamen Terrain').add_to(m1)  # 使用不同的底圖 'Stamen Terrain'

# 創建第二個地圖 m2
m2 = folium.Map(location=[0, 0], zoom_start=5, control_scale=True)  # 使用控制縮放和比例尺
folium.TileLayer('Stamen Toner').add_to(m2)  # 使用不同的底圖 'Stamen Toner'

# 使用 Streamlit 展示地圖
row1, row2 = st.columns(2)

with row1:
    output1 = st_folium(m1, width=400, height=300, key="map1")

with row2:
    output2 = st_folium(m2, width=400, height=300, key="map2")

    # 設定同步移動和縮放
    st.script_runner.heartbeat()
    st.session_state.map_center = output1["center"]
    st.session_state.map_zoom = output1["zoom"]

    def sync_map(event):
        # 根據另一個地圖的中心位置更新 m2 的中心和縮放級別
        m2.location = st.session_state.map_center
        m2.zoom_start = st.session_state.map_zoom

    st.session_state.sync_map = sync_map

