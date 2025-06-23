<<<<<<< HEAD

=======
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
import streamlit as st
import openai
import pyttsx3
import tempfile
import os
<<<<<<< HEAD
import datetime

# Botanical background CSS (applies to all screens, including login)
st.markdown("""
<style>
html, body, .stApp {
    background-color: #f6fdfb !important;
    background-image: url('https://raw.githubusercontent.com/tnf44260/chronica-copilot-saas/main/assets/healing_garden_background.png') !important;
    background-repeat: repeat !important;
    background-size: cover !important;
    background-attachment: fixed !important;
    background-position: center !important;
    font-family: 'Quicksand', sans-serif;
    color: #2c3e50;
    padding: 1rem;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Quicksand', sans-serif;
    color: #2c3e50;
}
.stButton>button {
    background-color: #a8d5ba;
    color: #2c3e50;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
    cursor: pointer;
}
.stButton>button:hover {
    background-color: #8cc9a1;
}
section[data-testid="stSidebar"] {
    background-color: rgba(230, 240, 233, 0.8) !important;
    padding: 1rem;
    border-radius: 8px;
    font-family: 'Quicksand', sans-serif;
    color: #18402a !important;
    background-image: url('https://raw.githubusercontent.com/tnf44260/chronica-copilot-saas/main/assets/leafy_sidebar.png');
    background-repeat: repeat-y;
    background-size: contain;
}
section[data-testid="stSidebar"] * {
    color: #18402a !important;
    text-shadow: 0 1px 2px rgba(255,255,255,0.15);
}
</style>
""", unsafe_allow_html=True)

# Login screen using email or name
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False

if not st.session_state.user_logged_in:
    st.title("🌿 Welcome to Chronica")
    st.subheader("A calm space to check in with yourself.")
    email = st.text_input("Please enter your email to begin:", key="login_email")
    if st.button("Enter Chronica", key="login_button"):
        if email.strip():
            st.session_state.user_logged_in = True
            st.session_state.user_email = email.strip()
            # Log login activity
            if "user_activity_log" not in st.session_state:
                st.session_state.user_activity_log = []
            st.session_state.user_activity_log.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "login",
                "details": {"email": email.strip()}
            })
        else:
            st.warning("Please enter a valid email to continue.")
    st.stop()
=======
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae

# Set your OpenAI API key here or via environment variable
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Initialize TTS engine if available
def init_tts():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        # Select a calming voice if available
        for voice in voices:
            if 'female' in voice.name.lower() or 'calm' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 150)  # Slower speech rate for calming effect
        return engine
    except Exception:
        return None

tts_engine = init_tts()

# Function to speak text if TTS engine is available
def speak(text):
    if tts_engine:
        tts_engine.say(text)
        tts_engine.runAndWait()

<<<<<<< HEAD

st.sidebar.title("🌿 Chronica AI Copilot")

# Restore user personalization from intake info if available
personal_name = ""
if st.session_state.get('intake_info', {}).get('name'):
    personal_name = st.session_state['intake_info']['name']

mode = st.sidebar.radio("Choose mode:", ["Guided", "Open Chat"])

