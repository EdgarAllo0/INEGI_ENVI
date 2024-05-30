# Libraries
import os
import streamlit as st
import pandas as pd
import requests


@st.cache_resource
def read_dataset_excel() -> pd.DataFrame:

    df = pd.read_excel('Inputs/dataset.xlsx', index_col='index')

    return df


@st.cache_data
def get_spatial_data():
    repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'

    # GeoJSON
    mx_regions_geo = requests.get(repo_url).json()

    return mx_regions_geo
