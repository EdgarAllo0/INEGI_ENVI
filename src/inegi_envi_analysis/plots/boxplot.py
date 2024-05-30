# Data Handlers
import streamlit as st
import pandas as pd
import seaborn as sns
import random

# Plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Modules
from src.inegi_envi_analysis.plots.standard_plots import EmptyPlot


@st.cache_resource
def BoxPlot(
        variable_1: pd.Series,
        variable_2: pd.Series,
):
    palette = list(sns.color_palette("Spectral", 50).as_hex())

    # Customize letter size
    letter_size = 15

    # Conditions for plotting
    condition_1 = (
            variable_1 is None or
            variable_1.empty or
            variable_1.isnull().all()
    )

    condition_2 = (
            variable_2 is None or
            variable_2.empty or
            variable_2.isnull().all()
    )

    # If all data is available
    if not condition_1 and not condition_2:

        fig = make_subplots()

        fig.add_trace(
            go.Box(
                y=variable_1,
                name='Negative Late Payment Category',
                marker_color=random.choice(palette)
            )
        )

        fig.add_trace(
            go.Box(
                y=variable_2,
                name='Positive Late Payment Category',
                marker_color=random.choice(palette)
            )
        )

        fig.update_xaxes(
            title_text='Late Payment Class',
            title_font=dict(size=letter_size),
        )

        fig.update_yaxes(
            title_text="Values",
            title_font=dict(size=letter_size),
        )

        title = str(variable_1.name).replace('_', ' ').title()
        fig.update_layout(
            title=f'{title} Box Plots',
        )

        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                xanchor="center",
                y=1.0,
                x=0.5,
                font=dict(
                    size=letter_size,
                    color="black"
                )
            )
        )

        fig.update_layout(
            height=600
        )

    else:

        fig = EmptyPlot()

        st.warning('There was an error with Series Data...', icon="⚠️")

    return fig
