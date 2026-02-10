import streamlit as st
import requests
import urllib3

# Disable SSL warnings for the bypass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# The production-grade endpoint is often more stable
BASE_URL = "https://api-prod.endlessmedical.com/v1/dx"

st.set_page_config(page_title="Physician AI Assistant", page_icon="⚕️")
st.title("⚕️ Physician Assistant Bot")

# Sidebar for basic health data (Required for accurate API results)
st.sidebar.header("Patient Profile")
age = st.sidebar.slider("Age", 1, 100, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

# Symptom Mapping
SYMPTOM_MAP = {
    "headache": "Headache",
    "fever": "Temp",
    "cough": "Cough",
    "stomach ache": "AbdominalPain"
}

def safe_api_call(method, url, **kwargs):
    """Helper to handle empty or non-JSON responses gracefully"""
    try:
        # We always use verify=False here to bypass the SSL error
        response = method(url, verify=False, timeout=10, **kwargs)
        if response.status_code != 200:
            return None, f"Server returned error code {response.status_code}"
        if not response.text.strip():
            return None, "Server returned an empty response."
        return response.json(), None
    except Exception as e:
        return None, str(e)

# Initialize Session
if 'session_id' not in st.session_state:
    data, err = safe_api_call(requests.get, f"{BASE_URL}/InitSession")
    if data and data.get("SessionID"):
        st.session_state.session_id = data.get("SessionID")
    else:
        st.error(f"Could not start session: {err}")

user_input = st.text_input("Describe your symptom:").lower()

if st.button("Analyze & Prescribe Guidance"):
    if user_input in SYMPTOM_MAP and 'session_id' in st.session_state:
        sid = st.session_state.session_id
        
        # Step 1: Accept Terms
        terms = "I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and EndlessMedical services."
        safe_api_call(requests.post, f"{BASE_URL}/AcceptTermsOfUse?SessionID={sid}&passphrase={terms}")
        
        # Step 2: Update Age & Gender (Value 1=Male, 2=Female)
        g_val = "1" if gender == "Male" else "2"
        safe_api_call(requests.post, f"{BASE_URL}/UpdateFeature?SessionID={sid}&name=Age&value={age}")
        safe_api_call(requests.post, f"{BASE_URL}/UpdateFeature?SessionID={sid}&name=Gender&value={g_val}")
        
        # Step 3: Add Symptom
        safe_api_call(requests.post, f"{BASE_URL}/UpdateFeature?SessionID={sid}&name={SYMPTOM_MAP[user_input]}&value=5")
        
        # Step 4: Analyze
        analysis, err = safe_api_call(requests.get, f"{BASE_URL}/Analyze?SessionID={sid}")
        
        if analysis and analysis.get("status") == "ok":
            st.subheader("Clinical Assessment")
            results = analysis.get("Diseases", [])
            if results:
                for disease in results:
                    # Disease format is often [Name, Probability]
                    st.write(f"- **{disease[0]}**: {disease[1]} probability")
                st.info("Typical medication for these symptoms may include OTC pain relief or rest. Consult a doctor for a formal prescription.")
            else:
                st.write("No specific conditions matched. Please provide more symptoms.")
        else:
            st.error(f"Analysis failed: {err}")
    else:
        st.warning("Please enter a known symptom (e.g., headache, fever).")
