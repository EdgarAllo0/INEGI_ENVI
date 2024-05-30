# Libraries
import streamlit as st
from streamlit_option_menu import option_menu

# Other Libraries
import pandas as pd

# Modules
from src.inegi_envi_analysis import read_dataset_excel

# Layouts
from src.inegi_envi_analysis import DataExplorationLayout


# Set the website layouts
st.set_page_config(
    page_title="INEGI - ENVI Analysis",
    layout="wide",
)

# Set the sidebar content
with st.sidebar:
    st.header('INEGI-ENVI (2020) Analysis')

    selected = option_menu(
        None,
        ["Data Exploration", "Hypothesis Testing", 'Models'],
        icons=['house', 'balloon', "cash"],
        menu_icon="cast",
        default_index=0
    )

    with open("assets/dictionary.xlsx", "rb") as file:
        excel_data = file.read()

    st.download_button(
        label="Download Data Dictionary",
        data=excel_data,
        file_name='dictionary.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
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

# Download data (you must run main.py before the Dashboard)
df = read_dataset_excel()

# Dashboard

if selected == 'Data Exploration':

    st.title("ENVI Data Exploration")

    DataExplorationLayout(df)

elif selected == 'Hypothesis Testing':

    st.title('Statistical Hypothesis Testing')

    st.warning('We are working on it...', icon="⚠️")

elif selected == 'Models':

    st.title('Econometric Models')

    st.warning('We are working on it...', icon="⚠️")
