import folium
import streamlit as st

# 創建地圖
m = folium.Map(location=[0, 0], zoom_start=2)

# 定義一個回調函數來同步地圖中心和縮放級別到 Streamlit session state
def sync_map(event, m):
    st.session_state.map_center = m.get_center()
    st.session_state.map_zoom = m.get_zoom()

# 將回調函數綁定到地圖的動作事件
m.on("moveend", sync_map, m)

# 在 Streamlit 中顯示地圖
output = st_folium(m, width=700, height=500, key="map1")

# 更新 `session_state` 的地圖參數
if "map_center" not in st.session_state:
    st.session_state.map_center = m.get_center()
    st.session_state.map_zoom = m.get_zoom()

# 顯示當前地圖中心和縮放級別
st.write(f"Current center: {st.session_state.map_center}, Zoom level: {st.session_state.map_zoom}")
