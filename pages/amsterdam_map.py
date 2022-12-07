import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Amsterdam Map", page_icon="🌍")

st.markdown("# Amsterdam Map")
st.sidebar.header("Map of Amsterdam")
st.write(
    """This page shows different visualisations for selected modalities 
    of a selected region in Amsterdam. For public transport, the 
    circles represent stops and the size of the circle represents the amount of
    passengers checking out at this stop"""
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
    uitchecks = uitchecks.loc[uitchecks["lon"] < 4.98]
    uitchecks = uitchecks.loc[uitchecks["lon"] > 4.92]
    uitchecks = uitchecks.loc[uitchecks["lat"] < 52.4]
    uitchecks = uitchecks.loc[uitchecks["lat"] > 52.35]


    print(uitchecks)
    print(uitchecks_per_hour)
    

    ALL_LAYERS = {
        "Public transport density": pdk.Layer(
            "ScatterplotLayer",
            data=uitchecks,
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[total_journeys]",
            radius_scale=0.08,
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