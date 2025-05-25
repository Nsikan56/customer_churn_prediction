import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model
model = joblib.load("churn_model.pkl")

st.title("Telecom Customer Churn Predictor")
st.markdown("Enter customer details below to predict churn likelihood.")

# Input form
gender = st.selectbox("Gender", ["Male", "Female"])
senior = st.selectbox("Senior Citizen", ["Yes", "No"])
partner = st.selectbox("Has Partner?", ["Yes", "No"])
dependents = st.selectbox("Has Dependents?", ["Yes", "No"])
tenure = st.slider("Tenure (months)", 0, 72)
monthly_charges = st.number_input("Monthly Charges", 0.0, 150.0, 70.0)
total_charges = st.number_input("Total Charges", 0.0, 10000.0, 3000.0)
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

# TODO: add more fields later...

if st.button("Predict Churn"):
    # Create input row and preprocess it to match model input
    input_dict = {
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "gender_Male": 1 if gender == "Male" else 0,
        "SeniorCitizen_Yes": 1 if senior == "Yes" else 0,
        "Partner_Yes": 1 if partner == "Yes" else 0,
        "Dependents_Yes": 1 if dependents == "Yes" else 0,
        "Contract_One year": 1 if contract == "One year" else 0,
        "Contract_Two year": 1 if contract == "Two year" else 0,
        # other columns should be filled as 0/default
    }

    df_input = pd.DataFrame([input_dict])
    df_input = df_input.reindex(columns=model.feature_names_in_, fill_value=0)

    # Predict
    proba = model.predict_proba(df_input)[0][1]
    st.success(f"Churn Risk: {proba:.2%}")
