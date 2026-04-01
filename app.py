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

    - This assessment is conducted solely for academic research purposes.
    - The data collected will be used only for analysis and study related to cognitive performance.
    - No personally identifiable information will be shared with third parties.
    - Your responses will remain confidential and anonymous.
    - Participation in this assessment is voluntary.
    - You may choose to exit the test at any time without any consequences.
    """)

    st.subheader("Eligibility Confirmation")

    c1 = st.checkbox("I confirm that I have passed 12th standard.")
    c2 = st.checkbox("I confirm that I am computer literate and can operate a computer independently.")
    consent = st.checkbox("I agree to participate and allow my data to be used for academic research purposes.")

    if c1 and c2 and consent:
        if st.button("Start Test", key="start_test_btn"):
            st.session_state.current_stage = "demographics"
            st.rerun()
    else:
        st.warning("Please confirm all the above statements to continue.")

    

if st.session_state.current_stage == "demographics":

    st.markdown("### Baseline & Demographic Information")

    name = st.text_input("Name", key="name")
    age = st.selectbox("Age Category", ["18-25", "26-35", "36-45", "46-55", "56+"], key="age")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
    hometown = st.text_input("Home Town", key="hometown")
    current_city = st.text_input("Current City", key="current_city")

    mother_language = st.selectbox(
        "Mother Language",
        ["Hindi", "English", "Bengali", "Tamil", "Telugu",
        "Marathi", "Gujarati", "Kannada", "Malayalam", "Other"],
        key="mother_language"
    )

    academic = st.selectbox(
        "Academic Qualification",
        ["Pursuing UG", "Pursuing PG", "Completed UG", "Completed PG"],
        key="academic"
    )

    service = st.selectbox(
        "Service Status",
        ["Employed", "Not Employed", "Retired"],
        key="service"
    )

    handedness = st.selectbox(
        "Handedness",
        ["Right", "Left", "Ambidextrous"],
    key="handedness"
        )

    device = st.selectbox(
        "Device Used",
        ["Laptop", "Desktop", "Mobile", "Tablet"],
        key="device"
    )

    vision = st.selectbox(
        "Vision Status",
        ["Normal", "Corrected to Normal"],
        key="vision"
    )

    prior_exposure = st.selectbox(
        "Prior exposure to any cognitive test recently?",
        ["Yes", "No"],
        key="prior_exposure"
    )

    if st.button("Continue", key="demo_continue_btn"):

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

        st.session_state.current_stage = "instructions"
        st.rerun()


# =====================================================
# INSTRUCTION SCREEN
# =====================================================

elif st.session_state.current_stage == "instructions":

    st.title("Instructions")

    st.markdown("""
    You will complete **three cognitive tasks** as part of this assessment:

    ### 🧠 Tasks Included
    1. **Numerical Ability Test** 
    2. **Stroop Test** 
    3. **Mental Rotation Task**

    ---

    ### ⏱️ Guidelines
    - Respond **as quickly and accurately as possible**.  
    - Each task is **time-sensitive**, so avoid delays.  
    - Read each question carefully before answering.
    - Do not use any external aids (calculators, pen, paper, etc.) during the test.

    ---

    ### ⚠️ Important Notes
    - Ensure you are in a **quiet and distraction-free environment**.  
    - Do not refresh or close the browser during the test.  
    - Once started, the test should be completed in one session.  

    ---

    Click the button below when you are ready to begin.
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
        # -------------------------------
    # 🎯 NORMALIZE SCORES (OUT OF 100)
    # -------------------------------

    # Numerical (already 0–1 → convert to 0–100)
    num_score = st.session_state.get("numerical_score", 0) * 100

    # Mental Rotation (already 0–1 → convert to 0–100)
    mrt_score = st.session_state.get("mrt_score", 0) * 100

    # Stroop (lower interference & error = better)
    stroop_error = st.session_state.get("stroop_error", 0)
    stroop_interference = st.session_state.get("stroop_interference", 0)

    # Simple normalization for Stroop
    # (you can tweak constants later if needed)
    stroop_score = 100 - ((stroop_error * 0.6) + (stroop_interference * 40))

    # Clamp score between 0–100
    stroop_score = max(0, min(100, stroop_score))


    # -------------------------------
    # 🧠 OVERALL SCORE
    # -------------------------------

    overall_score = (num_score + stroop_score + mrt_score) / 3


    # -------------------------------
    # 💬 INTERPRETATION LOGIC
    # -------------------------------

    if overall_score >= 75:
        summary = "You demonstrate strong overall cognitive performance with good reasoning and attention control."
    elif overall_score >= 50:
        summary = "Your cognitive performance is moderate with balanced abilities across tasks."
    else:
        summary = "Your performance suggests difficulty under time pressure. Practice may help improve your cognitive efficiency."


    # Strength identification
    scores = {
        "Numerical Ability": num_score,
        "Attention Control": stroop_score,
        "Spatial Ability": mrt_score
    }

    strength = max(scores, key=scores.get)
    weakness = min(scores, key=scores.get)


    # -------------------------------
    # 📊 DISPLAY REPORT
    # -------------------------------

    st.subheader("🧠 Your Cognitive Report")

    col1, col2, col3 = st.columns(3)

    col1.metric("Numerical Ability", f"{num_score:.0f} / 100")
    col2.metric("Attention Control", f"{stroop_score:.0f} / 100")
    col3.metric("Spatial Ability", f"{mrt_score:.0f} / 100")

    st.markdown("---")

    st.metric("Overall Cognitive Score", f"{overall_score:.0f} / 100")

    st.markdown("### 📝 Interpretation")
    st.write(summary)

    st.markdown(f"**Strength:** {strength}")
    st.markdown(f"**Can Improve:** {weakness}")

    st.markdown("---")

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
        "MR_spatial_score": st.session_state.get("mrt_score", 0),
        "MR_high_angle_accuracy": st.session_state.get("mrt_high_angle_acc", 0),
    }

    # Save to Google Sheets
    save_to_google_sheets(data)

    st.success("Your responses have been recorded successfully.")

    st.markdown("""
    Your participation is greatly appreciated.

    This data will be used strictly for academic purposes.
    """)

    st.success("You may now close this window.")

    


