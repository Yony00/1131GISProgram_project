import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Marker Cluster")

with st.expander("See source code"):
    with st.echo():

        m = leafmap.Map(center=[40, -100], zoom=4)
        cities = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"
        MS="https://raw.githubusercontent.com/RGT1143022/datafor1127/main/MSwithGEO10.geojson"

       # m.add_geojson(regions, layer_name="US Regions")
        m.add_geojson(MS, layer_name="Man Single Player Count")

        #m.add_points_from_xy(
        #    cities,
        #    x="longitude",
        #    y="latitude",
        #    color_column="region",
        #    icon_names=["gear", "map", "leaf", "globe"],
        #    spin=True,
        #    add_legend=True,
        #)

m.to_streamlit(height=700)
