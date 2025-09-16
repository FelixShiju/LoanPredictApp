"""
Created on Mon Sep 16 2025
@author: Felix
"""

import pickle
import streamlit as st

# ================= LOAD MODEL ==================
loan_model = pickle.load(open("loan_model.sav", "rb"))

# ================= STREAMLIT UI =================
st.set_page_config(page_title="Loan Prediction System", page_icon="💰", layout="centered")

st.title("💰 Loan Approval Prediction System")
st.markdown("___Fill in applicant details to check loan approval status.___")

# ================= INPUT FORM =================
col1, col2 = st.columns(2)

with col1:
    Gender = st.radio("👤 Gender", ["Male", "Female"])
    Married = st.radio("💍 Married", ["Yes", "No"])
    Dependents = st.radio("👶 Dependents", ["0", "1", "2", "3+"])  # "3+" must be mapped to 4
    Education = st.radio("🎓 Education", ["Graduate", "Not Graduate"])
    Self_Employed = st.radio("💼 Self Employed", ["Yes", "No"])

with col2:
    ApplicantIncome = st.number_input("💵 Applicant Income", min_value=0, step=100)
    CoapplicantIncome = st.number_input("💵 Co-applicant Income", min_value=0, step=100)
    LoanAmount = st.number_input("🏦 Loan Amount (in thousands)", min_value=0, step=1)
    Loan_Amount_Term = st.selectbox("📆 Loan Amount Term (months)", [360, 180, 120, 60])
    Credit_History = st.radio("📊 Credit History", ["1 = Good", "0 = Bad"])
    Property_Area = st.selectbox("🏠 Property Area", ["Urban", "Semiurban", "Rural"])

# ================= PREDICTION =================
if st.button("🔍 Predict Loan Approval"):
    # Encoding categorical values (same as training preprocessing)
    Gender = 1 if Gender == "Male" else 0
    Married = 1 if Married == "Yes" else 0
    Dependents = 4 if Dependents == "3+" else int(Dependents)
    Education = 1 if Education == "Graduate" else 0
    Self_Employed = 1 if Self_Employed == "Yes" else 0
    Credit_History = int(Credit_History[0])  # "1 = Good" → 1, "0 = Bad" → 0
    Property_Area = {"Rural": 0, "Semiurban": 1, "Urban": 2}[Property_Area]

    # Arrange inputs in the same order as training dataset (X)
    input_data = [[Gender, Married, Dependents, Education, Self_Employed,
                   ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term,
                   Credit_History, Property_Area]]

    # Prediction
    prediction = loan_model.predict(input_data)

    if prediction[0] == 1:
        st.success("✅ Loan is **Approved**!")
    else:
        st.error("❌ Loan is **Not Approved**.")



