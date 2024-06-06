# Libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import random
from scipy.stats import t
from scipy.stats import ttest_ind
import plotly.graph_objects as go


def calculate_degrees_of_freedom(
    series1: pd.Series,
    series2: pd.Series,
):
    # Calculate variances and size of the samples

    s1_sq = series1.var(ddof=1)  # ddof=1 to calculate sample variance
    s2_sq = series2.var(ddof=1)
    n1 = len(series1)
    n2 = len(series2)

    # Calculate the degrees of freedom
    numerator = (s1_sq / n1 + s2_sq / n2) ** 2
    denominator = ((s1_sq / n1) ** 2 / (n1 - 1)) + ((s2_sq / n2) ** 2 / (n2 - 1))
    dfreed = numerator / denominator

    return int(dfreed.round(0))


@st.cache_resource
def TStudentTest(
    series1: pd.Series,
    series2: pd.Series,
):
    # Colors:
    palette = list(sns.color_palette("Spectral", 20).as_hex())

    color1 = random.choice(palette)
    color2 = random.choice(palette)

    # Degrees of Freedom
    dfreed = calculate_degrees_of_freedom(series1, series2)

    # t-student Distribution
    x = np.linspace(-5, 5, 1000)

    y = t.pdf(x, dfreed)

    # Level of Significance
    alpha = 0.05

    # Critical t-value (tends to 1.96)
    critical_value = t.ppf(1 - alpha / 2, dfreed)

    t_stat, p_value = ttest_ind(series1, series2)

    t_stat = t_stat.round(2)

    # Now create the figure
    fig = go.Figure()

    # Add the t-student distribution
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color=color2, width=2),
            name=f't-distribution df={dfreed}'
        )
    )

    # Add reject areas
    x_fill_left = np.linspace(-5, -critical_value, 100)
    y_fill_left = t.pdf(x_fill_left, dfreed)

    fig.add_trace(
        go.Scatter(
            x=np.concatenate(
                [x_fill_left, x_fill_left[::-1]
                 ]
            ),
            y=np.concatenate(
                [y_fill_left, np.zeros_like(y_fill_left)
                 ]
            ),
            fill='toself',
            fillcolor=color1,
            line=dict(color=color1),
            name='Reject Area'
        )
    )

    x_fill_right = np.linspace(critical_value, 5, 100)
    y_fill_right = t.pdf(x_fill_right, dfreed)

    fig.add_trace(
        go.Scatter(
            x=np.concatenate(
                [x_fill_right, x_fill_right[::-1]
                 ]
            ),
            y=np.concatenate(
                [y_fill_right, np.zeros_like(y_fill_right)
                 ]
            ),
            fill='toself',
            fillcolor=color1,
            line=dict(color=color1),
            name='Reject Area'
        )
    )

    # Add vertical lines on critical values
    fig.add_trace(
        go.Scatter(
            x=[-critical_value, -critical_value],
            y=[0, t.pdf(-critical_value, dfreed)],
            mode='lines',
            line=dict(color='black', dash='dash'),
            name=f'Left Critical Value -{critical_value:.2f}'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[critical_value, critical_value],
            y=[0, t.pdf(critical_value, dfreed)],
            mode='lines',
            line=dict(color='black', dash='dash'),
            name=f'Right Critical Value {critical_value:.2f}'
        )
    )

    # Add the hypothesis t-value
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=t_stat,
            y0=0,
            x1=t_stat,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(
                color='#3E5F8A',
                width=2,
                dash="dash"
            ),
            name=f'T-Value: {t_stat}'
        )
    )

    fig.update_layout(
        shapes=[
            dict(
                type='line',
                x0=t_stat,
                x1=t_stat,
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
                x=t_stat,
                y=1,
                xref='x',
                yref='paper',
                text=f't-value: {t_stat} (p-value: {p_value:.2f})',
                showarrow=True,
                arrowhead=2,
                ax=0,
                ay=-40
            )
        ]
    )

    # Config
    fig.update_layout(
        title=f'T-Student Distribution with {dfreed} degrees of freedom',
        xaxis_title='t-values',
        yaxis_title='Density',
        showlegend=True
    )

    fig.update_layout(
        height=400
    )

    return fig
