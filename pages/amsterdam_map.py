import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.markdown("# Amsterdam Map")
st.sidebar.header("Map of Amsterdam")
st.write(
    """This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)


@st.experimental_memo
def from_data_file(filename):
    url = (
        "http://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename
    )
    return pd.read_json(url)


try:
    
    bikes = from_data_file("bike_rental_stats.json")
    print(bikes)
    uitchecks = pd.read_csv('gvb_uitchecks_171022.csv')
    uitchecks = uitchecks.set_index('AankomstHalteNaam').dropna().loc[:,['AankomstLat', 'AankomstLon']]
    uitchecks = uitchecks[9:]
    uitchecks['lon'] = uitchecks['AankomstLat']
    uitchecks['lat'] = uitchecks['AankomstLon']

    print(uitchecks)

    ALL_LAYERS = {
        "Public Transport": pdk.Layer(
            "HexagonLayer",
            data=uitchecks,
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
            
        )

    }
    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 52.2,
                    "longitude": 4.8,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )