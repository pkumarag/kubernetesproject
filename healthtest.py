import streamlit as st
import requests

# API Configuration
BASE_URL = "https://api.endlessmedical.com/v1/dx"

st.set_page_config(page_title="SafeDiag Medical Bot", page_icon="⚕️")
st.title("⚕️ SafeDiag Clinical Assistant")
st.caption("Powered by EndlessMedical Clinical Logic")

# 1. Initialize Session (Required by EndlessMedical)
if 'session_id' not in st.session_state:
    response = requests.get(f"{BASE_URL}/InitSession")
    if response.status_code == 200:
        st.session_state.session_id = response.json().get("SessionID")

# 2. User Input
st.info("Note: This bot uses structured clinical data. Use terms like 'Cough', 'Fever', or 'Headache'.")
user_symptom = st.text_input("Enter a primary symptom:")

if st.button("Analyze Symptoms"):
    if user_symptom:
        sid = st.session_state.session_id
        
        # Step A: Accept Terms (Required for analysis)
        requests.post(f"{BASE_URL}/AcceptTermsOfUse?SessionID={sid}&passphrase=I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and EndlessMedical services.")
        
        # Step B: Update Feature (Adding the symptom to your session)
        # Note: In a full app, you'd map "Fever" to the API's internal feature names
        requests.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name={user_symptom}&value=5") # Value 5 = Moderate/Present
        
        # Step C: Get Analysis
        analysis_res = requests.get(f"{BASE_URL}/Analyze?SessionID={sid}")
        
        if analysis_res.status_code == 200:
            data = analysis_res.json()
            st.subheader("Clinical Analysis")
            if data.get("status") == "ok":
                # Display results (The API returns diseases and their probabilities)
                st.write("Potential conditions based on clinical data:")
                st.json(data.get("Diseases", {})) 
            else:
                st.error("The API could not find a match for that specific term.")
    else:
        st.warning("Please enter a symptom.")

st.divider()
st.warning("**Disclaimer:** This is a demonstration. Always consult a human doctor before taking any medication.")
