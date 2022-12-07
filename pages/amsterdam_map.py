import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Amsterdam Map", page_icon="🌍")

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
    
    uitchecks = pd.read_csv('gvb_uitchecks_171022.csv')
    uitchecks = uitchecks.set_index('AankomstHalteNaam').dropna().loc[:,['AankomstLat', 'AankomstLon', 'AantalReizen', 'UurgroepOmschrijving (van aankomst)']]
    uitchecks_per_hour = uitchecks.copy()
    uitchecks_summed = uitchecks.groupby('AankomstHalteNaam').aggregate(sum)

    uitchecks['lon'] = uitchecks['AankomstLat']
    uitchecks['lat'] = uitchecks['AankomstLon']

    sum_dict = dict(zip(uitchecks_summed.index, uitchecks_summed['AantalReizen']))
    uitchecks['total_journeys'] = [sum_dict[i] for i in uitchecks.index]
    uitchecks = uitchecks[~uitchecks.index.duplicated(keep='first')]
    # print(uitchecks)
    print(uitchecks_per_hour)
    

    ALL_LAYERS = {
        "Public Transport": pdk.Layer(
            "HexagonLayer",
            data=uitchecks,
            get_position=["lon", "lat"],
            radius=50,
            elevation_scale=2,
            elevation_range=[0, 1000],
            extruded=True,
            
        ),
        "Circle Map": pdk.Layer(
            "ScatterplotLayer",
            data=uitchecks,
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[total_journeys]",
            radius_scale=0.04,
        ),
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
                    "latitude": 52.37,
                    "longitude": 4.93,
                    "zoom": 13,
                    "pitch": 30,
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