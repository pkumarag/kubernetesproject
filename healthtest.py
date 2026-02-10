import streamlit as st
import requests
import certifi

# Configuration
BASE_URL = "https://api.endlessmedical.com/v1/dx"

# Simple mapping dictionary to bridge user language to API features
SYMPTOM_MAP = {
    "stomach ache": "AbdominalPain",
    "fever": "Temp",
    "cough": "Cough",
    "headache": "Headache",
    "sore throat": "SoreThroat"
}

st.set_page_config(page_title="SafeDiag AI", page_icon="⚕️")
st.title("⚕️ Physician Consultation Assistant")

# Initialize Session
if 'session_id' not in st.session_state:
    # Use certifi.where() to fix the SSLError
    res = requests.get(f"{BASE_URL}/InitSession", verify=certifi.where())
    st.session_state.session_id = res.json().get("SessionID")

user_input = st.text_input("Describe your symptom (e.g., fever, stomach ache):").lower()

if st.button("Consult"):
    if user_input in SYMPTOM_MAP:
        sid = st.session_state.session_id
        feature = SYMPTOM_MAP[user_input]
        
        # 1. Accept Terms
        terms_url = f"{BASE_URL}/AcceptTermsOfUse?SessionID={sid}&passphrase=I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and EndlessMedical services."
        requests.post(terms_url, verify=certifi.where())
        
        # 2. Add Symptom (Value 5 = Present/Moderate)
        requests.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name={feature}&value=5", verify=certifi.where())
        
        # 3. Analyze
        analysis = requests.get(f"{BASE_URL}/Analyze?SessionID={sid}", verify=certifi.where()).json()
        
        if analysis.get("status") == "ok":
            st.subheader("Potential Assessments")
            # The API returns a dictionary of conditions and probabilities
            for disease, probability in analysis.get("Diseases", {}).items():
                st.write(f"**{disease}**: {probability}")
        else:
            st.error("Diagnostic engine error. Please try a different symptom.")
    else:
        st.warning("Please try: fever, cough, or stomach ache (Mapping dictionary is limited).")

st.info("💡 Tip: In a real app, you would use a 'GetFeatures' loop to map all 800+ symptoms.")
