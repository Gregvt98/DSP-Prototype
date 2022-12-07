
import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta

st.set_page_config(page_title = "Traffic volume over time")
st.markdown("# Bike volume over time")

bikes = pd.read_csv('strava_data.csv')[
    ['edge_uid','date','forward_commute_trip_count','reverse_commute_trip_count','osm_reference_id']]
bikes['total_commute'] = bikes['forward_commute_trip_count'] + bikes['reverse_commute_trip_count']
bikes['date'] = pd.to_datetime(bikes['date'])

time_slider = st.slider(
    label = 'Select a timeframe',
    min_value = datetime.date(2020,6,25),
    max_value = datetime.date(2022,6,25),
    value = (datetime.date(2021,4,25),datetime.date(2021,8,25)),
    step = timedelta(days = 14)
    )

bikes_agg = bikes.groupby('date').agg({'total_commute':'sum'}).loc[time_slider[0]:time_slider[1]]
st.line_chart(data = bikes_agg)
