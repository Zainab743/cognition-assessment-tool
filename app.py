from google_sheets import save_to_google_sheets
import uuid

import streamlit as st
import time

from math_test import run_math_test
from stroop_test import run_stroop_test
from mental_rotation_test import run_mental_rotation_test

st.set_page_config(page_title="Cognitive Assessment Tool", layout="centered")


# =====================================================
# CLOUD SAFE SESSION INITIALIZATION
# =====================================================

if "current_stage" not in st.session_state:
    st.session_state.current_stage = "consent"

if "stage_lock" not in st.session_state:
    st.session_state.stage_lock = True

if "heartbeat" not in st.session_state:
    st.session_state.heartbeat = time.time()


# =====================================================
# CONSENT + DEMOGRAPHICS PAGE
# =====================================================

if st.session_state.current_stage == "consent":

    st.title("Cognitive Assessment Study")

    st.markdown("""
    ### Digital Consent

    - I confirm that I have passed 12th standard.
    - I confirm that I am computer literate.
    - I understand that the data collected will be used **only for academic purposes**.
    - My participation is voluntary and I may withdraw at any time.
    """)

    consent = st.checkbox("I agree to participate")

    st.markdown("---")
    st.markdown("### Baseline & Demographic Information")

    name = st.text_input("Name")
    age = st.selectbox("Age Category", ["18-25", "26-35", "36-45", "46-55", "56+"])
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    hometown = st.text_input("Home Town")
    current_city = st.text_input("Current City")

    mother_language = st.selectbox(
        "Mother Language",
        ["Hindi", "English", "Bengali", "Tamil", "Telugu",
         "Marathi", "Gujarati", "Kannada", "Malayalam", "Other"]
    )

    academic = st.selectbox(
        "Academic Qualification",
        ["Pursuing UG", "Pursuing PG", "Completed UG", "Completed PG"]
    )

    service = st.selectbox(
        "Service Status",
        ["Employed", "Not Employed", "Retired"]
    )

    handedness = st.selectbox(
        "Handedness",
        ["Right", "Left", "Ambidextrous"]
    )

    device = st.selectbox(
        "Device Used",
        ["Laptop", "Desktop", "Mobile", "Tablet"]
    )

    vision = st.selectbox(
        "Vision Status",
        ["Normal", "Corrected to Normal"]
    )

    prior_exposure = st.selectbox(
        "Prior exposure to any cognitive test recently?",
        ["Yes", "No"]
    )

    if st.button("Start Test"):

        if not consent:
            st.warning("You must provide consent to proceed.")
            st.stop()

        if name.strip() == "":
            st.warning("Please enter your name.")
            st.stop()

        st.session_state.demographics = {
            "name": name,
            "age": age,
            "gender": gender,
            "hometown": hometown,
            "current_city": current_city,
            "mother_language": mother_language,
            "academic": academic,
            "service": service,
            "handedness": handedness,
            "device": device,
            "vision": vision,
            "prior_exposure": prior_exposure
        }

        st.session_state.stage_lock = False
        st.session_state.current_stage = "instructions"

        st.rerun()


# =====================================================
# INSTRUCTION SCREEN
# =====================================================

elif st.session_state.current_stage == "instructions":

    st.title("Instructions")

    st.markdown("""
    You will complete **three cognitive tasks**:

    1. Math Speed Test  
    2. Stroop Test  
    3. Mental Rotation Task  

    Respond quickly and accurately.

    Click the button below to begin the assessment.
    """)

    if st.button("Continue to Test"):

        st.session_state.stage_lock = False
        st.session_state.current_stage = "math"

        st.rerun()


# =====================================================
# TEST ENGINE ROUTER
# =====================================================

elif st.session_state.current_stage == "math":
    run_math_test()

elif st.session_state.current_stage == "stroop":
    run_stroop_test()

elif st.session_state.current_stage == "mental":
    run_mental_rotation_test()


# =====================================================
# FINAL SCREEN
# =====================================================

elif st.session_state.current_stage == "final":

    st.title("Thank You for Participating!")

    # Generate participant ID
    participant_id = str(uuid.uuid4())

    # Collect demographics
    demo = st.session_state.get("demographics", {})

    # Collect test scores
    numerical_score = st.session_state.get("numerical_score", 0)
    stroop_results = st.session_state.get("results", [])
    mrt_score = st.session_state.get("mrt_score", 0)

    # Basic Stroop metrics (safe fallback)
    stroop_error = 0
    stroop_mean_rt = 0
    stroop_interference = 0

    # Create data dictionary
    data = {
        "participant_id": participant_id,
        "name": demo.get("name", ""),
        "age": demo.get("age", ""),
        "gender": demo.get("gender", ""),
        "hometown": demo.get("hometown", ""),
        "Mother Language": demo.get("mother_language", ""),
        "qualification": demo.get("academic", ""),
        "service status": demo.get("service", ""),
        "handedness": demo.get("handedness", ""),
        "device used": demo.get("device", ""),
        "vision status": demo.get("vision", ""),
        "num_attempted": st.session_state.get("num_attempted", 0),
        "num_correct": st.session_state.get("num_correct", 0),
        "num_w_accuracy": st.session_state.get("num_weighted_accuracy", 0),
        "num_speed": st.session_state.get("num_speed", 0),
        "num_ability_score": st.session_state.get("numerical_score", 0),
        "Stroop_error": st.session_state.get("stroop_error", 0),
        "Stroop_mean_RT": st.session_state.get("stroop_mean_rt", 0),
        "Stroop_interference": st.session_state.get("stroop_interference", 0),
        "MR_acc": st.session_state.get("mrt_acc", 0),
        "MR_reaction": st.session_state.get("mrt_reaction", 0),
        "MR_Timed-out": st.session_state.get("mrt_timeout", 0),
    }

    # Save to Google Sheets
    save_to_google_sheets(data)

    st.success("Your responses have been recorded successfully.")

    st.markdown("""
    Your participation is greatly appreciated.

    This data will be used strictly for academic purposes.
    """)

    st.success("You may now close this window.")

    


