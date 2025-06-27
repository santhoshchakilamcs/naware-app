# # combined_app.py

# import os
# import openai
# import streamlit as st

# # ─── Import your three app‐modules ────────────────────────────────────────────
# from Investor_update import render_investor_ui
# from Newsletter import render_newsletter_ui
# from test import render_followup_ui  # rename if needed

# # ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Naware Multi-App Hub",
#     page_icon="📰✉️📈",
#     layout="wide",
# )

# # inject a bit of custom CSS
# st.markdown("""
#     <style>
#       /* make the sidebar header purple */
#       .css-1d391kg .css-1d391kg {
#         background: linear-gradient(135deg, #5A2A83 0%, #7C3AED 100%);
#       }
#       /* customize the block titles */
#       h1, h2, h3 {
#         color: #E83E8C !important;
#       }
#       /* tweak buttons to use pink outline */
#       button[kind="primary"] {
#         border: 2px solid #E83E8C !important;
#       }
#       /* link colors */
#       a {
#         color: #FF80AB !important;
#       }
#     </style>
# """, unsafe_allow_html=True)

# # ─── SHARED DEFAULTS ─────────────────────────────────────────────────────────
# DEFAULTS = {
#     "openai_api_key": os.getenv("OPENAI_API_KEY", "sk-svcacct-r3g8u1HTW-ixDqI5HW7JMgW3g1_qemT5h313pXChv05WH6hTgEF28BEwcCEJUghT3BlbkFJ5mI1Sb4EhsooE3f_V-9Aw7dJeZxpVOvjc52u2L9tdW6LryRShTI0mUDqoksUUAA"),
#     "pipedrive_domain": os.getenv("PIPEDRIVE_DOMAIN", "Naware"),
#     "pipedrive_api_token": os.getenv("PIPEDRIVE_API_TOKEN", "01f15a31881505c1271820bdb31b15d1041d6a26"),
#     "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
#     "smtp_port": os.getenv("SMTP_PORT", "587"),
#     "email_username": os.getenv("EMAIL_USERNAME", "santhosh@naware.io"),
#     "email_password": os.getenv("EMAIL_PASSWORD", "nkwk ruty bwfk jhop"),
#     "email_sender_name": os.getenv("EMAIL_SENDER_NAME", "Team Naware"),
#     "selected_model" : "gpt-4o-mini",
# }

# for k, v in DEFAULTS.items():
#     st.session_state.setdefault(k, v)

# openai.api_key = st.session_state.openai_api_key

# # ─── APP SELECTOR ─────────────────────────────────────────────────────────────
# st.sidebar.title("🚀 App Navigator")
# app_choice = st.sidebar.selectbox(
#     "Choose an app:",
#     [
#         "Investor Update",
#         "Newsletter Generator",
#         "Demo Follow-Up Emails"
#     ]
# )

# # ─── DISPATCH ────────────────────────────────────────────────────────────────
# if app_choice == "Investor Update":
#     render_investor_ui()

# elif app_choice == "Newsletter Generator":
#     render_newsletter_ui()

# elif app_choice == "Demo Follow-Up Emails":
#     render_followup_ui()


# combined_app.py

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
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "pipedrive_domain": os.getenv("PIPEDRIVE_DOMAIN", "Naware"),
    "pipedrive_api_token": os.getenv("PIPEDRIVE_API_TOKEN"),
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": os.getenv("SMTP_PORT", "587"),
    "email_username": os.getenv("EMAIL_USERNAME"),
    "email_password": os.getenv("EMAIL_PASSWORD"),
    "email_sender_name": os.getenv("EMAIL_SENDER_NAME", "Team Naware"),
    "selected_model": "gpt-4o-mini",
}

for k, v in DEFAULTS.items():
    if v is None and k in ["openai_api_key", "pipedrive_api_token", "email_username", "email_password"]:
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
