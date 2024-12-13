import folium
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium

# 創建第一個地圖 m1
m1 = folium.Map(location=[0, 0], zoom_start=1)  # 設定初始中心點和縮放級別
folium.Marker([25, 120], popup='Point 1').add_to(m1)  # 在地圖上添加點物件

# 創建第二個地圖 m2
m2 = folium.Map(location=[0, 0], zoom_start=1)  # 設定初始中心點和縮放級別
folium.Marker([24, 120], popup='Point 2').add_to(m2)  # 在地圖上添加點物件

# 使用 st_folium 在 Streamlit 中顯示地圖
import streamlit as st

row1, row2 = st.columns(2)

with row1:
    output1 = st_folium(m1, width=400, height=300, key="map1")

with row2:
    output2 = st_folium(m2, width=400, height=300, key="map2")
