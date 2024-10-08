import joblib
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import sys
sys.setrecursionlimit(5000)

def return_prediction(model, scaler, sample_json):
    id = sample_json['ID']
    pin = sample_json['Pin-code']
    age = sample_json['age']
    fm = sample_json['Fam members']
    edu = sample_json['Education']
    exp = sample_json['T.Experience']
    inc = sample_json['Income']
    mo = sample_json['Mortgage']
    fd = sample_json['Fixed Deposit']
    de = sample_json['Demat']
    nb = sample_json['Net Banking']
    dc = [[id, pin, age, fm, edu, exp, inc, mo, fd, de, nb]]
    dc = scaler.transform(dc)
    predictions = model.predict(dc)
    return predictions

# Load the scaler and model
scaler = joblib.load("C:\\Users\\Suyash Pandey\\PycharmProjects\\LOAN_CAMPAIGN\\scaler.joblib", "rb")
model = load_model("Loan_Predictor_2.joblib")

# Streamlit interface
st.title("Loan Provider")

id = st.number_input("Enter the ID of Customer (e.g., 10001)", min_value=0, step=1)
pin = st.number_input("Enter the Pin-code of Customer (e.g., 110001)", min_value=0, step=1)
age = st.number_input("Enter the age of Customer", min_value=18, max_value=100, step=1)
fm = st.number_input("Enter the number of Family Members in customer family", min_value=1, step=1)
edu = st.number_input("Enter the education level of the customer (1: not graduate, 2: undergraduate, 3: graduate, 4: post graduate)", min_value=0, max_value=2, step=1)
exp = st.number_input("Enter the total experience (years) of the customer in the industry", min_value=0, step=1)
inc = st.number_input("Enter the income (annual) of the customer", min_value=0.0, step=1000.0, format="%.2f")
mo = st.number_input("Enter Mortgage (if any)", min_value=0.0, step=1000.0, format="%.2f")
fd = st.number_input("Fixed Deposit (if any, 1: yes, 0: no)", min_value=0.0, step=1000.0, format="%.2f")
de = st.number_input("Demat Account (1: yes, 0: no)", min_value=0, max_value=1, step=1)
nb = st.number_input("Net Banking (1: yes, 0: no)", min_value=0, max_value=1, step=1)

if st.button('Predict'):
    # Prepare input data
    sample_input = np.array([[id, pin, age, fm, edu, exp, inc, mo, fd, de, nb]])
    dc_scaled = scaler.transform(sample_input)
    prediction = model.predict(dc_scaled)
    if prediction == 1:
        st.header("Loan has been successfully given to the customer")
    else:
        st.header("Bank failed in luring the customer")
