import streamlit as st
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# UPDATED: Use the primary production URL
BASE_URL = "https://api.endlessmedical.com/v1/dx"

st.set_page_config(page_title="Physician AI 2026", page_icon="⚕️")
st.title("⚕️ Physician Assistant Bot")

# Helper for API calls
def call_api(method, endpoint, params=None):
    try:
        url = f"{BASE_URL}/{endpoint}"
        # We use verify=False to bypass the SSL issue on Streamlit Cloud
        response = method(url, params=params, verify=False, timeout=10)
        if response.status_code == 404:
            return None, "Error 404: Endpoint not found. The API may have moved."
        return response.json(), None
    except Exception as e:
        return None, str(e)

# 1. Init Session
if 'sid' not in st.session_state:
    data, err = call_api(requests.get, "InitSession")
    if data and "SessionID" in data:
        st.session_state.sid = data["SessionID"]
        # Immediately Accept Terms (Required for all further calls)
        terms = "I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and EndlessMedical services."
        requests.post(f"{BASE_URL}/AcceptTermsOfUse?SessionID={st.session_state.sid}&passphrase={terms}", verify=False)
    else:
        st.error(f"Could not connect to medical server: {err}")

# 2. Input UI
symptom = st.selectbox("Select a Symptom", ["Headache", "Temp", "Cough", "AbdominalPain", "SoreThroat"])
age = st.number_input("Patient Age", 1, 100, 25)

if st.button("Analyze"):
    sid = st.session_state.sid
    # Update Age
    requests.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name=Age&value={age}", verify=False)
    # Update Symptom (Value 5 = Present)
    requests.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name={symptom}&value=5", verify=False)
    
    # Get Analysis
    analysis, err = call_api(requests.get, "Analyze", params={"SessionID": sid})
    
    if analysis and analysis.get("status") == "ok":
        st.subheader("Potential Diagnoses")
        for disease, prob in analysis.get("Diseases", {}).items():
            st.write(f"**{disease}**: {prob}")
    else:
        st.error(f"Analysis failed: {err}")

if st.button("Reset"):
    st.session_state.clear()
    st.rerun()
