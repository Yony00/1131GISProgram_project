import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import folium
from math import radians, sin, cos, sqrt, atan2
st.set_page_config(layout="wide")

st.title("📍尋找5公里內餐廳")

# 假設餐廳的 GeoJSON 檔案 URL
restaurant_geojson_url = 'https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson'
restaurants = gpd.read_file(restaurant_geojson_url)

# 確保資料包含經緯度列
restaurants['經度'] = restaurants.geometry.x
restaurants['緯度'] = restaurants.geometry.y

# 使用者輸入的經緯度
col1, col2 = st.columns(2)
with col1:
    lon = st.number_input("請填入經度", value=None, min_value=119.500, max_value=122.500)
with col2:
    lat = st.number_input("請填入緯度", value=None, min_value=22.000, max_value=24.000)

if lat is not None and lon is not None:
    radius = 5000  # 範圍為 5 公里
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # 地球半徑（公尺）
        phi1, phi2 = radians(lat1), radians(lat2)
        delta_phi = radians(lat2 - lat1)
        delta_lambda = radians(lon2 - lon1)
        a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
    
    # 計算每個餐廳與輸入位置的距離
    restaurants['距離(m)'] = restaurants.apply(
        lambda row: haversine(lat, lon, row['緯度'], row['經度']), axis=1
    )
    
    # 篩選出在 5 公里範圍內的餐廳
    nearby_restaurants = restaurants[restaurants['距離(m)'] <= radius]

    # 顯示地圖
    m = leafmap.Map(center=[lat, lon], zoom=12)
    
    # 顯示使用者位置
    folium.Marker(
        location=[lat, lon],
        popup=f"使用者位置\n經度: {lon}, 緯度: {lat}",
        icon=folium.Icon(color='blue', icon='star')
    ).add_to(m)

    # 顯示範圍
    folium.Circle(
        location=[lat, lon],
        radius=radius,
        color="cornflowerblue",
        fill=True,
        fill_opacity=0.6,
        opacity=1,
        popup="{} meters".format(radius)
    ).add_to(m)

    # 顯示範圍內的餐廳
    for _, row in nearby_restaurants.iterrows():
        folium.Marker(
            location=[row['緯度'], row['經度']],
            popup=f"{row['餐廳名稱']}\n距離: {row['距離(m)']:.2f} 米",
            icon=folium.Icon(color='green', icon='cutlery')
        ).add_to(m)

    # 顯示地圖
    m.to_streamlit(height=600)

    # 顯示範圍內的餐廳資料
    st.write("範圍內的餐廳：")
    st.table(nearby_restaurants[['餐廳名稱', '地址', '經度', '緯度', '距離(m)']])
else:
    st.write("請填入有效的經緯度")
