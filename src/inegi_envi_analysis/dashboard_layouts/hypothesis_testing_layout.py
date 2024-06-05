# Libraries
import streamlit as st
import pandas as pd

# Plots
from src.inegi_envi_analysis.plots import TStudentHistogram


def HypothesisTestingLayout(
    df: pd.DataFrame,
):

    st.subheader('Are women more prone to default?')

    col_left, buff1, mid_col, buff2, col_right = st.columns([3, 1, 3, 1, 3])

    with col_left:
        st.markdown("**Hypothesis**")

        st.markdown("*H0*: Women don't are more prone to default")

        st.markdown("*H1*: Women do are more prone to default")

    with mid_col:

        st.markdown("**Women's sample**")
        st.markdown(f"Delinquency Prob (Mean): {df[df['woman'] == 1]['late_payment_3'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['woman'] == 1]['late_payment_3'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['woman'] == 1]['late_payment_3'])}")

    with col_right:

        st.markdown("**Men's sample**")
        st.markdown(f"Delinquency Prob (Mean): {df[df['woman'] == 0]['late_payment_3'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['woman'] == 0]['late_payment_3'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['woman'] == 0]['late_payment_3'])}")

    fig1 = TStudentHistogram(
        df[df['woman'] == 0]['late_payment_3'],
        df[df['woman'] == 1]['late_payment_3']
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.divider()

    st.subheader('Are people with less income more likely to default on their mortgage?')

    col_left, buff1, mid_col, buff2, col_right = st.columns([3, 1, 3, 1, 3])

    with col_left:
        st.markdown("**Hypothesis**")

        st.markdown("*H0*: People with less income are not more prone to default")

        st.markdown("*H1*: People with less income are more prone to default")

    with mid_col:
        st.markdown("**Debtors' sample**")
        st.markdown(f"Income Mean: {df[df['late_payment_3'] == 1]['monthly_wage'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 1]['monthly_wage'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 1]['monthly_wage'])}")

    with col_right:
        st.markdown("**Non-debtors' sample**")
        st.markdown(f"Income Mean: {df[df['late_payment_3'] == 0]['monthly_wage'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 0]['monthly_wage'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 0]['monthly_wage'])}")

    fig2 = TStudentHistogram(
        df[df['late_payment_3'] == 1]['monthly_wage'],
        df[df['late_payment_3'] == 0]['monthly_wage']
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    st.subheader('Does the percentage of income that goes towards payments matter?')

    col_left, buff1, mid_col, buff2, col_right = st.columns([3, 1, 3, 1, 3])

    with col_left:
        st.markdown("**Hypothesis**")

        st.markdown("*H0*: The percentage of income that goes towards payment doesn't matter")

        st.markdown("*H1*: The percentage of income that goes towards payment does matter")

    with mid_col:
        st.markdown("**Debtors' sample**")
        st.markdown(f"Fraction Mean: {df[df['late_payment_3'] == 1]['payment_percentage'].div(100).mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 1]['payment_percentage'].div(100).var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 1]['payment_percentage'])}")

    with col_right:
        st.markdown("**Non-debtors' sample**")
        st.markdown(f"Fraction Mean: {df[df['late_payment_3'] == 0]['payment_percentage'].div(100).mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 0]['payment_percentage'].div(100).var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 0]['payment_percentage'])}")

    fig3 = TStudentHistogram(
        df[df['late_payment_3'] == 1]['payment_percentage'].div(100),
        df[df['late_payment_3'] == 0]['payment_percentage'].div(100)
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.divider()

    st.subheader('Do larger mortgages become unpayable?')

    col_left, buff1, mid_col, buff2, col_right = st.columns([3, 1, 3, 1, 3])

    with col_left:
        st.markdown("**Hypothesis**")

        st.markdown("*H0*: Larger credits don't increase the prone of default")

        st.markdown("*H1*: Larger credits do increase the prone of default")

    with mid_col:
        st.markdown("**Debtors' sample**")
        st.markdown(f"Credit Mean: {df[df['late_payment_3'] == 1]['credit_amount'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 1]['credit_amount'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 1]['credit_amount'])}")

    with col_right:
        st.markdown("**Non-debtors' sample**")
        st.markdown(f"Credit Mean: {df[df['late_payment_3'] == 0]['credit_amount'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 0]['credit_amount'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 0]['credit_amount'])}")

    fig4 = TStudentHistogram(
        df[df['late_payment_3'] == 1]['credit_amount'].div(100),
        df[df['late_payment_3'] == 0]['credit_amount'].div(100)
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.divider()

    st.subheader('Do more expensive houses become unpayable?')

    col_left, buff1, mid_col, buff2, col_right = st.columns([3, 1, 3, 1, 3])

    with col_left:
        st.markdown("**Hypothesis**")

        st.markdown("*H0*: More expensive houses don't increase the prone of default")

        st.markdown("*H1*: More expensive houses do increase the prone of default")

    with mid_col:
        st.markdown("**Debtors' sample**")
        st.markdown(f"Credit Mean: {df[df['late_payment_3'] == 1]['price'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 1]['price'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 1]['price'])}")

    with col_right:
        st.markdown("**Non-debtors' sample**")
        st.markdown(f"Credit Mean: {df[df['late_payment_3'] == 0]['price'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 0]['price'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 0]['price'])}")

    fig5 = TStudentHistogram(
        df[df['late_payment_3'] == 1]['price'].div(100),
        df[df['late_payment_3'] == 0]['price'].div(100)
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    st.divider()

    st.subheader('Is older people more prone to default?')

    col_left, buff1, mid_col, buff2, col_right = st.columns([3, 1, 3, 1, 3])

    with col_left:
        st.markdown("**Hypothesis**")

        st.markdown("*H0*: Older people are not more prone to default")

        st.markdown("*H1*: Older people are more prone to default")

    with mid_col:
        st.markdown("**Debtors' sample**")
        st.markdown(f"Age Mean: {df[df['late_payment_3'] == 1]['age'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 1]['age'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 1]['age'])}")

    with col_right:
        st.markdown("**Non-debtors' sample**")
        st.markdown(f"Age Mean: {df[df['late_payment_3'] == 0]['age'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['late_payment_3'] == 0]['age'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['late_payment_3'] == 0]['age'])}")

    fig6 = TStudentHistogram(
        df[df['late_payment_3'] == 0]['age'],
        df[df['late_payment_3'] == 1]['age']
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    st.divider()

    st.subheader('Does delinquency probability depends on the year of the mortgage acquisition?')

    years = st.selectbox(
        'Choose a Feature',
        (sorted(df['year_of_acquisition'].unique())),
    )

    col_left, buff1, mid_col, buff2, col_right = st.columns([3, 1, 3, 1, 3])

    with col_left:
        st.markdown("**Hypothesis**")

        st.markdown(f"*H0*: Acquiring a mortgage in {years} doesn't change the probability of default")

        st.markdown(f"*H1*: Acquiring a mortgage in {years} does change the probability of default")

    with mid_col:
        st.markdown("**Year of Acquisition Sample**")
        st.markdown(f"Age Mean: {df[df['year_of_acquisition'] == years]['late_payment_3'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['year_of_acquisition'] == years]['late_payment_3'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['year_of_acquisition'] == years]['late_payment_3'])}")

    with col_right:
        st.markdown("**Other Years Sample**")
        st.markdown(f"Age Mean: {df[df['year_of_acquisition'] != years]['late_payment_3'].mean().round(2)}")
        st.markdown(f"Variance: {df[df['year_of_acquisition'] != years]['late_payment_3'].var(ddof=1).round(2)}")
        st.markdown(f"Sample Size: {len(df[df['year_of_acquisition'] != years]['late_payment_3'])}")

    fig7 = TStudentHistogram(
        df[df['year_of_acquisition'] == years]['late_payment_3'],
        df[df['year_of_acquisition'] != years]['late_payment_3']
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )
