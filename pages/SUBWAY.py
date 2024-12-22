import streamlit as st
from streamlit_folium import st_folium
import folium
import geopandas as gpd
import requests
from shapely.geometry import Point

# 設定頁面標題
st.title("Interactive Map with Buffer Area")

# 初始化地圖
m = folium.Map(location=[23.6, 121], zoom_start=8)

# 使用者點擊地圖時更新座標並顯示環域
clicked_point = st_folium(m, key="folium_map")

# 檢查是否有點擊
if clicked_point and clicked_point.get("last_clicked"):
    lat = clicked_point["last_clicked"]["lat"]
    lon = clicked_point["last_clicked"]["lng"]

    # 將點擊的座標顯示給使用者
    st.success(f"You clicked at Latitude: {lat}, Longitude: {lon}")

    # 建立新地圖，將環域添加到地圖上
    m = folium.Map(location=[lat, lon], zoom_start=14)

    # 添加環域到地圖上（半徑為 3 公里 = 3000 米）
    folium.Circle(
        location=(lat, lon),
        radius=3000,  # 3 公里
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.2
    ).add_to(m)

    # 添加一個標記到點擊的位置
    folium.Marker(location=(lat, lon), popup="Selected Point").add_to(m)

    # 顯示更新後的地圖
    st_folium(m, key="updated_map", width=700)

    # 顯示 SUBWAY 餐廳地圖
    st.title("SUBWAY Restaurants within 3km")

    # 下載 GitHub 上的 GeoJSON 檔案
    geojson_url = "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson"

    # 使用 requests 下載 GeoJSON 檔案
    response = requests.get(geojson_url)

    if response.status_code == 200:
        # 將下載的資料轉換為 GeoJSON 格式
        gdf = gpd.read_file(response.text)

        # 將資料轉換為點資料格式
        gdf['geometry'] = gdf['geometry'].apply(lambda x: Point(x))

        # 建立中心點的地理範圍，3 公里圓形範圍
        point = Point(lon, lat)
        buffer_area = point.buffer(3000)  # 半徑 3 公里

        # 篩選出在該範圍內的 SUBWAY 餐廳
        subway_within_buffer = gdf[gdf.geometry.within(buffer_area)]

        # 初始化地圖，將地圖中心設置為第一個餐廳的位置
        first_location = subway_within_buffer.geometry.iloc[0].coords[0]
        m = folium.Map(location=[first_location[1], first_location[0]], zoom_start=12)

        # 在地圖上標註出這些 SUBWAY 餐廳
        for idx, row in subway_within_buffer.iterrows():
            folium.Marker(
                location=[row.geometry.y, row.geometry.x],
                popup=row['name']
            ).add_to(m)

        # 顯示更新後的地圖
        st_folium(m, key="subway_map", width=700)

        # 顯示餐廳列表
        st.write("SUBWAY Locations within 3km:")
        st.write(subway_within_buffer[['name', 'address']])
    else:
        st.error("Failed to download GeoJSON file from GitHub.")

else:
    st.info("Click on the map to generate a 3 km buffer area.")
