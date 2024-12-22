import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import requests
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(layout="wide")
st.title("📍尋找3公里內的Subway餐廳")

# 假設餐廳的 GeoJSON 檔案 URL
subway_geojson_url = 'https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson'

# 下載 GeoJSON 檔案
response = requests.get(subway_geojson_url)
if response.status_code == 200:
    subway_gdf = gpd.read_file(response.text)
else:
    subway_gdf = None

# 上方地圖：使用者點選位置
st.subheader("選擇位置")
m = folium.Map(location=[23.6, 121], zoom_start=9)

# 在地圖上顯示使用者點選位置
clicked_point = st_folium(m, key="folium_map", width=1000, height=1000)

# 計算距離的haversine函數
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # 地球半徑（公尺）
    phi1, phi2 = radians(lat1), radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 下方顯示範圍和餐廳資料
if clicked_point and clicked_point.get("last_clicked"):
    lat = clicked_point["last_clicked"]["lat"]
    lon = clicked_point["last_clicked"]["lng"]
    st.success(f"您選擇的位置：經度 {lon}, 緯度 {lat}")

    # 範圍半徑為 3 公里
    radius = 3000  # 3 公里

    # 顯示下方地圖，顯示選擇的位置和範圍
    m2 = folium.Map(location=[lat, lon], zoom_start=14)
    
    # 顯示選擇位置的標記
    folium.Marker(location=[lat, lon], popup=f"選擇位置\n經度: {lon}, 緯度: {lat}",
                  icon=folium.Icon(color='blue', icon='star')).add_to(m2)

    # 顯示範圍
    folium.Circle(location=[lat, lon], radius=radius, color="cornflowerblue", fill=True, fill_opacity=0.6).add_to(m2)

    # 篩選範圍內的餐廳
    if subway_gdf is not None:
        # 計算每個餐廳與選擇位置的距離
        subway_gdf['距離(m)'] = subway_gdf.apply(
            lambda row: haversine(lat, lon, row.geometry.y, row.geometry.x), axis=1
        )

        # 篩選出範圍內的餐廳
        nearby_restaurants = subway_gdf[subway_gdf['距離(m)'] <= radius]

        if nearby_restaurants.empty:
            folium.Marker(location=[lat, lon], popup="範圍內無餐廳", icon=folium.Icon(color='red')).add_to(m2)
        else:
            # 顯示範圍內的餐廳
            for _, row in nearby_restaurants.iterrows():
                folium.Marker(
                    location=[row.geometry.y, row.geometry.x],
                    popup=f"{row['name']}\n距離: {row['距離(m)']:.2f} 米",
                    icon=folium.Icon(color='green', icon='cutlery')
                ).add_to(m2)

    st_folium(m2, key="updated_map", width=1000, height=1000)
    

    # 顯示範圍內的餐廳資料
    if not nearby_restaurants.empty:
        st.write("範圍內的Subway餐廳：")
        st.table(nearby_restaurants[['name', 'address', 'hours', 'number']])
    else:
        st.write("範圍內無餐廳")
else:
    st.info("請在上方地圖上點選一個位置")
