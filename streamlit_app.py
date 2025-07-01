from test import render_followup_ui  # rename if needed
from Newsletter import render_newsletter_ui
from Investor_update import render_investor_ui
import os
import streamlit as st

from dotenv import load_dotenv
load_dotenv()


# ─── Import your three app‐modules ────────────────────────────────────────────

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Naware Multi-App Hub",
    page_icon="📰✉️📈",
    layout="wide",
)

# Enhanced CSS to match banner colors
st.markdown("""
    <style>
      /* Main app background gradient */
      .stApp {
        background: linear-gradient(135deg, #3D1A78 0%, #6B2C91 50%, #4A1E87 100%) !important;
      }

      /* Sidebar styling */
      .css-1d391kg {
        background: linear-gradient(180deg, #4A1E87 0%, #3D1A78 100%) !important;
        border-right: 2px solid #FF4081 !important;
      }

      /* Main content area */
      .main .block-container {
        background: rgba(77, 30, 135, 0.1) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 64, 129, 0.2) !important;
        backdrop-filter: blur(10px) !important;
      }

      /* Headers and titles */
      h1, h2, h3, h4, h5, h6 {
        color: #FF4081 !important;
        text-shadow: 0 0 10px rgba(255, 64, 129, 0.3) !important;
      }

      /* Sidebar title special styling */
      .css-1d391kg h1 {
        color: #FFFFFF !important;
        text-align: center !important;
        background: linear-gradient(45deg, #FF4081, #E91E63) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
      }

      /* Buttons */
      .stButton > button {
        background: linear-gradient(45deg, #FF4081, #E91E63) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        box-shadow: 0 4px 15px rgba(255, 64, 129, 0.4) !important;
        transition: all 0.3s ease !important;
      }

      .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 64, 129, 0.6) !important;
      }

      /* Selectbox and inputs */
      .stSelectbox > div > div {
        background-color: rgba(74, 30, 135, 0.8) !important;
        border: 1px solid #FF4081 !important;
        color: white !important;
      }

      .stTextInput > div > div > input {
        background-color: rgba(74, 30, 135, 0.8) !important;
        border: 1px solid #FF4081 !important;
        color: white !important;
      }

      .stTextArea > div > div > textarea {
        background-color: rgba(74, 30, 135, 0.8) !important;
        border: 1px solid #FF4081 !important;
        color: white !important;
      }

      /* Links */
      a {
        color: #FF4081 !important;
        text-decoration: none !important;
      }

      a:hover {
        color: #E91E63 !important;
        text-shadow: 0 0 5px rgba(255, 64, 129, 0.5) !important;
      }

      /* Success/info boxes */
      .stSuccess {
        background: linear-gradient(45deg, rgba(255, 64, 129, 0.1), rgba(233, 30, 99, 0.1)) !important;
        border-left: 4px solid #FF4081 !important;
      }

      .stInfo {
        background: linear-gradient(45deg, rgba(74, 30, 135, 0.2), rgba(107, 44, 145, 0.2)) !important;
        border-left: 4px solid #6B2C91 !important;
      }

      /* Metrics and dataframes */
      .metric-container {
        background: rgba(74, 30, 135, 0.3) !important;
        border: 1px solid rgba(255, 64, 129, 0.3) !important;
        border-radius: 10px !important;
      }

      /* Expander */
      .streamlit-expanderHeader {
        background: rgba(74, 30, 135, 0.5) !important;
        border: 1px solid #FF4081 !important;
        color: white !important;
      }

      /* Progress bars */
      .stProgress > div > div > div {
        background: linear-gradient(45deg, #FF4081, #E91E63) !important;
      }

      /* Custom glow effect for important elements */
      .css-1d391kg .css-1d391kg::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, rgba(255, 64, 129, 0.1) 0%, transparent 70%);
        pointer-events: none;
      }
    </style>
""", unsafe_allow_html=True)

# ─── SHARED DEFAULTS ─────────────────────────────────────────────────────────


DEFAULTS = {
    "OPENAI_API_KEY": st.secrets.get("OPENAI_API_KEY"),
    "PIPEDRIVE_DOMAIN": st.secrets.get("PIPEDRIVE_DOMAIN", "Naware"),
    "PIPEDRIVE_API_TOKEN": st.secrets.get("PIPEDRIVE_API_TOKEN"),
    "SMTP_SERVER": st.secrets.get("SMTP_SERVER", "smtp.gmail.com"),
    "SMTP_PORT": st.secrets.get("SMTP_PORT", "587"),
    "EMAIL_USERNAME": st.secrets.get("EMAIL_USERNAME"),
    "EMAIL_PASSWORD": st.secrets.get("EMAIL_PASSWORD"),
    "EMAIL_SENDER_NAME": st.secrets.get("EMAIL_SENDER_NAME", "Team Naware"),
    "selected_model": "gpt-4o-mini",
}

for k, v in DEFAULTS.items():
    if v is None and k in ["OPENAI_API_KEY", "PIPEDRIVE_API_TOKEN", "EMAIL_USERNAME", "EMAIL_PASSWORD"]:
        st.error(f"Missing required environment variable: {k}")
        st.stop()
    st.session_state.setdefault(k, v)


# ─── APP SELECTOR WITH ENHANCED STYLING ─────────────────────────────────────────
st.sidebar.title("🚀 Naware App Hub")
st.sidebar.markdown("---")

# Add a nice description
st.sidebar.markdown("""
<div style='text-align: center; padding: 10px; background: rgba(255, 64, 129, 0.1); border-radius: 10px; margin-bottom: 20px;'>
    <p style='color: white; margin: 0; font-size: 14px;'>
        🌟 <strong>AI & Robotics Solutions</strong><br>
        <em>Health • Safety • Sustainability</em>
    </p>
</div>
""", unsafe_allow_html=True)

app_choice = st.sidebar.selectbox(
    "Choose an application:",
    [
        "📊 Investor Update",
        "📰 Newsletter Generator",
        "📧 Demo Follow-Up Emails"
    ]
)

# Add some info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; padding: 15px; background: rgba(74, 30, 135, 0.3); border-radius: 10px;'>
    <p style='color: #FF4081; margin: 0; font-size: 12px;'>
        <strong>Naware Technologies</strong><br>
        🌱 Turf Weed Control with 100% Water<br>
        🤖 Powered by AI & Robotics
    </p>
</div>
""", unsafe_allow_html=True)

# ─── DISPATCH ────────────────────────────────────────────────────────────────
if app_choice == "📊 Investor Update":
    render_investor_ui()

elif app_choice == "📰 Newsletter Generator":
    render_newsletter_ui()

elif app_choice == "📧 Demo Follow-Up Emails":
    render_followup_ui()
