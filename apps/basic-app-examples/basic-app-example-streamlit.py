# in terminal:  streamlit run basic-app-example-streamlit.py

import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("https://raw.githubusercontent.com/tidyverse/dplyr/master/data-raw/starwars.csv")

var = st.selectbox(                                 # UI Input
    "Select variable:",
    ["mass", "height"],
    index=0
)

fig = px.histogram(                                 # Output computation 
    df,
    x=var,
    title=f"Histogram of {var}"
)

st.plotly_chart(fig, use_container_width=True)      # UI Output
