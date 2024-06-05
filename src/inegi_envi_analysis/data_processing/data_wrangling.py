# Libraries
import pandas as pd
import numpy as np

# Modules
from src.inegi_envi_analysis.data_processing.data_processing import create_dataframe


def create_data_set() -> pd.DataFrame:
    # Create DataFrames
    data = create_dataframe()

    # Excluding those with no mortgages
    data = data.loc[
        (data['P5_15_01'] == 1) |
        (data['P5_15_02'] == 1) |
        (data['P5_15_03'] == 1) |
        (data['P5_15_04'] == 1)
        ]

    # Excluding if they have more than one mortgage
    conditions = (
            (data['P5_15_01'] == 1).astype(int) +
            (data['P5_15_02'] == 1).astype(int) +
            (data['P5_15_03'] == 1).astype(int) +
            (data['P5_15_04'] == 1).astype(int)
    )

    data = data.loc[conditions == 1]

    # Then we are also going to exclude those that acquired a house between 2000 and 2019
    data = data.rename(columns={'P5_13_1': 'year_of_acquisition'})    # T means the year when the house was acquired
    data = data.dropna(subset=['year_of_acquisition'])
    data = data.loc[data['year_of_acquisition'].between(2000, 2019)]

    # Then we have to create a variable that captures how much time has happened since the house acquisition
    data['year_of_survey'] = 2020
    data['time_elapsed'] = data['year_of_survey'] - data['year_of_acquisition']
    data['time_elapsed'] = data['time_elapsed'].apply(lambda x: np.nan if x <= 0 else x)
    data = data.dropna(subset=['time_elapsed'])

    # FIRST LATE PAYMENT CONDITION #

    # Now set the credit duration
    data['P5_17_01'] = data['P5_17_01'].apply(lambda x: np.nan if x >= 98 else x)
    data['P5_17_01'] = data['P5_17_01'].apply(lambda x: np.nan if x == 0 else x)

    data['P5_17_02'] = data['P5_17_02'].apply(lambda x: np.nan if x >= 98 else x)
    data['P5_17_02'] = data['P5_17_02'].apply(lambda x: np.nan if x == 0 else x)

    data['P5_17_03'] = data['P5_17_03'].apply(lambda x: np.nan if x >= 98 else x)
    data['P5_17_03'] = data['P5_17_03'].apply(lambda x: np.nan if x == 0 else x)

    data['P5_17_04'] = data['P5_17_04'].apply(lambda x: np.nan if x >= 98 else x)
    data['P5_17_04'] = data['P5_17_04'].apply(lambda x: np.nan if x == 0 else x)

    data['credit_duration'] = data[['P5_17_01', 'P5_17_02', 'P5_17_03', 'P5_17_04']].fillna(0).sum(axis=1)
    data['credit_duration'] = data['credit_duration'].apply(lambda x: np.nan if x == 0 else x)

    data = data.dropna(subset=['credit_duration'])

    # Create the expected time left to finish the credit
    data['expected_time_to_finish'] = data['credit_duration'] - data['time_elapsed']

    data['expected_time_to_finish'] = data['expected_time_to_finish'].apply(lambda x: np.nan if x <= 0 else x)

    data = data.dropna(subset=['expected_time_to_finish'])

    # Create the reported time left to finish the credit
    data['P5_21_1_1'] = data['P5_21_1_1'].apply(lambda x: np.nan if x >= 98 else x)

    data['P5_21_2_1'] = data['P5_21_2_1'].apply(lambda x: np.nan if x >= 98 else x)

    data['P5_21_3_1'] = data['P5_21_3_1'].apply(lambda x: np.nan if x >= 98 else x)

    data['P5_21_4_1'] = data['P5_21_4_1'].apply(lambda x: np.nan if x >= 98 else x)

    data['reported_time_to_finish'] = data[['P5_21_1_1', 'P5_21_2_1', 'P5_21_3_1', 'P5_21_4_1']].fillna(0).sum(axis=1)
    data['reported_time_to_finish'] = data['reported_time_to_finish'].apply(lambda x: np.nan if x == 0 else x)

    data = data.dropna(subset=['reported_time_to_finish'])

    # Now create the first late payment condition
    data['late_payment_1'] = 0

    data.loc[(data['expected_time_to_finish'] < data['reported_time_to_finish']), "late_payment_1"] = 1

    data = data.dropna(subset=['late_payment_1'])

    # SECOND LATE PAYMENT CONDITION #

    # Paid amount
    data['P5_19_1'] = data['P5_19_1'].apply(lambda x: np.nan if x >= 9999886 else x)

    data['P5_19_2'] = data['P5_19_2'].apply(lambda x: np.nan if x >= 9999886 else x)

    data['P5_19_3'] = data['P5_19_3'].apply(lambda x: np.nan if x >= 9999886 else x)

    data['P5_19_4'] = data['P5_19_4'].apply(lambda x: np.nan if x >= 9999886 else x)

    data['paid_amount'] = data[['P5_19_1', 'P5_19_2', 'P5_19_3', 'P5_19_4']].fillna(0).sum(axis=1)
    data['paid_amount'] = data['paid_amount'].apply(lambda x: np.nan if x == 0 else x)

    data = data.dropna(subset=['paid_amount'])

    # Credit amount
    data['P5_16_01'] = data['P5_16_01'].apply(lambda x: np.nan if x >= 999999886 else x)

    data['P5_16_02'] = data['P5_16_02'].apply(lambda x: np.nan if x >= 999999886 else x)

    data['P5_16_03'] = data['P5_16_03'].apply(lambda x: np.nan if x >= 999999886 else x)

    data['P5_16_04'] = data['P5_16_04'].apply(lambda x: np.nan if x >= 999999886 else x)

    data['credit_amount'] = data[['P5_16_01', 'P5_16_02', 'P5_16_03', 'P5_16_04']].fillna(0).sum(axis=1)

    data['credit_amount'] = data['credit_amount'].apply(lambda x: np.nan if x == 0 else x)

    data = data.dropna(subset=['credit_amount'])

    # Paid fraction
    data['paid_fraction'] = (data['paid_amount'] / data['credit_amount']) * 100
    data = data.dropna(subset=['paid_fraction'])

    # Expected paid fraction
    data['expected_paid_fraction'] = (data['time_elapsed'] / data['credit_duration']) * 100
    data = data.dropna(subset=['expected_paid_fraction'])

    # Now create the second late payment condition
    data['late_payment_2'] = 0
    data.loc[(data['paid_fraction'] < data['expected_paid_fraction']), "late_payment_2"] = 1
    data = data.dropna(subset=['late_payment_2'])

    # THIRD LATE PAYMENT CONDITION #

    data['late_payment_3'] = data.apply(
        lambda row: 1 if row['late_payment_1'] == 1 or row['late_payment_2'] == 1 else 0,
        axis=1
    )
    data = data.dropna(subset=['late_payment_3'])

    # COVARIATES #

    # If household is under repairs (Dummy)
    data = data.rename(columns={'P6_1_6': 'repairs'})
    data['repairs'] = data['repairs'].apply(lambda x: np.nan if x == 9 else x)
    data['repairs'] = data['repairs'].apply(lambda x: 0 if x == 2 else x)
    data = data.dropna(subset=['repairs'])

    # If household is under remodeling (Dummy)
    data = data.rename(columns={'P6_1_7': 'remodeling'})
    data['remodeling'] = data['remodeling'].apply(lambda x: np.nan if x == 9 else x)
    data['remodeling'] = data['remodeling'].apply(lambda x: 0 if x == 2 else x)
    data = data.dropna(subset=['remodeling'])

    # Distance to Workplace (Satisfaction Categories)
    data = data.rename(columns={'P6_5_1': 'distance_workplace'})
    data['distance_workplace'] = data['distance_workplace'].apply(lambda x: np.nan if x == 9 else x)
    data = data.dropna(subset=['distance_workplace'])

    # Distance to School (Satisfaction Categories)
    data = data.rename(columns={'P6_5_2': 'distance_school'})
    data['distance_school'] = data['distance_school'].apply(lambda x: np.nan if x == 9 else x)
    data = data.dropna(subset=['distance_school'])

    # Distance to Health Center (Satisfaction Categories)
    data = data.rename(columns={'P6_5_3': 'distance_health_center'})
    data['distance_health_center'] = data['distance_health_center'].apply(lambda x: np.nan if x == 9 else x)
    data = data.dropna(subset=['distance_health_center'])

    # Distance to Marketplace (Satisfaction Categories)
    data = data.rename(columns={'P6_5_4': 'distance_marketplace'})
    data['distance_marketplace'] = data['distance_marketplace'].apply(lambda x: np.nan if x == 9 else x)
    data = data.dropna(subset=['distance_marketplace'])

    # House Price (Mexican pesos)
    data = data.rename(columns={'P5_14': 'price'})
    data['price'] = data['price'].apply(lambda x: np.nan if x >= 900000000 else x)
    data['price'] = data['price'].apply(lambda x: np.nan if x == 0 else x)
    data = data.dropna(subset=['price'])

    # Relation between price and credit amount
    data['credit_price_relation'] = (data['credit_amount'] / data['price']) * 100
    data = data.dropna(subset=['credit_price_relation'])

    # Age of the Property (years)
    data = data.rename(columns={'P4_19_1': 'age_property'})
    data['age_property'] = data['age_property'].apply(lambda x: np.nan if x >= 97 else x)
    data = data.dropna(subset=['age_property'])

    # Property Land (square meters)
    data = data.rename(columns={'P4_20_1': 'property_land'})
    data['property_land'] = data['property_land'].apply(lambda x: np.nan if x >= 997 else x)
    data = data.dropna(subset=['property_land'])

    # Construction Land (square meters)
    data = data.rename(columns={'P4_21_1': 'construction_land'})
    data['construction_land'] = data['construction_land'].apply(lambda x: np.nan if x >= 997 else x)
    data = data.dropna(subset=['construction_land'])

    # Structure cracks (Dummy)
    data = data.rename(columns={'P4_25_1': 'cracks'})
    data['cracks'] = data['cracks'].apply(lambda x: np.nan if x == 9 else x)
    data['cracks'] = data['cracks'].apply(lambda x: 0 if x == 2 else x)
    data = data.dropna(subset=['cracks'])

    # Intentions to move (Dummy)
    data = data.rename(columns={'P6_12': 'moving'})
    data['moving'] = data['moving'].apply(lambda x: np.nan if x == 9 else x)
    data['moving'] = data['moving'].apply(lambda x: 0 if x == 2 else x)
    data = data.dropna(subset=['moving'])

    # Second property (Dummy)
    data = data.rename(columns={'P7_1': 'second_property'})
    data['second_property'] = data['second_property'].apply(lambda x: np.nan if x == 9 else x)
    data['second_property'] = data['second_property'].apply(lambda x: 0 if x == 2 else x)
    data = data.dropna(subset=['second_property'])

    # Wages (Mexican pesos)
    data = data.rename(columns={'P3_4': 'wage'})
    data['wage'] = data['wage'].apply(lambda x: np.nan if x == 'NA' else x)
    data['wage'] = data['wage'].astype(float)
    data['wage'] = data['wage'].apply(lambda x: np.nan if x >= 98000 else x)
    data['wage'] = data['wage'].apply(lambda x: np.nan if x == 0 else x)
    data = data.dropna(subset=['wage'])

    # Monthly payments (Mexican pesos)
    data = data.rename(columns={'P5_2': 'monthly_payments'})
    data['monthly_payments'] = data['monthly_payments'].apply(lambda x: np.nan if x >= 999999888 else x)
    data = data.dropna(subset=['monthly_payments'])

    # Employment Status (Categorical)
    data = data.rename(columns={'P3_1': 'employment_status'})
    data['employment_status'] = data['employment_status'].apply(lambda x: np.nan if x == 'NA' else x)
    data['employment_status'] = data['employment_status'].astype(float)
    data = data.dropna(subset=['employment_status'])

    # Unemployment Status (Dummy)
    data['unemployed'] = data.apply(
        lambda row: 1 if row['employment_status'] == 3 or row['employment_status'] == 4 else 0,
        axis=1
    )
    data = data.dropna(subset=['unemployed'])

    # Retirement Status (Dummy)
    data['retired'] = data.apply(
        lambda row: 1 if row['employment_status'] == 4 else 0,
        axis=1
    )
    data = data.dropna(subset=['retired'])

    # Occupation (Categorical)
    data = data.rename(columns={'P3_3': 'occupation'})
    data['occupation'] = data['occupation'].apply(lambda x: np.nan if x == 'NA' else x)
    data['occupation'] = data['occupation'].astype(float)
    data = data.dropna(subset=['occupation'])

    # Wage Frequency (Categorical)
    data = data.rename(columns={'P3_4A': 'wage_frequency'})
    data['wage_frequency'] = data['wage_frequency'].apply(lambda x: np.nan if x == 'NA' else x)
    data['wage_frequency'] = data['wage_frequency'].astype(float)
    data['wage_frequency'] = data['wage_frequency'].apply(lambda x: np.nan if x == 9 else x)
    data = data.dropna(subset=['wage_frequency'])

    # Monthly Wage (Mexican pesos)
    data['monthly_wage'] = 0
    data.loc[data['wage_frequency'] == 1, 'monthly_wage'] = data['wage'] * 4
    data.loc[data['wage_frequency'] == 2, 'monthly_wage'] = data['wage'] * 2
    data.loc[data['wage_frequency'] == 3, 'monthly_wage'] = data['wage']
    data.loc[data['wage_frequency'] == 4, 'monthly_wage'] = data['wage'] / 12
    data.loc[data['wage_frequency'].isna(), 'monthly_wage'] = np.nan
    data.loc[data['wage'].isna(), 'monthly_wage'] = np.nan
    data['wage_frequency'] = data['wage_frequency'].apply(lambda x: np.nan if x == 0 else x)
    data = data.dropna(subset=['monthly_wage'])

    # Percentage of Wage used to payments
    data['payment_percentage'] = (data['monthly_payments'] / data['monthly_wage']) * 100

    # Users age (Categorical)
    data = data.rename(columns={'EDAD': 'age'})
    data['age'] = data['age'].apply(lambda x: np.nan if x >= 97 else x)
    data = data.dropna(subset=['age'])

    # Woman (Dummy)
    data['woman'] = 0
    data.loc[data['SEXO'] == 1, 'woman'] = 1
    data = data.dropna(subset=['woman'])

    # Civil Status (Categorical)
    data = data.rename(columns={'P2_8': 'civil_status'})
    data['civil_status'] = data['civil_status'].apply(lambda x: np.nan if x == 'NA' else x)
    data['civil_status'] = data['civil_status'].astype(float)
    data = data.dropna(subset=['civil_status'])

    # Zone mapping
    zone_mapping = {
        1: "North Central",
        2: "North",
        3: "Northwest",
        4: "South",
        5: "North",
        6: "North Central",
        7: "South",
        8: "North",
        9: "Central",
        10: "Northwest",
        11: "Central",
        12: "South",
        13: "Central",
        14: "North Central",
        15: "Central",
        16: "North Central",
        17: "Central",
        18: "Northwest",
        19: "North",
        20: "South",
        21: "Central",
        22: "Central",
        23: "South",
        24: "North Central",
        25: "Northwest",
        26: "North",
        27: "South",
        28: "North",
        29: "Central",
        30: "South",
        31: "South",
        32: "Northwest"
    }

    # Assign values to the 'zone' column using the mapping dictionary
    data['zone'] = 0
    data['zone'] = data['ENT'].astype(int).map(zone_mapping)
    data = data.dropna(subset=['zone'])

    data = data.rename(columns={'ENT': 'federal_entity'})

    data = data[[col for col in data.columns if not col.startswith('P')]]

    data = data[[col for col in data.columns if not col.isupper()]]

    return data
