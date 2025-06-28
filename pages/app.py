# main app logic 

import base64
import streamlit as st
import numpy as np
import tempfile
import os
import time
import speech_recognition as sr
from pydub import AudioSegment
from datetime import datetime
from deep_translator import GoogleTranslator
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import whisper  


# ---------------------------
# --- Streamlit Page Config ---
# ---------------------------

st.set_page_config(page_title="Voicera", page_icon="🎤", layout="centered")

# ---------------------------
# --- Mobile-Responsive CSS ---
# ---------------------------

st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        .stApp {
            max-width: 100%;
            padding: 1rem;
        }
        @media only screen and (max-width: 600px) {
            .stApp {
                padding: 0.5rem !important;
            }
            button[kind="primary"] {
                width: 100%;
                font-size: 18px !important;
                padding: 12px !important;
            }
            .css-1cpxqw2, .css-1q8dd3e {
                font-size: 16px !important;
            }
            textarea {
                font-size: 16px !important;
            }
            .block-container {
                padding: 0.5rem 1rem !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# --- Logo ---
# ---------------------------

logo_path = "logo.png"  # Replace with your path
if os.path.exists(logo_path):
    logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()
    st.markdown(f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{logo_base64}' width='140'/>
            <h1 style='margin-bottom: 0; font-size: 22px;'>Voicera: Where every Voice finds its Words</h1>
            <p style='font-style: italic; font-size: 18px;'>Speak it. See it. Voicera it.</p>
            <p style='font-size: 12px; max-width: 600px; margin: auto;'>Voicera is your smart AI-assistant that turns your voice into accurate text using speech recognition. Record audio, stop, and download your transcript instantly.</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------
# 📜 Sidebar
# ---------------------------

# Sidebar theme selector
# ------------------- Theme Selector -------------------
# ------------------- Theme Selector -------------------
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.selectbox(
    "🎨 Choose Theme", 
    ["🪩 Pearl", "🌠 Dusk", "🏙 Sky", "🌷 Rose", "🌿 Mist", "🌇 Warm Sunset", "🎇 Midnight Violet"],
    index=0
)

# Define CSS for each theme with animated gradient
animated_themes = {
    "🪩 Pearl": """
        background: linear-gradient(-45deg, #ffffff, #f0f0f0, #e6e6e6, #dddddd);
        color: black;
    """,
    "🌠 Dusk": """
        background: linear-gradient(-45deg, #1c1c1c, #2a2a2a, #3a0f0f, #1a1a1a);
        color: white;
    """,
    "🏙 Sky": """
        background: linear-gradient(-45deg, #a1c4fd, #c2e9fb, #b2d8f7, #d0eaff);
        color: black;
    """,
    "🌷 Rose": """
        background: linear-gradient(-45deg, #ffdde1, #fbbdcd, #ffe0c3, #f8cdd0);
        color: black;
    """,
    "🌿 Mist": """
        background: linear-gradient(-45deg, #c1fcd3, #a3f7bf, #b0f3d1, #d2f1e4);
        color: black;
    """,
    "🌇 Warm Sunset": """
        background: linear-gradient(-45deg, #f3904f, #ff6e7f, #ffb88c, #fca085);
        color: black;
    """,
    "🎇 Midnight Violet": """
        background: linear-gradient(-45deg, #2c3e50, #4b0082, #6a0572, #1e1e2f);
        color: white;
    """
}

# Inject animated background style
st.markdown(f"""
    <style>
    .stApp {{
        {animated_themes[theme]}
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }}

    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    textarea, .stTextInput > div > input, .stDownloadButton button {{
        font-size: 16px !important;
    }}
    </style>
""", unsafe_allow_html=True)


st.sidebar.markdown("""
1. Upload a **.wav** or **.mp3** file  
2. Or **record live using mic**  
3. Select output language  
4. Transcription will run automatically
""")

if st.sidebar.button("🔄 Reset App"):
    keys_to_preserve = ["dashboard_data"]
    for key in list(st.session_state.keys()):
        if key not in keys_to_preserve:
            del st.session_state[key]
    st.rerun()

# ---------------------------
# --- Language Selection ---
# ---------------------------

lang_dict = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es"
}
lang_choice = st.selectbox("🌍 Select Output Language", list(lang_dict.keys()), index=0)
selected_lang = lang_dict[lang_choice]

# ---------------------------
# --- Session Vars ---
# ---------------------------

if "dashboard_data" not in st.session_state:
    st.session_state.dashboard_data = []

# ---------------------------
# --- Upload Audio ---
# ---------------------------

st.markdown("### 📁 Upload Audio File")
uploaded_file = st.file_uploader("Upload .mp3 or .wav file", type=["mp3", "wav"])

# ---------------------------
# --- Record from Mic ---
# ---------------------------

st.markdown("### 🎙️ Record using Microphone")
audio_bytes = audio_recorder(text="Click to Record", recording_color="#ea2525", neutral_color="#278cf6", icon_name="microphone")

# ---------------------------
# --- Transcription Function ---
# ---------------------------

# Load Whisper model (cached to avoid reloading)
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")  # Options: tiny, base, small, medium, large

model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

# ---------------------------
# --- Process Audio ---
# ---------------------------

# --- Process Audio ---
if audio_bytes or uploaded_file:
    with st.spinner("⏳ Processing..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            if uploaded_file:
                ext = os.path.splitext(uploaded_file.name)[1].lower()
                if ext == ".mp3":
                    audio = AudioSegment.from_mp3(uploaded_file)
                    audio.export(temp_audio.name, format="wav")
                else:
                    temp_audio.write(uploaded_file.read())
            elif audio_bytes:
                temp_audio.write(audio_bytes)
            audio_path = temp_audio.name

        try:
            start = time.time()
            original_text = transcribe_audio(audio_path)
            if selected_lang == "en":
                translated_text = original_text
            else:
                translated_text = GoogleTranslator(source="auto", target=selected_lang).translate(original_text)
            end = time.time()

            st.success("✅ Transcription & Translation Complete!")
            st.markdown(f"⏱️ **Time Taken:** `{round(end - start, 2)} sec`")
            st.text_area("📝 Translated Text", translated_text, height=200)

            st.download_button("📅 Download Transcript", translated_text, file_name="voicera_transcript.txt")

            tts = gTTS(translated_text, lang=selected_lang)
            tts_path = f"tts_{int(time.time())}.mp3"
            tts.save(tts_path)

            with open(tts_path, "rb") as f:
                tts_bytes = f.read()
                st.audio(tts_bytes, format="audio/mp3")
                st.download_button("🔊 Download Audio", tts_bytes, file_name="voicera_tts.mp3")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.dashboard_data.append({
                "Time": timestamp,
                "Input Language": "Auto Detected (Whisper)",
                "Output Language": lang_choice,
                "Transcript": translated_text
            })

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
            if 'tts_path' in locals() and os.path.exists(tts_path):
                os.remove(tts_path)

# ---------------------------
# 📊 Dashboard
# ---------------------------

if st.session_state.dashboard_data:
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 📊 Dashboard")
    st.sidebar.dataframe(st.session_state.dashboard_data[::-1], use_container_width=True)

# ---------------------------
# 🔹 Footer
# ---------------------------

st.markdown("---")
st.markdown("<center>Made with ❤️ by Himani Joshi</center>", unsafe_allow_html=True)
