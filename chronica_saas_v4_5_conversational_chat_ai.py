import streamlit as st
import openai
import pyttsx3
import tempfile
import os

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

# Guided mode: step-based conversational flow
if mode == "Guided":
    st.write("Welcome to the guided mode. Let's explore your feelings step-by-step with compassion and care.")

    if 'guided_step' not in st.session_state:
        st.session_state.guided_step = 0
        st.session_state.guided_responses = []

    guided_steps = [
        "How are you feeling today emotionally and physically?",
        "Can you describe any specific symptoms or sensations you are experiencing?",
        "What are some current stressors or challenges in your life?",
        "What coping strategies or supports have you found helpful?",
        "Is there anything else you'd like to share or explore?"
    ]

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
            {"role": "user", "content": "Please provide a gentle, supportive summary of the following patient responses:"}
        ]
        for i, answer in enumerate(st.session_state.guided_responses):
            summary_prompt.append({"role": "user", "content": f"Q: {guided_steps[i]}\nA: {answer}"})

        summary = get_ai_response(summary_prompt)
        st.markdown(f"### Summary:\n{summary}")

        if st.button("Play Summary (Voice)"):
            speak(summary)

        if st.button("Export Summary"):
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".txt") as f:
                f.write("Chronica Healing Garden Summary\n\n")
                for i, answer in enumerate(st.session_state.guided_responses):
                    f.write(f"{guided_steps[i]}\n{answer}\n\n")
                f.write("Summary:\n")
                f.write(summary)
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
elif mode == "Open Chat":
    st.write("Welcome to open chat mode. Feel free to share anything, and I will respond with care and understanding.")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display intake info if available
    intake_info = st.session_state.get('intake_info')
    if intake_info:
        with st.expander("Your Intake Information"):
            st.markdown(f"**Name:** {intake_info['name']}")
            st.markdown(f"**Age:** {intake_info['age']}")
            st.markdown(f"**Diagnosis:** {intake_info['diagnosis']}")
            st.markdown(f"**Medication:** {intake_info['medication'] or 'None'}")
            st.markdown(f"**Symptoms:** {', '.join(intake_info['symptoms'])}")

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
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**Chronica:** {chat['content']}")

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []