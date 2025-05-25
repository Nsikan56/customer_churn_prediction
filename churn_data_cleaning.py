import pandas as pd

def clean_churn_data(filepath):
    """
    Loads and cleans the Telco Customer Churn dataset.

    Parameters:
    filepath (str): Path to the CSV file.

    Returns:
    pd.DataFrame: Cleaned and encoded dataset ready for modeling.
    """
    # Load the dataset
    df = pd.read_csv(filepath)

    # Convert TotalCharges to numeric, coercing errors from empty strings
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(" ", pd.NA), errors='coerce')

    # Drop rows with missing TotalCharges
    df = df.dropna(subset=['TotalCharges'])

    # Drop customerID (not predictive)
    df = df.drop(columns=['customerID'])

    # Convert SeniorCitizen from int to categorical string
    df['SeniorCitizen'] = df['SeniorCitizen'].replace({1: 'Yes', 0: 'No'})

    # Convert target variable Churn to binary
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

    # Identify categorical columns
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    # One-hot encode categorical variables
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    return df_encoded

# usage:
# df_clean = clean_churn_data('WA_Fn-UseC_-Telco-Customer-Churn.csv')
