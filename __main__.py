# Libraries
import os
import pandas as pd

# Modules
from inegi_envi_analysis import download_envi_data
from inegi_envi_analysis import unzip_envi_data
from inegi_envi_analysis import create_data_set

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

data = create_data_set()

data.to_excel('Inputs/dataset.xlsx')

