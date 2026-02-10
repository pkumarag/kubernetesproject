import streamlit as st
import requests
import urllib3

# 1. Silence SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 2. UPDATED ENDPOINT: Use the base domain directly
# Some Streamlit environments prefer the non-prod or specific v1 path
BASE_URL = "https://api.endlessmedical.com/v1/dx"

st.set_page_config(page_title="Physician AI", page_icon="⚕️")
st.title("⚕️ Physician Assistant Bot")

# --- INITIALIZATION ---
# We check 'sid' in session_state so we don't call the API on every click
if 'sid' not in st.session_state:
    try:
        # Try to initialize session
        res = requests.get(f"{BASE_URL}/InitSession", verify=False, timeout=5)
        if res.status_code == 200:
            data = res.json()
            st.session_state.sid = data.get("SessionID")
            
            # Auto-accept terms immediately
            terms = "I have read, understood and I accept and agree to comply with the Terms of Use of EndlessMedicalAPI and EndlessMedical services."
            requests.post(f"{BASE_URL}/AcceptTermsOfUse?SessionID={st.session_state.sid}&passphrase={terms}", verify=False)
        else:
            st.error(f"Medical Server Error ({res.status_code}). Please try again later.")
    except Exception as e:
        st.error(f"Connection Failed: {e}")

# --- USER INTERFACE ---
symptom = st.selectbox("Select Symptom", ["Headache", "Temp", "Cough", "AbdominalPain"])
age = st.number_input("Age", 1, 100, 25)

if st.button("Analyze"):
    # SAFETY CHECK: Only run if sid exists
    if 'sid' in st.session_state:
        sid = st.session_state.sid
        try:
            # 1. Send Age
            requests.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name=Age&value={age}", verify=False)
            # 2. Send Symptom
            requests.post(f"{BASE_URL}/UpdateFeature?SessionID={sid}&name={symptom}&value=5", verify=False)
            
            # 3. Get Result
            analysis = requests.get(f"{BASE_URL}/Analyze?SessionID={sid}", verify=False).json()
            
            if analysis.get("status") == "ok":
                st.subheader("Results")
                st.write(analysis.get("Diseases", "No specific match found."))
            else:
                st.error("Analysis Error: Check your inputs.")
        except Exception as e:
            st.error(f"Error during analysis: {e}")
    else:
        st.error("Session not initialized. Please refresh the page.")

if st.button("Clear & Restart"):
    st.session_state.clear()
    st.rerun()
