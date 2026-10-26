import streamlit as st
import pickle
import pandas as pd

# 1. Load the machine learning engine artifact
with open('credit_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Professional Header Presentation
st.title("🛡️ AI Micro-Lending Underwriting Engine")
st.write("Alternative credit scoring mechanism for unbanked small business enterprises (SMEs).")

st.markdown("---")

# 2. Financial Metrics Data Gathering Input Fields
sales = st.slider(
    "Average Monthly Sales / SBP Revenue Tier", 
    min_value=10000, 
    max_value=500000, 
    value=150000, 
    step=5000,
    format="%d PKR"
)

missed_bills = st.slider(
    "Number of Missed Utility Bill Payments (Past 12 Months)", 
    min_value=0, 
    max_value=12, 
    value=0 # Default to 0 to test clean approval parameters easily
)

st.markdown("---")

# 3. Dynamic Matrix Score Computation Execution
if st.button("Run Underwriting Risk Assessment"):
    # Structuring data matrix layout matching model expected parameters
    input_data = pd.DataFrame([[sales, missed_bills]], columns=['monthly_sales', 'missed_utility_bills'])
    
    # Executing calculation matrix
    prediction = model.predict(input_data)
    prob_val = model.predict_proba(input_data) 
    
    # FIXED INDEX: Extract structural value safely from scikit-learn probability matrix row 0, col 1
    raw_score = float(prob_val[0][1]) * 100
    
    # Underwriting Overrides (Business Rules & Risk Mitigations)
    if missed_bills >= 6:
        confidence_score = min(raw_score, 35.0)  # Heavy penalty constraint for chronic default indicators
    elif missed_bills >= 3:
        confidence_score = min(raw_score, 65.0)  # Moderate constraint rule threshold
    else:
        confidence_score = raw_score             # Clean background profile maps unpenalized scores

    # Calculating Cap limits based on your custom underwriting policy parameters
    if sales < 100000:
        max_loan_allowed = sales * 6
        tier_rationale = "Max loan tier capped at 6 months of revenue (Sales < 100,000 PKR)."
    elif sales <= 200000:
        max_loan_allowed = sales * 12
        tier_rationale = "Max loan tier capped at 12 months of revenue (Sales <= 200,000 PKR)."
    else: # 3 Lac+ category (Sales > 200k up into premium categories)
        max_loan_allowed = 10000000 # 1 Crore PKR limit
        tier_rationale = "Premium tier qualification (Sales > 200,000 PKR). Maximum line ceiling extended up to 1 Crore PKR."

    st.subheader("Evaluation Analysis & Results")
    
    # Final Output Logic Mapping Engine Decision Thresholds
    if confidence_score >= 70.0:
        st.success(f"🎉 **RISK STATUS: LOAN APPROVED** \n\n**Calculated Repayment Confidence Score:** {confidence_score:.2f}%")
        
        # Displaying tailored maximum lines dynamically matching your limits
        st.metric(label="Maximum Credit Exposure Line Allowed", value=f"{max_loan_allowed:,} PKR")
        st.info(f"📋 **Underwriting Policy Notes:** {tier_rationale}\n\n💡 **Product Terms:** 24% Fixed APR micro-credit line.")
    else:
        st.error(f"❌ **RISK STATUS: LOAN REJECTED** \n\n**Calculated Repayment Confidence Score:** {confidence_score:.2f}%")
        st.warning(f"⚠️ **Risk Flag:** The applicant has {missed_bills} missed utility payments. High operational delinquencies imply elevated default risk.")
        st.metric(label="Maximum Credit Line Approved", value="0 PKR (Exposure Restricted)")

      
