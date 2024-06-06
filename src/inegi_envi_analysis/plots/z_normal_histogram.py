# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import random
from scipy.stats import norm
from scipy.stats import mannwhitneyu
import plotly.graph_objects as go


@st.cache_resource
def NormalDistribution(
    series1: pd.Series,
    series2: pd.Series,
):
    # Colors:
    palette = list(sns.color_palette("Spectral", 20).as_hex())

    color1 = random.choice(palette)
    color2 = random.choice(palette)

    x = np.linspace(-5, 5, 1000)

    y = norm.pdf(x, 0, 1)

    # Level of Significance
    alpha = 0.05

    # Critical Z-Score
    z_critical = norm.ppf(1 - alpha / 2)

    # Calculate Z-Score
    mean1 = np.mean(series1)
    mean2 = np.mean(series2)
    std1 = np.std(series1, ddof=1)
    std2 = np.std(series2, ddof=1)
    n1 = len(series1)
    n2 = len(series2)

    # Calculate Mann-Whitney U Statistic
    u_statistic, u_p_value = mannwhitneyu(series1, series2, alternative='two-sided')

    # Calculate expected value and variance of U
    E_U = n1 * n2 / 2
    Var_U = n1 * n2 * (n1 + n2 + 1) / 12

    # Calculate Z-score
    z = ((u_statistic - E_U) / np.sqrt(Var_U)).round(2)

    # Now create the figure
    fig = go.Figure()

    # Add the t-student distribution
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color=color2, width=2),
            name=f'Normal Distribution'
        )
    )

    # Add left critical area
    x_critical_left = np.linspace(-4, -z_critical, 500)
    y_critical_left = norm.pdf(x_critical_left, 0, 1)

    fig.add_trace(
        go.Scatter(
            x=x_critical_left,
            y=y_critical_left,
            fill='tozeroy',
            name='Left Critical Area',
            mode='none',
            line=dict(color=color1),
            fillcolor=color1,
        )
    )

    # Add right critical area
    x_critical_right = np.linspace(z_critical, 4, 500)
    y_critical_right = norm.pdf(x_critical_right, 0, 1)

    fig.add_trace(
        go.Scatter(
            x=x_critical_right,
            y=y_critical_right,
            fill='tozeroy',
            name='Right Critical Area',
            mode='none',
            line=dict(color=color1),
            fillcolor=color1,
        )
    )

    # Add lines on Critical Z
    fig.add_trace(
        go.Scatter(
            x=[-z_critical, -z_critical],
            y=[0, norm.pdf(z_critical)],
            mode='lines',
            line=dict(color='black', dash='dash'),
            name=f'Critical Value -{z_critical:.2f}'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[z_critical, z_critical],
            y=[0, norm.pdf(z_critical)],
            mode='lines',
            line=dict(color='black', dash='dash'),
            name=f'Critical Value {z_critical:.2f}'
        )
    )

    # Add vertical lines on z-score values
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=z,
            y0=0,
            x1=z,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(
                color='#3E5F8A',
                width=2,
                dash="dash"
            ),
            name=f'Z-Score: {z}'
        )
    )

    # Add the arrow for Z-Score
    fig.update_layout(
        shapes=[
            dict(
                type='line',
                x0=z,
                x1=z,
                y0=0,
                y1=1,
                xref='x',
                yref='paper',
                line=dict(
                    color='#3E5F8A',
                    width=2,
                    dash="dash"
                )
            )
        ],
        annotations=[
            dict(
                x=z,
                y=1,
                xref='x',
                yref='paper',
                text=f'U-Score: {z}',
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40
            )
        ]
    )

    # Config
    fig.update_layout(
        title=f'Normal Distribution, Z-Score and Mann-Whitney U Statistic',
        xaxis_title='Values',
        yaxis_title='Density',
        showlegend=True
    )

    fig.update_layout(
        height=400
    )

    return fig
