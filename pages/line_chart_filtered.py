
import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta

st.set_page_config(page_title = "Traffic volume over time")
st.markdown("# Bike volume over time")

bikes_agg = pd.read_csv('bikes_agg.csv')
bikes_agg['date'] = pd.to_datetime(bikes_agg['date'])

time_slider = st.slider(
    label = 'Select a timeframe',
    min_value = datetime.date(2020,6,25),
    max_value = datetime.date(2022,6,25),
    value = (datetime.date(2021,4,25),datetime.date(2021,8,25)),
    step = timedelta(days = 14)
    )

bikes_plot = bikes_agg.loc[time_slider[0]:time_slider[1]]
st.line_chart(data = bikes_plot)