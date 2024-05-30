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
def HistogramPlot(
    data: pd.Series
):
    # Set colors
    color_1 = '#000000'
    color_2 = '#2C2C2C'
    palette = list(sns.color_palette("Spectral", 10).as_hex())

    # Customize letter size
    letter_size = 15

    # Conditions for plotting
    condition_1 = (
            data is None or
            data.empty or
            data.isnull().all()
    )

    # If there is no available data
    if condition_1:

        fig = EmptyPlot()

        st.warning('There was an error with Series Data...', icon="⚠️")

    # If data is available
    elif not condition_1:

        fig = make_subplots()

        fig.add_trace(
            go.Histogram(
                x=data,
                histnorm='probability',
                name='PDF',
                marker=dict(
                    color=random.choice(palette)  # Replace with your desired color
                )
            )
        )

        # Mean
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=data.mean(),
                y0=0,
                x1=data.mean(),
                y1=1,
                xref="x",
                yref="paper",
                line=dict(
                    color=color_1,
                    width=2,
                    dash="dash"
                ),
                name='Mean'
            )
        )

        # Median
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=data.median(),
                y0=0,
                x1=data.median(),
                y1=1,
                xref="x",
                yref="paper",
                line=dict(
                    color=color_2,
                    width=2,
                    dash="dash"
                ),
                name='Median'
            )
        )

        fig.update_xaxes(
            title_text='Values',
            title_font=dict(size=letter_size),
        )

        fig.update_yaxes(
            title_text="Frequency",
            title_font=dict(size=letter_size),
        )

        fig.update_layout(
            title=f'{str(data.name).replace('_', ' ').title()} Histogram',
            shapes=[
                dict(
                    type='line',
                    x0=data.mean(),
                    x1=data.mean(),
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',
                    line=dict(
                        color=color_1,
                        width=2,
                        dash="dash"
                    )
                ),
                dict(
                    type='line',
                    x0=data.median(),
                    x1=data.median(),
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',
                    line=dict(
                        color=color_2,
                        width=2,
                        dash="dash"
                    )
                )
            ],
            annotations=[
                dict(
                    x=data.mean(),
                    y=1,
                    xref='x',
                    yref='paper',
                    text='Mean',
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-40
                ),
                dict(
                    x=data.median(),
                    y=1,
                    xref='x',
                    yref='paper',
                    text='Median',
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-40
                )
            ]
        )

        fig.update_layout(
            height=600
        )

    else:

        fig = EmptyPlot()

        st.warning('There was an error with Series Data...', icon="⚠️")

    return fig
