import streamlit as st
import base64
import os

# ----- Page Config -----
st.set_page_config(page_title="Voicera", page_icon="🎤", layout="centered")

# ----- Logo -----
logo_path = "D:/speech_to_text/logo.png"
if os.path.exists(logo_path):
    logo_base64 = base64.b64encode(open(logo_path, "rb").read()).decode()
    logo_html = f"<img src='data:image/png;base64,{logo_base64}' width='200' style='margin-bottom: 10px;'/>"
else:
    logo_html = "<h1>Voicera</h1>"

# ----- Custom Aurora Theme -----
st.markdown("""
    <style>
    body {
        margin: 0;
        padding: 0;
    }

    .stApp {
        background: linear-gradient(-45deg, #8360c3, #2ebf91, #7f7fd5, #91eae4);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: white;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    h1, h2, h3, p {
        text-align: center;
        color: white !important;
    }

    .launch-btn {
        padding: 15px 35px;
        font-size: 20px;
        background-color: #ffffff10;
        border: 2px solid #ffffff70;
        border-radius: 12px;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    }

    .launch-btn:hover {
        background-color: #ffffff30;
        transform: scale(1.05);
        border-color: white;
    }

    </style>
""", unsafe_allow_html=True)

# ----- Main Content -----
st.markdown(f"""
    <div style='text-align: center; padding-top: 60px;'>
        {logo_html}
        <h1>Voicera: Where Every Voice Finds Its Words</h1>
        <p style='font-size:22px;'>AI-powered voice-to-text assistant for fast, smart, and accurate conversion</p>
        <br><br>
        <a href="/app" target="_self">
            <button class='launch-btn'>🚀 Launch Voicera App</button>
        </a>
    </div>
""", unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.markdown("<center>Made with ❤️ by Himani Joshi</center>", unsafe_allow_html=True)

