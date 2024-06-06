# Libraries
import streamlit as st
import pandas as pd

# Plots
from src.inegi_envi_analysis.plots import HistogramPlot
from src.inegi_envi_analysis.plots import StackedHistogramPlot
from src.inegi_envi_analysis.plots import BoxPlot
from src.inegi_envi_analysis.plots import ViolinPlot
from src.inegi_envi_analysis.plots import StackedBarPlot
from src.inegi_envi_analysis.hypothesis_tests import JarqueBetaTest


def DataExplorationLayout(
        df: pd.DataFrame,
):

    st.subheader('Filtered Data')

    st.dataframe(df, height=300)

    st.subheader('Histograms')

    histogram_vars = st.selectbox(
        'Choose a Feature',
        (list(df.select_dtypes(include=['number']).columns)),
    )

    fig = HistogramPlot(df[histogram_vars])

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader('Stacked Histograms')

    col1, col2 = st.columns(2)

    with col1:
        late_payment_conditions_1 = st.selectbox(
            'Choose a Late Payment Condition',
            (['late_payment_1', 'late_payment_2', 'late_payment_3']),
            key='payment1'
        )

    with col2:
        stacked_histogram_vars = st.selectbox(
            'Choose a Feature',
            (list(df.drop(
                columns=['late_payment_1', 'late_payment_2', 'late_payment_3']
            ).select_dtypes(include=['number']).columns)),
        )

    fig1 = StackedHistogramPlot(
        df[df[late_payment_conditions_1] == 0][stacked_histogram_vars],
        df[df[late_payment_conditions_1] == 1][stacked_histogram_vars],
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.subheader('Box Plots')

    col3, col4 = st.columns(2)

    with col3:
        late_payment_conditions_2 = st.selectbox(
            'Choose a Late Payment Condition',
            (['late_payment_1', 'late_payment_2', 'late_payment_3']),
            key='payment2'
        )

    with col4:
        unique_counts = df.nunique()

        columns_with_more_than_10_unique_values = unique_counts[unique_counts > 10].index

        result_df = df[columns_with_more_than_10_unique_values]

        boxplot_vars = st.selectbox(
            'Choose a Feature',
            (list(result_df.select_dtypes(include=['number']).columns)),
            key='bxvar'
        )

    fig2 = BoxPlot(
        df[df[late_payment_conditions_2] == 0][boxplot_vars],
        df[df[late_payment_conditions_2] == 1][boxplot_vars],
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.subheader('Violin Plots')

    col5, col6 = st.columns(2)

    with col5:
        late_payment_conditions_3 = st.selectbox(
            'Choose a Late Payment Condition',
            (['late_payment_1', 'late_payment_2', 'late_payment_3']),
            key='payment3'
        )

    with col6:
        violin_vars = st.selectbox(
            'Choose a Feature for Violin Plots',
            (list(df.drop(
                columns=['late_payment_1', 'late_payment_2', 'late_payment_3']
            ).select_dtypes(include=['number']).columns)),
        )

    fig3 = ViolinPlot(
        df,
        late_payment_conditions_3,
        violin_vars,
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    col7, col8 = st.columns(2)

    with col7:
        late_payment_conditions_4 = st.selectbox(
            'Choose a Late Payment Condition',
            (['late_payment_1', 'late_payment_2', 'late_payment_3']),
            key='payment4'
        )

    with col8:
        unique_counts_2 = df.nunique()

        columns_with_less_than_10_unique_values = unique_counts[unique_counts_2 <= 10].index

        result_df_2 = df[columns_with_less_than_10_unique_values]

        stacked_barplot_vars = st.selectbox(
            'Choose a Feature for Stacked Bar Plot',
            (list(result_df_2.select_dtypes(include=['number']).columns)),
        )

    fig4 = StackedBarPlot(
        df,
        late_payment_conditions_4,
        stacked_barplot_vars,
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.subheader('Normality Tests')

    unique_counts = df.nunique()

    columns_with_more_than_10_unique_values = unique_counts[unique_counts > 10].index

    result_df = df[columns_with_more_than_10_unique_values]

    normal_tests_vars = st.selectbox(
        'Choose a Feature',
        (list(result_df.select_dtypes(include=['number']).columns)),
        key='normvar'
    )

    fig4 = JarqueBetaTest(
        df[normal_tests_vars]
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )
