import streamlit as st
import folium
import geopandas as gpd
import requests
import pandas as pd  # 加入 pandas 模組
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# 設定頁面標題
st.title("發現鄰近美味！速食餐廳互動式地圖")

# 定義速食餐廳選項
restaurant_choices = ["全部", "麥當勞", "肯德基", "SUBWAY"]
restaurant_selection = st.selectbox("選擇速食餐廳", restaurant_choices)

# 定義 GeoJSON 檔案的 URL
geojson_urls = {
    "SUBWAY": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/SB10.geojson",
    "肯德基": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/KK10.geojson",
    "麥當勞": "https://raw.githubusercontent.com/Yony00/20241127-class/refs/heads/main/MM10.geojson"
}

# 下載和讀取每個 GeoJSON 檔案
geo_dfs = {}
for name, url in geojson_urls.items():
    response = requests.get(url)
    if response.status_code == 200:
        gdf = gpd.read_file(response.text)
        gdf["brand"] = name  # 如果 brand 欄位不存在，填入對應的品牌
        geo_dfs[name] = gdf
    else:
        st.error(f"無法下載 GeoJSON 檔案: {name}")

# 根據選擇合併資料
if restaurant_selection == "全部":
    combined_gdf = gpd.GeoDataFrame(pd.concat(geo_dfs.values(), ignore_index=True))
else:
    combined_gdf = geo_dfs.get(restaurant_selection)

# 如果有有效資料，繪製地圖
if combined_gdf is not None and not combined_gdf.empty:
    # 初始化地圖，將地圖中心設置為指定的座標
    m = folium.Map(location=[23.6, 121], zoom_start=8)

    # 自定義圖標
    icons = {
        "SUBWAY": "https://raw.githubusercontent.com/Yony00/1131GISProgram_project/refs/heads/main/cookie.png",  # SUBWAY 預設圖標
        "肯德基": "https://raw.githubusercontent.com/Yony00/1131GISProgram_project/refs/heads/main/fried-chicken.png",  # 肯德基炸雞圖標
        "麥當勞": "https://raw.githubusercontent.com/Yony00/1131GISProgram_project/refs/heads/main/french-fires.png"   # 麥當勞薯條圖標
    }

    # 當 brand 未定義時，顯示三間速食餐廳的圖標
    if 'brand' not in combined_gdf.columns:
        # 顯示所有品牌的點位
        for brand, gdf in geo_dfs.items():
            for idx, row in gdf.iterrows():
                lat, lon = row.geometry.y, row.geometry.x
                icon_url = icons.get(brand, icons["SUBWAY"])  # 根據品牌選擇對應圖標
                custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 30))

                # 使用 HTML 格式來顯示 popup 內容
                popup_content = f"""
                <strong>分店:</strong> {row['name'] if 'name' in row else 'Unknown'}<br>
                <strong>電話:</strong> {row['number'] if 'number' in row else 'Not Available'}<br>
                <strong>地址:</strong> {row['address'] if 'address' in row else 'Not Available'}<br>
                <strong>營業時間:</strong> {row['hours'] if 'hours' in row else 'Not Available'}<br>
                """

                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_content, max_width=300),
                    icon=custom_icon
                ).add_to(m)

    else:
        # 如果有 brand 欄位，根據選擇顯示指定品牌的圖標
        for idx, row in combined_gdf.iterrows():
            lat, lon = row.geometry.y, row.geometry.x
            brand = row.get("brand", "SUBWAY")  # 預設 brand 如果未定義，填入 SUBWAY
            icon_url = icons.get(brand, icons["SUBWAY"])  # 根據品牌選擇對應圖標
            custom_icon = folium.CustomIcon(icon_url, icon_size=(30, 30))

            # 使用 HTML 格式來顯示 popup 內容
            popup_content = f"""
            <strong>分店:</strong> {row['name'] if 'name' in row else 'Unknown'}<br>
            <strong>電話:</strong> {row['number'] if 'number' in row else 'Not Available'}<br>
            <strong>地址:</strong> {row['address'] if 'address' in row else 'Not Available'}<br>
            <strong>營業時間:</strong> {row['hours'] if 'hours' in row else 'Not Available'}<br>
            """

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                icon=custom_icon
            ).add_to(m)

    # 顯示地圖
    st_folium(m, width=1800, height=800)

    # 顯示目前的餐廳分店列表
    if 'name' in combined_gdf.columns:
        st.write(f"{restaurant_selection} 餐廳分布:")
        st.write(combined_gdf[['name', 'number', 'address', 'hours']])
else:
    st.error(f"無法載入 {restaurant_selection} 的分布資料。")
