# Libraries
import os
import pandas as pd

# Modules
from src.inegi_envi_analysis import download_envi_data
from src.inegi_envi_analysis import unzip_envi_data
from src.inegi_envi_analysis import create_data_set

# Get Data
if os.path.exists('Inputs/envi_raw_data/envi_data.zip') and os.path.isdir('Inputs/envi_raw_data/envi_data.zip'):
    print("Data already exists")
else:
    download_envi_data()
    print("Data downloaded")

# Unzip Data
if os.path.exists('Inputs/envi_unzipped_data') and os.path.isdir('Inputs/envi_unzipped_data'):
    print("Data already unzipped")
else:
    unzip_envi_data()
    print("Data Unzipped Successfully")

# Create DataSet
if os.path.exists('Inputs/dataset.xlsx') and os.path.isdir('Inputs/dataset.xlsx'):
    print("Data Set already exists")
else:
    data = create_data_set()
    data.to_excel('Inputs/dataset.xlsx')
    print("Data Set successfully created")


from src.inegi_envi_analysis import get_spatial_data

json = get_spatial_data()