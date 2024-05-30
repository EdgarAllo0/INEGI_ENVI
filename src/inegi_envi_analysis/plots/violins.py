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
def ViolinPlot(
        df: pd.DataFrame | None,
        column1: str,
        column2: str,
):
    palette = list(sns.color_palette("Spectral", 50).as_hex())

    # Customize letter size
    letter_size = 15

    # Category dict
    cat_dict = {
        0: 'Negative Late Payment Category',
        1: 'Positive Late Payment Category'
    }

    # Conditions for plotting
    condition_1 = (
            df is None or
            df.empty
    )

    # If all data is available
    if not condition_1:

        fig = make_subplots()

        for i in [0, 1]:
            fig.add_trace(
                go.Violin(
                    x=df[column1][df[column1] == i],
                    y=df[column2][df[column1] == i],
                    name=cat_dict[i],
                    box_visible=False,
                    meanline_visible=True,
                    line_color=random.choice(palette)
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

        title = {column2.replace('_', ' ').title()}
        fig.update_layout(
            title=f'{title} Violin Plots',
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
