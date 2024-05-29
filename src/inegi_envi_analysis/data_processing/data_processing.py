# Libraries
import pandas as pd


def read_data_csv(
    path: str,
):
    try:
        df = pd.read_csv(path)
        df['index'] = (df['FOLIO'].astype(str) + '-' + df['VIV_SEL'].astype(str) + '-' + df['EST_DIS'].astype(str) +
                       '-' + df['UPM_DIS'].astype(str) + '-' + df['FACTOR'].astype(str))
        df.set_index('index', inplace=True)
        df.drop_duplicates(inplace=True)
        print("File successfully read")
        return df

    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='utf-8')
        df['index'] = (df['FOLIO'].astype(str) + '-' + df['VIV_SEL'].astype(str) + '-' + df['EST_DIS'].astype(str) +
                       '-' + df['UPM_DIS'].astype(str) + '-' + df['FACTOR'].astype(str))
        df.set_index('index', inplace=True)
        df.drop_duplicates(inplace=True)
        print("File successfully read with UTF-8 Encoding")
        return df

    except FileNotFoundError:
        print("File not found")
        return None

    except Exception as e:
        print(f"Unexpected error Error: {e}")
        return None


def remove_duplicate_columns(
    df
):
    # Identify duplicate columns
    cols = pd.Series(df.columns)

    # Mark duplicates as True except for the first occurrence
    cols_duplicated = cols.duplicated(keep='first')

    # Drop the duplicate columns
    df_cleaned = df.loc[:, ~cols_duplicated]

    return df_cleaned


def create_dataframe(
):
    data1 = read_data_csv('Inputs/envi_unzipped_data/Bases de datos/TVIVIENDA.csv')
    data2 = read_data_csv('Inputs/envi_unzipped_data/Bases de datos/TSDEM.csv')
    data2 = data2[data2['PAREN'] == 1]
    data2 = data2[data2['HOGAR'] == 1]

    data3 = read_data_csv('Inputs/envi_unzipped_data/Bases de datos/THOGAR.csv')
    data3 = data3[data3['HOGAR'] == 1]

    df_concat = pd.concat([data1, data2, data3], axis=1)

    df_concat = df_concat.loc[:, ~df_concat.columns.duplicated()]

    return df_concat
