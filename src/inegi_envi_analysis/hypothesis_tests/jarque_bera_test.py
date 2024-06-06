# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import random
from scipy.stats import jarque_bera
from scipy.stats import chi2
import plotly.graph_objects as go


@st.cache_resource
def JarqueBetaTest(
    series: pd.Series,
):
    # Colors:
    palette = list(sns.color_palette("Spectral", 20).as_hex())

    color1 = random.choice(palette)
    color2 = random.choice(palette)

    # Jarque-Bera Tests
    jb_statistic, jb_p_value = jarque_bera(series)

    # Degrees of Freedom
    dfreed = 2

    # level fo significance
    alpha = 0.05

    # Critical Value
    critical_value = chi2.ppf(1 - alpha, dfreed)

    # t-student Distribution
    x = np.linspace(0, 15, 1000)

    y = chi2.pdf(x, dfreed)

    # Now create the figure
    fig = go.Figure()

    # Add the Chi-Square distribution
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color=color2, width=2),
            name='Chi-Square Distribution df=2'
        )
    )

    # Add reject areas
    x_fill_right = np.linspace(critical_value, 15, 100)
    y_fill_right = chi2.pdf(x_fill_right, dfreed)

    fig.add_trace(
        go.Scatter(
            x=np.concatenate([x_fill_right, x_fill_right[::-1]]),
            y=np.concatenate([y_fill_right, np.zeros_like(y_fill_right)]),
            fill='toself',
            fillcolor=color1,
            line=dict(color=color1),
            name='Reject Area'
        )
    )

    # Add critical values
    fig.add_trace(
        go.Scatter(
            x=[critical_value, critical_value],
            y=[0, chi2.pdf(critical_value, dfreed)],
            mode='lines',
            line=dict(color='black', dash='dash'),
            name=f'Critical Value {critical_value:.2f}'
        )
    )

    # Add the Jarque-Bera Statistic
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=jb_statistic if jb_statistic < 14 else 14,
            y0=0,
            x1=jb_statistic if jb_statistic < 14 else 14,
            y1=chi2.pdf(jb_statistic, dfreed) if jb_statistic < 15 else 0,
            xref="x",
            yref="y",
            line=dict(
                color='#3E5F8A',
                width=2,
                dash="dash"
            ),
            name=f'Jarque-Bera Statistic: {jb_statistic:.2f}'
        )
    )

    # Add annotation for Jarque-Bera
    fig.add_annotation(
        x=jb_statistic if jb_statistic < 14 else 14,
        y=chi2.pdf(jb_statistic, dfreed) if jb_statistic < 14 else 0,
        xref='x',
        yref='y',
        text=f'Jarque-Bera: {jb_statistic:.2f} (p-value: {jb_p_value:.2f})',
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40
    )

    # Config
    fig.update_layout(
        title='Chi-Square Distribution with 2df and Jarque-Bera Statistic',
        xaxis_title='Values',
        yaxis_title='Density',
        showlegend=True,
        height=400
    )

    return fig
