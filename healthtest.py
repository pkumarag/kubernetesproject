import streamlit as st
import requests
import urllib3

# 1. Disable the SSL warnings so they don't clutter your app
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BASE_URL = "https://api.endlessmedical.com/v1/dx"

# Mapping common terms to API-recognized features
SYMPTOM_MAP = {
    "stomach ache": "AbdominalPain",
    "fever": "Temp",
    "cough": "Cough",
    "headache": "Headache",
    "sore throat": "SoreThroat"
}

st.set_page_config(page_title="SafeDiag AI - No SSL", page_icon="⚕️")
st.title("⚕️ Physician Assistant Bot")
st.caption("SSL Verification: Disabled for Compatibility")

# 2. Initialize Session
if 'session_id' not in st.session_state:
    try:
        # Use verify=False to bypass the SSL error
        res = requests.get(f"{BASE_URL}/InitSession", verify=False)
        st.session_state.session_id = res.json().get("SessionID")
    except Exception as e:
        st.error(f"Connection Failed: {e}")

user_input = st.text_input("Enter symptom (fever, cough, headache, etc.):").lower()

if st.button("Start Consultation"):
    if user_input in SYMPTOM_MAP:
        sid = st.session_state.session_id
        feature = SYMPTOM_MAP[user_input]
        
        # Step A: Accept Terms (verify=False)
        terms_text = "I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and EndlessMedical services."
        requests.post(f"{BASE_URL}/AcceptTermsOfUse?SessionID={sid}&passphrase={terms_text}", verify=False)
        
        # Step B: Update Symptom (verify=False)
        requests.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name={feature}&value=5", verify=False)
        
        # Step C: Analyze (verify=False)
        analysis_res = requests.get(f
