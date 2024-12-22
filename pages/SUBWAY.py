import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import requests
from math import radians, sin, cos, sqrt, atan2

st.set_page_config(layout="wide")
st.title("📍尋找自訂範圍內的Subway餐廳")

st.markdown(
    """
    內建爬蟲程式，抓取BWF世界羽聯網頁(https://bwf.tournamentsoftware.com/ranking/) \n
    可查詢的最早的排名紀錄開始，至今所有週次的世界排名資料，取前100名 \n
    此專案提供單項的排名資料視覺化、互動地圖呈現，並且可選擇與其他週次比較\n
    另外也提供特定選手(組別)的搜尋與比較   \n
    由於BWF的排名紀錄網頁顯示日期的格式是 ：月/日/年 (m/d/y)，因此以下顯示也依此格式   \n
    此程式ChatGPT出了90%力，感謝哆啦GPT夢    
    """
)

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
col1, col2 = st.columns([3, 2])  # 設定比例，3:2的比例

with col1:
    m = folium.Map(location=[23.6, 121], zoom_start=8)

    # 在地圖上顯示使用者點選位置
    clicked_point = st_folium(m, key="folium_map", width=750, height=600)

# 計算距離的haversine函數
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # 地球半徑（公尺）
    phi1, phi2 = radians(lat1), radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)
    a = sin(delta_phi / 2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 讓使用者自訂範圍半徑
radius = st.slider(
    "選擇範圍半徑 (公尺)",
    min_value=0,  # 最小範圍0公尺
    max_value=10000,  # 最大範圍10000公尺
    value=3000,  # 預設值3000公尺
    step=1,  # 步長為500公尺
)

# 下方顯示範圍和餐廳資料
if clicked_point and clicked_point.get("last_clicked"):
    lat = clicked_point["last_clicked"]["lat"]
    lon = clicked_point["last_clicked"]["lng"]
    st.success(f"您選擇的位置：經度 {lon}, 緯度 {lat}，範圍半徑 {radius} 公尺")

    # 顯示下方地圖，顯示選擇的位置和範圍
    with col2:
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
                # 找到距離最近的餐廳
                closest_restaurant = nearby_restaurants.loc[nearby_restaurants['距離(m)'].idxmin()]

                # 顯示範圍內的餐廳
                for _, row in nearby_restaurants.iterrows():
                    if row['name'] == closest_restaurant['name']:
                        # 使用不同的顏色標示最近的餐廳
                        folium.Marker(
                            location=[row.geometry.y, row.geometry.x],
                            popup=f"{row['name']} (最近)\n距離: {row['距離(m)']:.2f} 米",
                            icon=folium.Icon(color='red', icon='cutlery')
                        ).add_to(m2)
                    else:
                        folium.Marker(
                            location=[row.geometry.y, row.geometry.x],
                            popup=f"{row['name']}\n距離: {row['距離(m)']:.2f} 米",
                            icon=folium.Icon(color='green', icon='cutlery')
                        ).add_to(m2)

        # 添加圖例
        legend_html = """
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 250px; height: 150px; 
                    background-color: white; opacity: 0.8; z-index:9999; font-size:14px; 
                    border-radius: 10px; padding: 10px;">
            <b>圖例</b><br>
            <i style="background:blue; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></i> 您的位置<br>
            <i style="background:cornflowerblue; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></i> 範圍內的餐廳<br>
            <i style="background:red; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></i> 最近的餐廳<br>
            <i style="background:green; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></i> 其他餐廳
        </div>
        """
        # 把圖例HTML加入到folium地圖
        m2.get_root().html.add_child(folium.Element(legend_html))

        st_folium(m2, key="updated_map", width=750, height=600)

        # 顯示範圍內的餐廳資料
        if not nearby_restaurants.empty:
            st.write("範圍內的Subway餐廳：")
            st.table(nearby_restaurants[['name', 'address', 'hours', 'number']])
        else:
            st.write("範圍內無餐廳")
else:
    st.info("請在上方地圖上點選一個位置")
