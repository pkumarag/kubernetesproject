import streamlit as st
import openai

# Configuration
st.set_page_config(page_title="Med-Assist AI", page_icon="⚕️")
st.title("⚕️ Physician Assistant -Created By Pankaj")

# Legal Disclaimer
st.warning("DISCLAIMER: This tool is for informational purposes only. It is NOT a substitute for professional medical advice.")

# User Input
symptoms = st.text_area("Describe your symptoms in detail:", placeholder="e.g., I have a sharp pain in my lower back and a mild fever...")

if st.button("Get Analysis"):
    if symptoms:
        with st.spinner('Consulting medical database...'):
            # The prompt is key: it must force the AI to be cautious
            prompt = f"""
            System: You are a medical triage assistant. Analyze the symptoms provided.
            1. Suggest the most likely conditions.
            2. Suggest typical Over-The-Counter (OTC) treatments if applicable.
            3. CRITICAL: List 'Red Flags' that require an Emergency Room visit.
            4. State clearly that this must be confirmed by a doctor.
            
            User Symptoms: {symptoms}
            """
            # Call your LLM API here
            # response = openai.ChatCompletion.create(...)
            st.subheader("Potential Assessment")
            st.write("Based on your symptoms, you may be experiencing [Condition].")
            st.info("Suggested next step: Consult a General Physician for a physical exam.")
    else:
        st.error("Please enter symptoms to continue.")
