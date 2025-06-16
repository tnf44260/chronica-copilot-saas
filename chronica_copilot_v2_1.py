import streamlit as st
import pandas as pd
from datetime import datetime
import openai

# Leafy Design Styling 🌿
st.markdown("""
    <style>
    .main {background-color: #F7F9F4;}
    .stButton>button {background-color: #A8D5BA; color: #333333; border-radius: 12px; padding: 0.5em 1em;}
    .stTextInput>div>div>input {border-radius: 10px;}
    .stTextArea textarea {border-radius: 10px;}
    .stSelectbox>div>div {border-radius: 10px;}
    .stMultiSelect>div>div {border-radius: 10px;}
    .stRadio>div>div {border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🌿 Chronica Copilot SaaS v2.1")

# Initialize session state
if 'patient_profile' not in st.session_state:
    st.session_state.patient_profile = {}
if 'copilot_checkins' not in st.session_state:
    st.session_state.copilot_checkins = []
if 'conversation_step' not in st.session_state:
    st.session_state.conversation_step = 0
if 'checkin_data' not in st.session_state:
    st.session_state.checkin_data = {}

# OpenAI Key 🔑 (uses Streamlit Secrets for deployment)
client = openai.OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# Profile Intake
if not st.session_state.patient_profile:
    st.header("📋 Let's set up your Copilot profile")

    name = st.text_input("What’s your name?")
    age = st.number_input("How old are you?", min_value=0, max_value=120)

    chronic_conditions_list = [
        "Lupus", "Gastroparesis", "PCOS", "Endometriosis", "IC", "MCAS",
        "POTS", "EDS", "Fibromyalgia", "IBS", "MS", "RA", "Sjogren's",
        "Long Covid", "Dysautonomia", "Other"
    ]

    conditions = st.multiselect("Which chronic conditions are you managing?", chronic_conditions_list)

    if st.button("Save My Profile"):
        st.session_state.patient_profile = {
            "Name": name,
            "Age": age,
            "Conditions": ', '.join(conditions),
            "ProfileCreated": datetime.now().strftime("%Y-%m-%d")
        }
        st.success("✅ Your Copilot profile is ready!")
        st.session_state.conversation_step = 1

# Conversational Check-In Flow
if st.session_state.patient_profile and st.session_state.conversation_step > 0:
    st.header(f"👋 Hi {st.session_state.patient_profile['Name']}, let’s check in together 🌿")

    if st.session_state.conversation_step == 1:
        emotions = st.text_input("How are you feeling emotionally today?")
        if st.button("Next ➔"):
            st.session_state.checkin_data['EmotionalState'] = emotions
            st.session_state.conversation_step = 2

    elif st.session_state.conversation_step == 2:
        symptoms = st.text_input("Which symptoms are standing out right now?")
        if st.button("Next ➔"):
            st.session_state.checkin_data['Symptoms'] = symptoms
            st.session_state.conversation_step = 3

    elif st.session_state.conversation_step == 3:
        triggers = st.text_input("Anything triggering your symptoms today?")
        if st.button("Next ➔"):
            st.session_state.checkin_data['Triggers'] = triggers
            st.session_state.conversation_step = 4

    elif st.session_state.conversation_step == 4:
        sleep_quality = st.radio("How was your sleep last night?", 
                                  ["Excellent", "Good", "Fair", "Poor", "Exhausted"])
        if st.button("Next ➔"):
            st.session_state.checkin_data['SleepQuality'] = sleep_quality
            st.session_state.conversation_step = 5

    elif st.session_state.conversation_step == 5:
        notes = st.text_area("Anything else you want to share today?")
        if st.button("Submit Check-In ✅"):
            st.session_state.checkin_data['ExtraNotes'] = notes
            st.session_state.conversation_step = 6

# GPT Copilot Reflection
if st.session_state.conversation_step == 6:

    gpt_input = f"""
Emotional State: {st.session_state.checkin_data['EmotionalState']}
Symptoms: {st.session_state.checkin_data['Symptoms']}
Triggers: {st.session_state.checkin_data['Triggers']}
Sleep Quality: {st.session_state.checkin_data['SleepQuality']}
Extra Notes: {st.session_state.checkin_data['ExtraNotes']}
"""

    system_prompt = f"""
You are Chronica Copilot — a trauma-informed AI chronic condition companion.

Today's patient check-in is:

{gpt_input}

Please return ONLY:

- SummaryReflection (short validating summary)
- EmotionalFocus
- SymptomFocus
- PacingSuggestion (daily pacing advice)
- NervousSystemTip (nervous system calming tip)

Be warm, encouraging, simple, and gently supportive.
"""

    with st.spinner("Processing your Copilot reflection..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": gpt_input}
            ],
            temperature=0.4,
            max_tokens=600
        )

        output = response.choices[0].message.content

    parsed_summary = {}
    for line in output.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            parsed_summary[key.strip()] = value.strip()

    checkin_record = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        **st.session_state.checkin_data,
        **parsed_summary
    }

    st.session_state.copilot_checkins.append(checkin_record)
    st.session_state.today_summary = parsed_summary
    st.session_state.conversation_step = 7

# Reflection Output
if st.session_state.conversation_step == 7:

    st.subheader("🌿 Copilot Reflection Summary")

    for key, value in st.session_state.today_summary.items():
        st.write(f"**{key}:** {value}")

    if st.button("Finish Check-In ➔"):
        st.session_state.conversation_step = 0

# Session History Table
if st.session_state.copilot_checkins:
    st.subheader("📊 My Copilot Session History")

    df = pd.DataFrame(st.session_state.copilot_checkins)
    st.dataframe(df)

    if st.button("💾 Export Session Log"):
        df.to_csv("chronica_copilot_session_log.csv", index=False)
        st.success("✅ Session log exported.")

# Profile Viewer
if st.session_state.patient_profile:
    with st.expander("🌿 My Chronica Profile"):
        for key, value in st.session_state.patient_profile.items():
            st.write(f"**{key}:** {value}")

        if st.button("Export My Profile"):
            pd.DataFrame([st.session_state.patient_profile]).to_csv("chronica_patient_profile.csv", index=False)
            st.success("✅ Profile exported.")
