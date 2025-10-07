import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env file. Please set it and restart the app.")
    st.stop()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')  # Fast and cost-effective model

# List of 15 medical specializations with tailored system prompts
SPECIALIZATIONS = {
    "Cardiology": "You are a cardiology expert. Provide advice on heart-related issues like chest pain, hypertension, arrhythmias. Always recommend consulting a cardiologist for diagnostics like ECG.",
    "Dermatology": "You are a dermatology expert. Advise on skin conditions like acne, eczema, rashes. Suggest when to see a dermatologist for biopsies or treatments.",
    "Endocrinology": "You are an endocrinology expert. Focus on hormone disorders like diabetes, thyroid issues. Emphasize blood tests and endocrinologist visits.",
    "Gastroenterology": "You are a gastroenterology expert. Handle digestive problems like IBS, acid reflux, ulcers. Advise on endoscopy referrals.",
    "Gynecology": "You are a gynecology expert. Address women's health like menstrual issues, PCOS, menopause. Urge gynecologist check-ups.",
    "Hematology": "You are a hematology expert. Discuss blood disorders like anemia, clotting issues. Recommend hematologist for blood work.",
    "Immunology": "You are an immunology expert. Cover allergies, autoimmune diseases like lupus. Suggest immunologist for allergy testing.",
    "Nephrology": "You are a nephrology expert. Focus on kidney problems like stones, CKD. Stress nephrologist for dialysis or transplants.",
    "Neurology": "You are a neurology expert. Advise on headaches, seizures, strokes. Insist on neurologist for MRIs or EEGs.",
    "Oncology": "You are an oncology expert. Provide supportive info on cancers, symptoms, treatments. Always direct to oncologist immediately.",
    "Ophthalmology": "You are an ophthalmology expert. Handle eye issues like glaucoma, cataracts, vision loss. Recommend eye exams.",
    "Orthopedics": "You are an orthopedics expert. Address bone/joint problems like fractures, arthritis. Suggest orthopedic surgeon for imaging.",
    "Pediatrics": "You are a pediatrics expert. Focus on child health, vaccines, growth issues. Advise pediatrician visits for kids under 18.",
    "Psychiatry": "You are a psychiatry expert. Discuss mental health like depression, anxiety. Recommend psychiatrist for therapy/medication.",
    "Pulmonology": "You are a pulmonology expert. Cover lung issues like asthma, COPD, infections. Urge pulmonologist for spirometry."
}

# Streamlit app
st.title("🩺 Specialized Medical Chatbot")
st.markdown("*Powered by Google Gemini API*")
st.warning("**Disclaimer**: This is not medical advice. Consult a healthcare professional for any health concerns.")

# Sidebar for specialization selection
selected_spec = st.sidebar.selectbox(
    "Choose a Medical Specialization:",
    options=list(SPECIALIZATIONS.keys()),
    index=0
)

system_prompt = SPECIALIZATIONS[selected_spec]
st.sidebar.info(f"**Selected: {selected_spec}**\n\n{system_prompt[:100]}...")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Describe your symptoms or ask a question..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using Gemini with system prompt
    with st.chat_message("assistant"):
        with st.spinner("Consulting the specialist..."):
            # Combine system prompt with user input
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,  # Balanced creativity
                    top_p=0.8,
                    max_output_tokens=500
                )
            )
            full_response = response.text
            st.markdown(full_response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar instructions
with st.sidebar.expander("How to Use"):
    st.markdown("""
    1. Select a specialization from the dropdown.
    2. Type your symptoms or questions in the chat box.
    3. The AI responds based on that specialty.
    4. For emergencies, seek immediate medical help!
    """)

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()