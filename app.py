import streamlit as st
import pickle
import pandas as pd

# 1. Load the AI brain we created in Step 3
with open('credit_model.pkl', 'rb') as file:
    model = pickle.load(file)

st.title("AI Micro Lending Risk Engine")
st.write("This portal uses alternative underwriting data to score unbanked small business owners.")

# 2. Create the input fields for the user
sales = st.slider(
    "Average Monthly Sales", 
    min_value=10000, 
    max_value=500000, 
    value=50000, 
    step=5000,
    format="%d PKR"
)

missed_bills = st.slider(
    "Number of missed utility bills (Last 12 Months)", 
    min_value=0, 
    max_value=12, 
    value=1
)

# 3. Run the prediction when the button is clicked
if st.button("Assess Credit Eligibility"):
    input_data = pd.DataFrame([[sales, missed_bills]], columns=['monthly_sales', 'missed_utility_bills'])
    
    # Get raw model outputs
    prediction = model.predict(input_data)
    prob_val = model.predict_proba(input_data) 
    
    # Crucial Fix: Safely extract the plain number from the model's array structure
    confidence_score = float(prob_val[0][1]) * 100
    
    # Financial Rule Safeguard: High-risk behavior overrides
    if missed_bills >= 6:
        # Forces a low score and direct rejection for missing half a year or more of utility bills
        if confidence_score > 35.0:
            confidence_score = 35.0
    elif missed_bills >= 3:
        # Forces a borderline score for multiple missed bills
        if confidence_score > 65.0:
            confidence_score = 65.0

    st.subheader("Evaluation Results")
    
    # Determine approval status based on safeguarded score
    if confidence_score >= 70.0:
        st.success(f"🎉 LOAN APPROVED! \n\n**Repayment Confidence Score:** {confidence_score:.2f}%")
        st.info("💡 **Recommended terms:** 24% APR micro-credit line.")
    else:
        st.error(f"❌ LOAN REJECTED \n\n**Repayment Confidence Score:** {confidence_score:.2f}%")
        st.warning("⚠️ **Risk Factor:** High number of missed utility payments indicates elevated credit risk.")

   