# Intake form: always available as modal or collapsible if not in sidebar
=======
# CSS and background styling for healing garden theme
st.markdown("""
<style>
.stApp {
    background-color: #f6fdfb;
    background-image: url('https://raw.githubusercontent.com/tnf44260/chronica-copilot-saas/main/assets/healing_garden_background.png');
    background-repeat: repeat;
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    font-family: 'Quicksand', sans-serif;
    color: #2c3e50;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Quicksand', sans-serif;
    color: #2c3e50;
}
.stButton>button {
    background-color: #a8d5ba;
    color: #2c3e50;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🌿 Chronica AI Copilot")

mode = st.sidebar.radio("Choose mode:", ["Guided", "Open Chat"])

>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
show_intake_form = st.sidebar.checkbox("Show intake form")

# Diagnosis to symptom mapping for dynamic symptom selection
diagnosis_symptoms_map = {
    "Anxiety": [
        "Racing heart",
        "Sweating",
        "Restlessness",
        "Muscle tension",
        "Fatigue",
        "Difficulty concentrating",
        "Irritability"
    ],
    "Depression": [
        "Persistent sadness",
        "Loss of interest",
        "Fatigue",
        "Sleep disturbances",
        "Feelings of worthlessness",
        "Difficulty concentrating",
        "Appetite changes"
    ],
    "PTSD": [
        "Flashbacks",
        "Nightmares",
        "Avoidance",
        "Hypervigilance",
        "Emotional numbness",
        "Irritability",
        "Sleep problems"
    ],
    "Bipolar Disorder": [
        "Mood swings",
        "Increased energy",
        "Impulsivity",
        "Sleep disturbances",
        "Irritability",
        "Depressive episodes"
    ],
    "General": [
        "Headache",
        "Fatigue",
        "Muscle pain",
        "Sleep disturbances",
        "Appetite changes",
        "Mood swings"
    ]
}

<<<<<<< HEAD
def intake_form_body():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=st.session_state.get('intake_info', {}).get('name', ''), key="intake_name")
    with col2:
        age = st.number_input("Age", min_value=0, max_value=120, step=1, value=st.session_state.get('intake_info', {}).get('age', 0), key="intake_age")
    diagnosis = st.selectbox("Diagnosis (select one)", options=[""] + list(diagnosis_symptoms_map.keys()), index=(list(diagnosis_symptoms_map.keys()).index(st.session_state.get('intake_info', {}).get('diagnosis')) + 1 if st.session_state.get('intake_info', {}).get('diagnosis') in diagnosis_symptoms_map else 0), key="intake_diag")
    medication = st.text_input("Current Medication(s)", value=st.session_state.get('intake_info', {}).get('medication', ''), key="intake_med")
    symptoms_options = diagnosis_symptoms_map.get(diagnosis, diagnosis_symptoms_map["General"])
    # Always retain defaults on reload for multiselect
    symptoms_selected = st.multiselect("Select your symptoms (you can select multiple)", options=symptoms_options, default=st.session_state.get('intake_info', {}).get('symptoms', []), key="intake_symptoms")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if not name.strip():
            st.warning("Please enter your name.")
        elif not diagnosis.strip():
            st.warning("Please select a diagnosis.")
        elif not symptoms_selected:
            st.warning("Please select at least one symptom.")
        else:
            st.success(f"Thank you {name}. Your intake form has been submitted.")
            st.session_state['intake_info'] = {
                "name": name.strip(),
                "age": age,
                "diagnosis": diagnosis,
                "medication": medication.strip(),
                "symptoms": symptoms_selected
            }
            # Log intake activity
            if "user_activity_log" not in st.session_state:
                st.session_state.user_activity_log = []
            st.session_state.user_activity_log.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "intake_form_submit",
                "details": dict(st.session_state['intake_info'])
            })
    return submitted

if show_intake_form:
    st.header("Intake Form")
    with st.form("intake_form"):
        intake_form_body()
else:
    # Provide collapsible intake form if not shown in sidebar
    with st.expander("Show Intake Form (optional)", expanded=False):
        with st.form("intake_form_sidebar"):
            intake_form_body()

if personal_name:
    st.header(f"🌿 Welcome back, {personal_name}!")
else:
    st.header("🌿 Your Chronica Dashboard")
=======
# Intake form with name, age, diagnosis, medication, symptoms
if show_intake_form:
    with st.form("intake_form"):
        st.header("Intake Form")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        diagnosis = st.selectbox("Diagnosis (select one)", options=[""] + list(diagnosis_symptoms_map.keys()))
        medication = st.text_input("Current Medication(s)")
        symptoms_options = diagnosis_symptoms_map.get(diagnosis, diagnosis_symptoms_map["General"])
        symptoms_selected = st.multiselect("Select your symptoms (you can select multiple)", options=symptoms_options)
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not name.strip():
                st.warning("Please enter your name.")
            elif not diagnosis.strip():
                st.warning("Please select a diagnosis.")
            elif not symptoms_selected:
                st.warning("Please select at least one symptom.")
            else:
                st.success(f"Thank you {name}. Your intake form has been submitted.")
                # Store intake info in session state for use in chat
                st.session_state['intake_info'] = {
                    "name": name.strip(),
                    "age": age,
                    "diagnosis": diagnosis,
                    "medication": medication.strip(),
                    "symptoms": symptoms_selected
                }

st.header("🌿 Your Healing Garden")
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae

# Helper function to call OpenAI ChatCompletion with prompt and history
def get_ai_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            n=1,
            stop=None
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"Error communicating with AI: {e}")
        return "Sorry, I am having trouble responding right now."

<<<<<<< HEAD
# --- GUIDED MODE WITH JOURNAL, NEXT STEPS, AND TONE ---
=======
# Guided mode: step-based conversational flow
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
if mode == "Guided":
    st.write("Welcome to the guided mode. Let's explore your feelings step-by-step with compassion and care.")

    if 'guided_step' not in st.session_state:
        st.session_state.guided_step = 0
        st.session_state.guided_responses = []
<<<<<<< HEAD
    if 'past_summaries' not in st.session_state:
        st.session_state.past_summaries = []
    if 'guided_complete' not in st.session_state:
        st.session_state.guided_complete = False
    if 'guided_journal' not in st.session_state:
        st.session_state.guided_journal = ""
    if 'guided_tone' not in st.session_state:
        st.session_state.guided_tone = "Calm"
=======
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae

    guided_steps = [
        "How are you feeling today emotionally and physically?",
        "Can you describe any specific symptoms or sensations you are experiencing?",
        "What are some current stressors or challenges in your life?",
        "What coping strategies or supports have you found helpful?",
        "Is there anything else you'd like to share or explore?"
    ]

<<<<<<< HEAD
    # Trauma-informed tone selection
    voice_tones = ["Calm", "Supportive", "Uplifting", "Gentle", "Empowering"]
    st.session_state.guided_tone = st.selectbox("AI Voice Tone", voice_tones, index=voice_tones.index(st.session_state.get("guided_tone", "Calm")), key="guided_tone_select")

    if not st.session_state.guided_complete and st.session_state.guided_step < len(guided_steps):
        prompt = guided_steps[st.session_state.guided_step]
        response = st.text_area(prompt, key=f"guided_input_{st.session_state.guided_step}")

        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Next", key=f"guided_next_{st.session_state.guided_step}"):
                if response.strip():
                    # Save current response only if at correct step
                    if len(st.session_state.guided_responses) == st.session_state.guided_step:
                        st.session_state.guided_responses.append(response.strip())
                    else:
                        st.session_state.guided_responses[st.session_state.guided_step] = response.strip()
                    st.session_state.guided_step += 1
                    # Log guided step activity
                    if "user_activity_log" not in st.session_state:
                        st.session_state.user_activity_log = []
                    st.session_state.user_activity_log.append({
                        "timestamp": datetime.datetime.now().isoformat(),
                        "type": "guided_step",
                        "details": {
                            "step": st.session_state.guided_step,
                            "prompt": prompt,
                            "response": response.strip()
                        }
                    })
                    st.experimental_rerun()
                else:
                    st.warning("Please enter a response before continuing.")
        with col2:
            if st.session_state.guided_step > 0:
                if st.button("Previous", key=f"guided_prev_{st.session_state.guided_step}"):
                    if st.session_state.guided_responses:
                        st.session_state.guided_responses.pop()
                    st.session_state.guided_step = max(0, st.session_state.guided_step - 1)
                    st.experimental_rerun()
    elif not st.session_state.guided_complete:
        st.session_state.guided_complete = True
        st.success("Thank you for sharing. Here's a compassionate summary of your responses:")

        # AI summary prompt (trauma-informed, supportive, and using selected tone)
        summary_prompt = [
            {"role": "system", "content":
                f"You are a compassionate, trauma-informed AI therapist. Use a {st.session_state.guided_tone.lower()} and supportive tone."},
=======
    if st.session_state.guided_step < len(guided_steps):
        prompt = guided_steps[st.session_state.guided_step]
        response = st.text_area(prompt, key=f"guided_input_{st.session_state.guided_step}")

        if st.button("Next", key="guided_next"):
            if response.strip():
                st.session_state.guided_responses.append(response.strip())
                st.session_state.guided_step += 1
            else:
                st.warning("Please enter a response before continuing.")
    else:
        st.success("Thank you for sharing. Here's a compassionate summary of your responses:")

        # Build prompt for AI summarization
        summary_prompt = [
            {"role": "system", "content": "You are a compassionate, trauma-informed AI therapist."},
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
            {"role": "user", "content": "Please provide a gentle, supportive summary of the following patient responses:"}
        ]
        for i, answer in enumerate(st.session_state.guided_responses):
            summary_prompt.append({"role": "user", "content": f"Q: {guided_steps[i]}\nA: {answer}"})
<<<<<<< HEAD
        summary = get_ai_response(summary_prompt)

        # Doctor summary
        doctor_prompt = [
            {"role": "system", "content": "You are a professional medical AI assistant."},
            {"role": "user", "content": "Based on the following patient responses, provide a concise medical summary suitable for a doctor’s visit:"}
        ]
        for i, answer in enumerate(st.session_state.guided_responses):
            doctor_prompt.append({"role": "user", "content": f"Q: {guided_steps[i]}\nA: {answer}"})
        doctor_summary = get_ai_response(doctor_prompt)

        # Optional: AI-generated journal entry or insight
        journal_prompt = [
            {"role": "system", "content":
                f"You are a supportive journaling coach and therapist. Based on the following responses, write a gentle, insightful journal entry or personal insight for the user (in the first person), using a {st.session_state.guided_tone.lower()} and reflective tone."}
        ]
        for i, answer in enumerate(st.session_state.guided_responses):
            journal_prompt.append({"role": "user", "content": f"Q: {guided_steps[i]}\nA: {answer}"})
        st.session_state.guided_journal = get_ai_response(journal_prompt)

        # Limit to last 5 summaries for clean historical view
        st.session_state.past_summaries.append({
            "reflection_summary": summary,
            "doctor_summary": doctor_summary,
            "journal": st.session_state.guided_journal,
            "tone": st.session_state.guided_tone,
            "timestamp": datetime.datetime.now().isoformat()
        })
        if len(st.session_state.past_summaries) > 5:
            st.session_state.past_summaries = st.session_state.past_summaries[-5:]

        # Log guided complete activity
        if "user_activity_log" not in st.session_state:
            st.session_state.user_activity_log = []
        st.session_state.user_activity_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "guided_complete",
            "details": {
                "responses": list(st.session_state.guided_responses),
                "summary": summary
            }
        })

        # Display summaries
        st.markdown("### Your Chronica Reflection Summary")
        st.markdown(summary)

        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Play Reflection Summary (Voice)"):
                speak(summary)
        with col2:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as f:
                f.write("Chronica Reflection Summary\n\n")
=======

        summary = get_ai_response(summary_prompt)
        st.markdown(f"### Summary:\n{summary}")

        if st.button("Play Summary (Voice)"):
            speak(summary)

        if st.button("Export Summary"):
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as f:
                f.write("Chronica Healing Garden Summary\n\n")
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
                for i, answer in enumerate(st.session_state.guided_responses):
                    f.write(f"{guided_steps[i]}\n{answer}\n\n")
                f.write("Summary:\n")
                f.write(summary)
<<<<<<< HEAD
                temp_filepath_reflection = f.name
            with open(temp_filepath_reflection, "rb") as file:
                st.download_button(
                    label="Download Reflection Summary as TXT",
                    data=file,
                    file_name="chronica_reflection_summary.txt",
                    mime="text/plain"
                )
            try:
                os.remove(temp_filepath_reflection)
            except Exception:
                pass

        st.markdown("### Doctor Visit Summary")
        with st.expander("View Doctor Summary", expanded=True):
            st.markdown(doctor_summary)
            col3, col4 = st.columns([1,1])
            with col3:
                if st.button("Play Doctor Summary (Voice)"):
                    speak(doctor_summary)
            with col4:
                with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as f:
                    f.write("Chronica Doctor Visit Summary\n\n")
                    for i, answer in enumerate(st.session_state.guided_responses):
                        f.write(f"{guided_steps[i]}\n{answer}\n\n")
                    f.write("Doctor Summary:\n")
                    f.write(doctor_summary)
                    temp_filepath_doctor = f.name
                with open(temp_filepath_doctor, "rb") as file:
                    st.download_button(
                        label="Download Doctor Summary as TXT",
                        data=file,
                        file_name="chronica_doctor_summary.txt",
                        mime="text/plain"
                    )
                try:
                    os.remove(temp_filepath_doctor)
                except Exception:
                    pass

        # Optional AI-generated Journal/Insight
        st.markdown("### AI-Generated Journal Entry / Insight")
        st.info(st.session_state.guided_journal)
        colj, _ = st.columns([1,1])
        with colj:
            if st.button("Play Journal Entry (Voice)"):
                speak(st.session_state.guided_journal)

        # Affirmation/closing line (restored)
        st.markdown("#### 🌱 *Remember: Every small step is progress. You are worthy of care and compassion.*")

        # What would you like to do next?
        st.markdown("### What would you like to do next?")
        col_restart, col_openchat, col_logout = st.columns([1,1,1])
        next_action = None
        with col_restart:
            if st.button("Restart"):
                next_action = "restart"
        with col_openchat:
            if st.button("Return to Open Chat"):
                next_action = "openchat"
        with col_logout:
            if st.button("Log Out"):
                next_action = "logout"
        if next_action == "restart":
            st.session_state.guided_step = 0
            st.session_state.guided_responses = []
            st.session_state.guided_complete = False
            st.session_state.guided_journal = ""
            st.experimental_rerun()
        elif next_action == "openchat":
            st.session_state.guided_step = 0
            st.session_state.guided_responses = []
            st.session_state.guided_complete = False
            st.session_state.guided_journal = ""
            # Switch mode
            st.session_state['__streamlit_sidebar_radio__Choose mode:'] = "Open Chat"
            st.experimental_rerun()
        elif next_action == "logout":
            st.session_state.clear()
            st.experimental_rerun()

        if st.session_state.past_summaries:
            with st.expander("Past Summaries (last 5 sessions)"):
                for idx, summ in enumerate(reversed(st.session_state.past_summaries)):
                    time_str = summ.get("timestamp", "")[:19].replace("T", " ")
                    st.markdown(f"#### Session {len(st.session_state.past_summaries) - idx} (Tone: {summ.get('tone', 'Calm')}, {time_str})")
                    st.markdown("**Your Chronica Reflection Summary:**")
                    st.markdown(summ["reflection_summary"])
                    st.markdown("**Doctor Visit Summary:**")
                    st.markdown(summ["doctor_summary"])
                    st.markdown("**AI Journal Entry:**")
                    st.markdown(summ.get("journal",""))
                    st.markdown("---")

# --- OPEN CHAT MODE WITH FULL AI MEMORY, INTAKE DATA, AND TONE ---
=======
                temp_filepath = f.name
            with open(temp_filepath, "rb") as file:
                st.download_button(
                    label="Download Summary as TXT",
                    data=file,
                    file_name="chronica_summary.txt",
                    mime="text/plain"
                )
            try:
                os.remove(temp_filepath)
            except Exception:
                pass

        if st.button("Restart Guided Session"):
            st.session_state.guided_step = 0
            st.session_state.guided_responses = []

# Open Chat mode with OpenAI integration and voice input/output
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
elif mode == "Open Chat":
    st.write("Welcome to open chat mode. Feel free to share anything, and I will respond with care and understanding.")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
<<<<<<< HEAD
    if 'openchat_tone' not in st.session_state:
        st.session_state.openchat_tone = "Calm"

    # Intake data, if available
    intake_info = st.session_state.get('intake_info')
    if intake_info:
        with st.expander("Your Intake Information", expanded=True):
=======

    # Display intake info if available
    intake_info = st.session_state.get('intake_info')
    if intake_info:
        with st.expander("Your Intake Information"):
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
            st.markdown(f"**Name:** {intake_info['name']}")
            st.markdown(f"**Age:** {intake_info['age']}")
            st.markdown(f"**Diagnosis:** {intake_info['diagnosis']}")
            st.markdown(f"**Medication:** {intake_info['medication'] or 'None'}")
            st.markdown(f"**Symptoms:** {', '.join(intake_info['symptoms'])}")

<<<<<<< HEAD
    # Trauma-informed tone selection for Open Chat
    openchat_voice_tones = ["Calm", "Supportive", "Uplifting", "Gentle", "Empowering"]
    st.session_state.openchat_tone = st.selectbox("AI Voice Tone", openchat_voice_tones, index=openchat_voice_tones.index(st.session_state.get("openchat_tone", "Calm")), key="openchat_tone_select")

    user_input = st.text_input("You:", key="openchat_input", placeholder="Type your message here...")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Send", key="openchat_send"):
            if user_input.strip():
                # Append user message
                st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
                # Log open chat user activity
                if "user_activity_log" not in st.session_state:
                    st.session_state.user_activity_log = []
                st.session_state.user_activity_log.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "open_chat_user",
                    "details": {"message": user_input.strip()}
                })

                # System prompt uses intake data and tone for context
                intake_str = ""
                if intake_info:
                    intake_str = (
                        f"User name: {intake_info.get('name','')}, "
                        f"Age: {intake_info.get('age','')}, "
                        f"Diagnosis: {intake_info.get('diagnosis','')}, "
                        f"Medication: {intake_info.get('medication','')}, "
                        f"Symptoms: {', '.join(intake_info.get('symptoms',[]))}."
                    )
                system_prompt = {
                    "role": "system",
                    "content": (
                        "You are Chronica, a trauma-informed, compassionate AI therapist. "
                        f"Respond with empathy, validation, and gentle guidance. "
                        f"Use a {st.session_state.openchat_tone.lower()} and supportive tone. "
                        + (f"Here is the user's intake info for context: {intake_str}" if intake_str else "")
                    )
                }

                # FULL chat memory: include all turns in the threaded context
                messages = [system_prompt]
                for chat in st.session_state.chat_history:
                    messages.append({"role": chat["role"], "content": chat["content"]})

                ai_response = get_ai_response(messages)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                # Log open chat AI activity
                st.session_state.user_activity_log.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "open_chat_ai",
                    "details": {"message": ai_response}
                })

                # Optionally speak the AI response
                if st.session_state.get("voice_output_enabled", False):
                    speak(ai_response)
                st.experimental_rerun()
            else:
                st.warning("Please enter a message before sending.")
    with col2:
        voice_enabled = st.checkbox("Enable voice output", key="voice_output_checkbox", value=st.session_state.get("voice_output_enabled", False))
        st.session_state["voice_output_enabled"] = voice_enabled

    # Display threaded chat history with context
    for idx, chat in enumerate(st.session_state.chat_history):
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**Chronica:** {chat['content']}")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
import streamlit as st
import openai
import pyttsx3
import tempfile
import os
import datetime

# --- Botanical Styling ---
st.markdown("""
<style>
html, body, .stApp {
    background-color: #f6fdfb !important;
    background-image: url('https://raw.githubusercontent.com/tnf44260/chronica-copilot-saas/main/assets/healing_garden_background.png') !important;
    background-repeat: repeat !important;
    background-size: cover !important;
    background-attachment: fixed !important;
    background-position: center !important;
    font-family: 'Quicksand', sans-serif;
    color: #2c3e50;
    padding: 1rem;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Quicksand', sans-serif;
    color: #2c3e50;
}
.stButton>button {
    background-color: #a8d5ba;
    color: #2c3e50;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
    cursor: pointer;
}
.stButton>button:hover {
    background-color: #8cc9a1;
}
section[data-testid="stSidebar"] {
    background-color: rgba(230, 240, 233, 0.8) !important;
    padding: 1rem;
    border-radius: 8px;
    font-family: 'Quicksand', sans-serif;
    color: #18402a !important;
    background-image: url('https://raw.githubusercontent.com/tnf44260/chronica-copilot-saas/main/assets/leafy_sidebar.png');
    background-repeat: repeat-y;
    background-size: contain;
}
section[data-testid="stSidebar"] * {
    color: #18402a !important;
    text-shadow: 0 1px 2px rgba(255,255,255,0.15);
}
</style>
""", unsafe_allow_html=True)

# --- Login Screen ---
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if not st.session_state.user_logged_in:
    st.title("🌿 Welcome to Chronica")
    st.subheader("A calm space to check in with yourself.")
    email = st.text_input("Please enter your email to begin:", key="login_email")
    if st.button("Enter Chronica", key="login_button"):
        if email.strip():
            st.session_state.user_logged_in = True
            st.session_state.user_email = email.strip()
            if "user_activity_log" not in st.session_state:
                st.session_state.user_activity_log = []
            st.session_state.user_activity_log.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "login",
                "details": {"email": email.strip()}
            })
        else:
            st.warning("Please enter a valid email to continue.")
    st.stop()

# --- OpenAI API Key ---
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# --- Voice Integration ---
def init_tts():
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'female' in voice.name.lower() or 'calm' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 150)
        return engine
    except Exception:
        return None
tts_engine = init_tts()
def speak(text):
    if tts_engine:
        tts_engine.say(text)
        tts_engine.runAndWait()

# --- Sidebar ---
st.sidebar.title("🌿 Chronica AI Copilot")
personal_name = ""
if st.session_state.get('intake_info', {}).get('name'):
    personal_name = st.session_state['intake_info']['name']
mode = st.sidebar.radio("Choose mode:", ["Guided", "Chat"])
show_intake_form = st.sidebar.checkbox("Show intake form")

# --- Intake Form ---
diagnosis_symptoms_map = {
    "Anxiety": [
        "Racing heart", "Sweating", "Restlessness", "Muscle tension", "Fatigue", "Difficulty concentrating", "Irritability"
    ],
    "Depression": [
        "Persistent sadness", "Loss of interest", "Fatigue", "Sleep disturbances", "Feelings of worthlessness", "Difficulty concentrating", "Appetite changes"
    ],
    "PTSD": [
        "Flashbacks", "Nightmares", "Avoidance", "Hypervigilance", "Emotional numbness", "Irritability", "Sleep problems"
    ],
    "Bipolar Disorder": [
        "Mood swings", "Increased energy", "Impulsivity", "Sleep disturbances", "Irritability", "Depressive episodes"
    ],
    "General": [
        "Headache", "Fatigue", "Muscle pain", "Sleep disturbances", "Appetite changes", "Mood swings"
    ]
}
def intake_form_body():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=st.session_state.get('intake_info', {}).get('name', ''), key="intake_name")
    with col2:
        age = st.number_input("Age", min_value=0, max_value=120, step=1, value=st.session_state.get('intake_info', {}).get('age', 0), key="intake_age")
    diagnosis = st.selectbox(
        "Diagnosis (select one)",
        options=[""] + list(diagnosis_symptoms_map.keys()),
        index=(list(diagnosis_symptoms_map.keys()).index(st.session_state.get('intake_info', {}).get('diagnosis')) + 1 if st.session_state.get('intake_info', {}).get('diagnosis') in diagnosis_symptoms_map else 0),
        key="intake_diag"
    )
    medication = st.text_input("Current Medication(s)", value=st.session_state.get('intake_info', {}).get('medication', ''), key="intake_med")
    symptoms_options = diagnosis_symptoms_map.get(diagnosis, diagnosis_symptoms_map["General"])
    symptoms_selected = st.multiselect(
        "Select your symptoms (you can select multiple)",
        options=symptoms_options,
        default=st.session_state.get('intake_info', {}).get('symptoms', []),
        key="intake_symptoms"
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        if not name.strip():
            st.warning("Please enter your name.")
        elif not diagnosis.strip():
            st.warning("Please select a diagnosis.")
        elif not symptoms_selected:
            st.warning("Please select at least one symptom.")
        else:
            st.success(f"Thank you {name}. Your intake form has been submitted.")
            st.session_state['intake_info'] = {
                "name": name.strip(),
                "age": age,
                "diagnosis": diagnosis,
                "medication": medication.strip(),
                "symptoms": symptoms_selected
            }
            if "user_activity_log" not in st.session_state:
                st.session_state.user_activity_log = []
            st.session_state.user_activity_log.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "intake_form_submit",
                "details": dict(st.session_state['intake_info'])
            })
    return submitted
if show_intake_form:
    st.header("Intake Form")
    with st.form("intake_form"):
        intake_form_body()
else:
    with st.expander("Show Intake Form (optional)", expanded=False):
        with st.form("intake_form_sidebar"):
            intake_form_body()

# --- Greeting ---
if personal_name:
    st.header(f"🌿 Welcome back, {personal_name}!")
else:
    st.header("🌿 Your Chronica Dashboard")

# --- OpenAI Chat Helper ---
def get_ai_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            n=1,
            stop=None
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"Error communicating with AI: {e}")
        return "Sorry, I am having trouble responding right now."

# --- GUIDED MODE ---
if mode == "Guided":
    st.write("Welcome to the guided mode. Let's explore your feelings step-by-step with compassion and care.")
    if 'guided_step' not in st.session_state:
        st.session_state.guided_step = 0
        st.session_state.guided_responses = []
    if 'past_summaries' not in st.session_state:
        st.session_state.past_summaries = []
    if 'guided_complete' not in st.session_state:
        st.session_state.guided_complete = False
    if 'guided_journal' not in st.session_state:
        st.session_state.guided_journal = ""
    if 'guided_tone' not in st.session_state:
        st.session_state.guided_tone = "Calm"
    guided_steps = [
        "How are you feeling today emotionally and physically?",
        "Can you describe any specific symptoms or sensations you are experiencing?",
        "What are some current stressors or challenges in your life?",
        "What coping strategies or supports have you found helpful?",
        "Is there anything else you'd like to share or explore?"
    ]
    voice_tones = ["Calm", "Supportive", "Uplifting", "Gentle", "Empowering"]
    st.session_state.guided_tone = st.selectbox(
        "AI Voice Tone", voice_tones,
        index=voice_tones.index(st.session_state.get("guided_tone", "Calm")),
        key="guided_tone_select"
    )
    if not st.session_state.guided_complete and st.session_state.guided_step < len(guided_steps):
        prompt = guided_steps[st.session_state.guided_step]
        response = st.text_area(prompt, key=f"guided_input_{st.session_state.guided_step}")
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Next", key=f"guided_next_{st.session_state.guided_step}"):
                if response.strip():
                    if len(st.session_state.guided_responses) == st.session_state.guided_step:
                        st.session_state.guided_responses.append(response.strip())
                    else:
                        st.session_state.guided_responses[st.session_state.guided_step] = response.strip()
                    st.session_state.guided_step += 1
                    if "user_activity_log" not in st.session_state:
                        st.session_state.user_activity_log = []
                    st.session_state.user_activity_log.append({
                        "timestamp": datetime.datetime.now().isoformat(),
                        "type": "guided_step",
                        "details": {
                            "step": st.session_state.guided_step,
                            "prompt": prompt,
                            "response": response.strip()
                        }
                    })
                    st.experimental_rerun()
                else:
                    st.warning("Please enter a response before continuing.")
        with col2:
            if st.session_state.guided_step > 0:
                if st.button("Previous", key=f"guided_prev_{st.session_state.guided_step}"):
                    if st.session_state.guided_responses:
                        st.session_state.guided_responses.pop()
                    st.session_state.guided_step = max(0, st.session_state.guided_step - 1)
                    st.experimental_rerun()
    elif not st.session_state.guided_complete:
        st.session_state.guided_complete = True
        st.success("Thank you for sharing. Here's a compassionate summary of your responses:")
        summary_prompt = [
            {"role": "system", "content":
                f"You are a compassionate, trauma-informed AI therapist. Use a {st.session_state.guided_tone.lower()} and supportive tone."},
            {"role": "user", "content": "Please provide a gentle, supportive summary of the following patient responses:"}
        ]
        for i, answer in enumerate(st.session_state.guided_responses):
            summary_prompt.append({"role": "user", "content": f"Q: {guided_steps[i]}\nA: {answer}"})
        summary = get_ai_response(summary_prompt)
        doctor_prompt = [
            {"role": "system", "content": "You are a professional medical AI assistant."},
            {"role": "user", "content": "Based on the following patient responses, provide a concise medical summary suitable for a doctor’s visit:"}
        ]
        for i, answer in enumerate(st.session_state.guided_responses):
            doctor_prompt.append({"role": "user", "content": f"Q: {guided_steps[i]}\nA: {answer}"})
        doctor_summary = get_ai_response(doctor_prompt)
        journal_prompt = [
            {"role": "system", "content":
                f"You are a supportive journaling coach and therapist. Based on the following responses, write a gentle, insightful journal entry or personal insight for the user (in the first person), using a {st.session_state.guided_tone.lower()} and reflective tone."}
        ]
        for i, answer in enumerate(st.session_state.guided_responses):
            journal_prompt.append({"role": "user", "content": f"Q: {guided_steps[i]}\nA: {answer}"})
        st.session_state.guided_journal = get_ai_response(journal_prompt)
        st.session_state.past_summaries.append({
            "reflection_summary": summary,
            "doctor_summary": doctor_summary,
            "journal": st.session_state.guided_journal,
            "tone": st.session_state.guided_tone,
            "timestamp": datetime.datetime.now().isoformat()
        })
        if len(st.session_state.past_summaries) > 5:
            st.session_state.past_summaries = st.session_state.past_summaries[-5:]
        if "user_activity_log" not in st.session_state:
            st.session_state.user_activity_log = []
        st.session_state.user_activity_log.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "guided_complete",
            "details": {
                "responses": list(st.session_state.guided_responses),
                "summary": summary
            }
        })
        st.markdown("### Your Chronica Reflection Summary")
        st.markdown(summary)
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Play Reflection Summary (Voice)"):
                speak(summary)
        with col2:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as f:
                f.write("Chronica Reflection Summary\n\n")
                for i, answer in enumerate(st.session_state.guided_responses):
                    f.write(f"{guided_steps[i]}\n{answer}\n\n")
                f.write("Summary:\n")
                f.write(summary)
                temp_filepath_reflection = f.name
            with open(temp_filepath_reflection, "rb") as file:
                st.download_button(
                    label="Download Reflection Summary as TXT",
                    data=file,
                    file_name="chronica_reflection_summary.txt",
                    mime="text/plain"
                )
            try:
                os.remove(temp_filepath_reflection)
            except Exception:
                pass
        st.markdown("### Doctor Visit Summary")
        with st.expander("View Doctor Summary", expanded=True):
            st.markdown(doctor_summary)
            col3, col4 = st.columns([1,1])
            with col3:
                if st.button("Play Doctor Summary (Voice)"):
                    speak(doctor_summary)
            with col4:
                with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as f:
                    f.write("Chronica Doctor Visit Summary\n\n")
                    for i, answer in enumerate(st.session_state.guided_responses):
                        f.write(f"{guided_steps[i]}\n{answer}\n\n")
                    f.write("Doctor Summary:\n")
                    f.write(doctor_summary)
                    temp_filepath_doctor = f.name
                with open(temp_filepath_doctor, "rb") as file:
                    st.download_button(
                        label="Download Doctor Summary as TXT",
                        data=file,
                        file_name="chronica_doctor_summary.txt",
                        mime="text/plain"
                    )
                try:
                    os.remove(temp_filepath_doctor)
                except Exception:
                    pass
        st.markdown("### AI-Generated Journal Entry / Insight")
        st.info(st.session_state.guided_journal)
        colj, _ = st.columns([1,1])
        with colj:
            if st.button("Play Journal Entry (Voice)"):
                speak(st.session_state.guided_journal)
        st.markdown("#### 🌱 *Remember: Every small step is progress. You are worthy of care and compassion.*")
        st.markdown("### What would you like to do next?")
        col_restart, col_chat, col_logout = st.columns([1,1,1])
        next_action = None
        with col_restart:
            if st.button("Restart"):
                next_action = "restart"
        with col_chat:
            if st.button("Go to Chat"):
                next_action = "chat"
        with col_logout:
            if st.button("Log Out"):
                next_action = "logout"
        if next_action == "restart":
            st.session_state.guided_step = 0
            st.session_state.guided_responses = []
            st.session_state.guided_complete = False
            st.session_state.guided_journal = ""
            st.experimental_rerun()
        elif next_action == "chat":
            st.session_state.guided_step = 0
            st.session_state.guided_responses = []
            st.session_state.guided_complete = False
            st.session_state.guided_journal = ""
            st.session_state['__streamlit_sidebar_radio__Choose mode:'] = "Chat"
            st.experimental_rerun()
        elif next_action == "logout":
            st.session_state.clear()
            st.experimental_rerun()
        if st.session_state.past_summaries:
            with st.expander("Past Summaries (last 5 sessions)"):
                for idx, summ in enumerate(reversed(st.session_state.past_summaries)):
                    time_str = summ.get("timestamp", "")[:19].replace("T", " ")
                    st.markdown(f"#### Session {len(st.session_state.past_summaries) - idx} (Tone: {summ.get('tone', 'Calm')}, {time_str})")
                    st.markdown("**Your Chronica Reflection Summary:**")
                    st.markdown(summ["reflection_summary"])
                    st.markdown("**Doctor Visit Summary:**")
                    st.markdown(summ["doctor_summary"])
                    st.markdown("**AI Journal Entry:**")
                    st.markdown(summ.get("journal",""))
                    st.markdown("---")

# --- CHAT MODE ---
elif mode == "Chat":
    st.write("Welcome to chat mode. Feel free to share anything, and I will respond with care and understanding.")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'openchat_tone' not in st.session_state:
        st.session_state.openchat_tone = "Calm"
    intake_info = st.session_state.get('intake_info')
    if intake_info:
        with st.expander("Your Intake Information", expanded=True):
            st.markdown(f"**Name:** {intake_info['name']}")
            st.markdown(f"**Age:** {intake_info['age']}")
            st.markdown(f"**Diagnosis:** {intake_info['diagnosis']}")
            st.markdown(f"**Medication:** {intake_info['medication'] or 'None'}")
            st.markdown(f"**Symptoms:** {', '.join(intake_info['symptoms'])}")
    openchat_voice_tones = ["Calm", "Supportive", "Uplifting", "Gentle", "Empowering"]
    st.session_state.openchat_tone = st.selectbox(
        "AI Voice Tone", openchat_voice_tones,
        index=openchat_voice_tones.index(st.session_state.get("openchat_tone", "Calm")),
        key="openchat_tone_select"
    )
    user_input = st.text_input("You:", key="openchat_input", placeholder="Type your message here...")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Send", key="openchat_send"):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
                if "user_activity_log" not in st.session_state:
                    st.session_state.user_activity_log = []
                st.session_state.user_activity_log.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "open_chat_user",
                    "details": {"message": user_input.strip()}
                })
                intake_str = ""
                if intake_info:
                    intake_str = (
                        f"User name: {intake_info.get('name','')}, "
                        f"Age: {intake_info.get('age','')}, "
                        f"Diagnosis: {intake_info.get('diagnosis','')}, "
                        f"Medication: {intake_info.get('medication','')}, "
                        f"Symptoms: {', '.join(intake_info.get('symptoms',[]))}."
                    )
                system_prompt = {
                    "role": "system",
                    "content": (
                        "You are Chronica, a trauma-informed, compassionate AI therapist. "
                        f"Respond with empathy, validation, and gentle guidance. "
                        f"Use a {st.session_state.openchat_tone.lower()} and supportive tone. "
                        + (f"Here is the user's intake info for context: {intake_str}" if intake_str else "")
                    )
                }
                messages = [system_prompt]
                for chat in st.session_state.chat_history:
                    messages.append({"role": chat["role"], "content": chat["content"]})
                ai_response = get_ai_response(messages)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                st.session_state.user_activity_log.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "open_chat_ai",
                    "details": {"message": ai_response}
                })
                if st.session_state.get("voice_output_enabled", False):
                    speak(ai_response)
                st.experimental_rerun()
            else:
                st.warning("Please enter a message before sending.")
    with col2:
        voice_enabled = st.checkbox("Enable voice output", key="voice_output_checkbox", value=st.session_state.get("voice_output_enabled", False))
        st.session_state["voice_output_enabled"] = voice_enabled
    for idx, chat in enumerate(st.session_state.chat_history):
=======
    user_input = st.text_input("You:", key="openchat_input")

    if st.button("Send", key="openchat_send"):
        if user_input.strip():
            # Append user message
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})

            # Prepare messages for OpenAI with system prompt for trauma-informed tone
            system_prompt = {
                "role": "system",
                "content": (
                    "You are Chronica, a trauma-informed, compassionate AI therapist. "
                    "Respond with empathy, validation, and gentle guidance."
                )
            }

            messages = [system_prompt]
            for chat in st.session_state.chat_history:
                messages.append({"role": chat["role"], "content": chat["content"]})

            ai_response = get_ai_response(messages)
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

            # Optionally speak the AI response
            if st.checkbox("Enable voice output", key="voice_output_checkbox"):
                speak(ai_response)
        else:
            st.warning("Please enter a message before sending.")

    # Display chat history
    for chat in st.session_state.chat_history:
>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**Chronica:** {chat['content']}")
<<<<<<< HEAD
=======

>>>>>>> f4e8ba55b4f94fdd1df392317d150003e324e8ae
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []