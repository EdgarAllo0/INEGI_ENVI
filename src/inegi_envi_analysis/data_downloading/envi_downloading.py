# Libraries
import requests
import os
import zipfile

data_url = 'https://www.inegi.org.mx/contenidos/programas/envi/2020/microdatos/envi_2020_base_de_datos_csv.zip'

envi_directory_raw_data = 'Inputs/envi_raw_data'
envi_directory_unzipped_data = 'Inputs/envi_unzipped_data'


def download_envi_data(
        url: str = data_url,
        directory: str = envi_directory_raw_data,
):
    output_file_path = os.path.join(directory, 'envi_data.zip')

    # Create directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        # Send HTTP request to download the file
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the content to a file
            with open(output_file_path, 'wb') as out_file:
                out_file.write(response.content)
            print(f'File downloaded successfully and saved to {output_file_path}')

        else:
            print(f'Failed to download file: HTTP status code {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'An error occurred while downloading the file: {e}')

    return None


def unzip_envi_data(
    zipped_data_directory: str = envi_directory_raw_data,
    unzipped_data_directory: str = envi_directory_unzipped_data,
):
    # Create directory if it does not exist
    if not os.path.exists(unzipped_data_directory):
        os.makedirs(unzipped_data_directory)

    with zipfile.ZipFile(zipped_data_directory + '/envi_data.zip', 'r') as zip_ref:

        zip_ref.extractall(unzipped_data_directory)

    return None
