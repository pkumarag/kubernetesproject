import streamlit as st

st.set_page_config(page_title="AI Medical Triage", page_icon="⚕️")

# --- UI Header ---
st.title("⚕️ Physician Triage Assistant")
st.markdown("""
This assistant helps categorize your symptoms and provides general guidance.
**Note:** This is not a diagnosis. In an emergency, call **911** (or your local emergency number).
""")

# --- Patient Data ---
with st.sidebar:
    st.header("Patient Profile")
    age = st.number_input("Age", 1, 120, 30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    pre_existing = st.multiselect("Conditions", ["Diabetes", "Hypertension", "Asthma", "None"])

# --- Symptom Analysis ---
symptom = st.text_input("Describe your symptoms (e.g., 'Sharp chest pain', 'Mild fever and cough')")

if st.button("Analyze & Get Guidance"):
    if not symptom:
        st.warning("Please enter your symptoms first.")
    else:
        st.subheader("Assessment Result")
        
        # LOGIC: Emergency Red Flags (Always check these first)
        red_flags = ["chest pain", "difficulty breathing", "heavy bleeding", "confusion", "slurred speech"]
        is_emergency = any(flag in symptom.lower() for flag in red_flags)
        
        if is_emergency:
            st.error("🚨 **URGENT: SEEK EMERGENCY CARE IMMEDIATELY**")
            st.write("Your symptoms suggest a potentially life-threatening condition.")
        else:
            # Simulated Triage logic based on 2026 Medical Standards
            st.info("📊 **Triage Level: Moderate / Non-Urgent**")
            
            st.markdown(f"""
            **Potential Causes to Discuss with a Doctor:**
            - Viral Infection (Common Cold/Flu)
            - Tension-related discomfort
            
            **Suggested Next Steps:**
            1. **Rest & Hydration:** Most mild symptoms improve with 24-48 hours of rest.
            2. **Monitor:** If fever exceeds 103°F (39.4°C), seek medical attention.
            3. **Schedule:** Book a non-emergency appointment via Telehealth.
            """)
            
            # Simulated Medication Guidance (Standard OTC)
            with st.expander("Typical Over-the-Counter (OTC) Guidance"):
                st.write("""
                *For fever/pain:* Paracetamol (Acetaminophen) or Ibuprofen. 
                *Always check the label for dosage and consult a pharmacist if you are taking other medications.*
                """)

# --- Feedback Loop ---
st.divider()
if st.button("Reset Session"):
    st.rerun()
