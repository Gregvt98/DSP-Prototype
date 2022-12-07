import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Dataframe Demo", page_icon="📊")

st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)


@st.cache
def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


try:
    uitchecks = pd.read_csv('gvb_uitchecks_171022.csv')
    uitchecks = uitchecks.set_index('AankomstHalteNaam').dropna().loc[:,['AankomstLat', 'AankomstLon', 'AantalReizen', 'UurgroepOmschrijving (van aankomst)']]
    df = get_UN_data()

    stops = st.multiselect(
        "Choose transport stops", list(uitchecks.index.unique()), ["Centraal Station"]
    )
    if not stops:
        st.error("Please select at least one country.")
    else:
        data = uitchecks.loc[stops].groupby("UurgroepOmschrijving (van aankomst)").aggregate(sum)['AantalReizen']
        
        st.write("### Checkout amounts for selected stops per hour", data.sort_index())
        data = data.T.reset_index()
        # data = pd.melt(data, id_vars=["index"]).rename(
        #     columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        # )
        print(data)
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="UurGroepOmschrijving (van aankomst):T",
                y=alt.Y("AantalReizen:Q", stack=None),
                # color="AantalReizen:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )