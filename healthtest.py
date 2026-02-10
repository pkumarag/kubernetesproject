import streamlit as st
import requests
import urllib3

# 1. Force-disable all SSL warnings to keep the UI clean
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BASE_URL = "https://api.endlessmedical.com/v1/dx"

# Create a global session that ignores SSL
session = requests.Session()
session.verify = False 

st.set_page_config(page_title="Physician AI", page_icon="⚕️")
st.title("⚕️ Physician Assistant Bot")

# 2. Collect Essential Medical Data (Required by API)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
with col2:
    gender = st.selectbox("Gender", ["Male", "Female"])

symptom_input = st.text_input("Enter symptom (e.g., headache, fever, cough):").lower()

# Mapping common terms
SYMPTOM_MAP = {"headache": "Headache", "fever": "Temp", "cough": "Cough", "stomach ache": "AbdominalPain"}

if st.button("Generate Prescription/Advice"):
    if symptom_input in SYMPTOM_MAP:
        try:
            # Step A: Initialize Session
            init_res = session.get(f"{BASE_URL}/InitSession")
            sid = init_res.json().get("SessionID")
            
            # Step B: Accept Terms
            terms = "I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and EndlessMedical services."
            session.post(f"{BASE_URL}/AcceptTermsOfUse?SessionID={sid}&passphrase={terms}")
            
            # Step C: Update Features (Age, Gender, and Symptom)
            session.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name=Age&value={age}")
            session.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name=Gender&value=2" if gender == "Female" else f"{BASE_URL}/UpdateFeature?SessionID={sid}&name=Gender&value=1")
            session.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name={SYMPTOM_MAP[symptom_input]}&value=5")
            
            # Step D: Analyze
            analysis = session.get(f"{BASE_URL}/Analyze?SessionID={sid}").json()
            
            if analysis.get("status") == "ok":
                st.success("Analysis Complete")
                st.subheader("Potential Conditions:")
                for disease, prob in analysis.get("Diseases", {}).items():
                    st.write(f"- **{disease}**: {prob}")
            else:
                st.error("The API could not process this clinical data.")
                
        except Exception as e:
            st.error(f"System Error: {e}")
    else:
        st.warning("Please enter a recognized symptom like 'fever'.")
