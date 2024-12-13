import leafmap.foliumap as leafmap
import streamlit as st

# 創建地圖
m = leafmap.Map(center=(0, 0), zoom=2)

# 定義一個函數來同步地圖中心到 Streamlit session state
def sync_map(event):
    st.session_state.map_center = event["center"]

# 顯示地圖並將 `m` 傳遞給 `m.to_streamlit()` 用來監聽移動事件
m.to_streamlit()

# 初始化 session state 的地圖中心
if "map_center" not in st.session_state:
    st.session_state.map_center = m.center

# 顯示當前地圖中心
st.write(f"Current center: {st.session_state.map_center}")
