import geopandas as gpd
import leafmap

# 创建两个简单的 GeoDataFrame
data1 = {'geometry': ['POINT (0 0)', 'POINT (1 1)', 'POINT (2 2)']}
gdf1 = gpd.GeoDataFrame(data1, geometry='geometry')
gdf1.set_crs("EPSG:4326", inplace=True)

data2 = {'geometry': ['POINT (0 1)', 'POINT (1 2)', 'POINT (2 3)']}
gdf2 = gpd.GeoDataFrame(data2, geometry='geometry')
gdf2.set_crs("EPSG:4326", inplace=True)

# 创建地图
m = leafmap.Map()

# 尝试分割地图
try:
    m.split_map(gdf1, gdf2, left_layer_name="Layer 1", right_layer_name="Layer 2")
    m.to_streamlit(height=700)

except Exception as e:
    print(f"Error: {e}")
