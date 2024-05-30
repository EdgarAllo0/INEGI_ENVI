# StreamLit
import streamlit as st

# Data
import pandas as pd
import seaborn as sns

# Plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@st.cache_resource
def EmptyPlot():

    fig = go.Figure()

    fig.update_layout(
        height=700
        )

    fig.update_layout(
        title="No Available Information for this Variable"
        )

    return fig