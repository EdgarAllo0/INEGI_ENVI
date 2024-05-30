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
def StackedHistogramPlot(
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
            go.Histogram(
                x=variable_1,
                histnorm='probability',
                name='PDF (Negative Late Payment Category)',
                marker=dict(
                    color=random.choice(palette)  # Replace with your desired color
                )
            )
        )

        fig.add_trace(
            go.Histogram(
                x=variable_2,
                histnorm='probability',
                name='PDF (Positive Late Payment Category)',
                opacity=0.2,
                marker=dict(
                    color=random.choice(palette)  # Replace with your desired color
                )
            )
        )

        fig.update_layout(
            barmode='overlay',
        )

        fig.update_xaxes(
            title_text='Values',
            title_font=dict(size=letter_size),
        )

        fig.update_yaxes(
            title_text="Frequency",
            title_font=dict(size=letter_size),
        )

        title = str(variable_1.name).replace('_', ' ').title()
        fig.update_layout(
            title=f'{title} Stacked Histogram',
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
