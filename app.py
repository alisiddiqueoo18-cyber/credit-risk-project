import streamlit as st
import pandas as pd
import pickle

# # 1. Load the AI brain we created in Step 3
with open('credit_model.pkl', 'rb') as file:
    model = pickle.load(file)

st.title("AI Micro Lending Risk Engine")
st.write("This portal uses alternative underwriting data to score unbanked small business owners.")

# # 2. Create the input fields for the user
sales = st.slider("Average Monthly Sales (PKR / $)", 10000, 500000, 50000)
missed_bills = st.slider("Number of Missed Utility Bills (Last 12 Months)", 0, 12, 1)

# # 3. Run the prediction when the button is clicked
if st.button("Assess Credit Eligibility"):
    input_data = pd.DataFrame([[sales, missed_bills]], columns=['monthly_sales', 'missed_utility_bills'])
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]
    
    st.subheader("Evaluation Results")
    if prediction[0] == 1:
        st.success(f"LOAN APPROVED! Repayment Confidence Score: {probability*100:.2f}%")
        st.info("Recommended terms: 24% APR micro-credit line.")
    else:
        st.error(f"LOAN REJECTED. Default risk too high (Confidence: {probability*100:.2f}%)")
