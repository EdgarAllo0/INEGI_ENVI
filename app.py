# Libraries
import streamlit as st
from streamlit_option_menu import option_menu

# Other Libraries
import pandas as pd

# Modules
from src.inegi_envi_analysis import HistogramPlot
from src.inegi_envi_analysis import StackedHistogramPlot
from src.inegi_envi_analysis import BoxPlot

# Set the website layouts
st.set_page_config(
    page_title="INEGI - ENVI Analysis",
    layout="wide",
)

with st.sidebar:
    st.header('INEGI-ENVI (2020) Analysis')

    selected = option_menu(
        None,
        ["Data Exploration", "Hypothesis Testing", 'Models'],
        icons=['house', 'balloon', "cash"],
        menu_icon="cast",
        default_index=0
    )

    st.subheader('A Work by Not a Recommendation')

    st.text('Author: Edgar Alcántara')

    st.link_button(
        "Check out my LinkedIn profile",
        "https://www.linkedin.com/in/edgar-mauricio-alc%C3%A1ntara-l%C3%B3pez-33505b237/"
    )

    st.link_button(
        "Go check my Portfolio on GitHub",
        "https://github.com/EdgarAllo0"
    )

if selected == 'Data Exploration':

    st.title("ENVI Data Exploration")

    df = pd.read_excel('Inputs/dataset.xlsx', index_col='index')

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
        )

    fig2 = BoxPlot(
        df[df[late_payment_conditions_2] == 0][boxplot_vars],
        df[df[late_payment_conditions_2] == 1][boxplot_vars],
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


elif selected == 'Hypothesis Testing':

    st.title('Statistical Hypothesis Testing')

    st.warning('We are working on it...', icon="⚠️")

elif selected == 'Models':

    st.title('Econometric Models')

    st.warning('We are working on it...', icon="⚠️")
