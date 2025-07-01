import os
import time
import ssl
import smtplib
import requests
import re
import streamlit as st
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()


def render_followup_ui():
    # ——— Defaults & session init —————————————————————————
    DEFAULTS = {
        "contacts": [],
        "previews": {},
        "approved": set(),
        "openai_api_key": os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY"),
        "pipedrive_domain": os.getenv("PIPEDRIVE_DOMAIN", "Naware") or st.secrets.get("PIPEDRIVE_DOMAIN"),
        "pipedrive_api_token": os.getenv("PIPEDRIVE_API_TOKEN") or st.secrets.get("PIPEDRIVE_API_TOKEN"),
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com") or st.secrets.get("SMTP_SERVER"),
        "smtp_port": os.getenv("SMTP_PORT", "587") or st.secrets.get("SMTP_PORT"),
        "email_username": os.getenv("EMAIL_USERNAME") or st.secrets.get("EMAIL_USERNAME"),
        "email_password": os.getenv("EMAIL_PASSWORD") or st.secrets.get("EMAIL_PASSWORD"),
        "email_sender_name": os.getenv("EMAIL_SENDER_NAME", "Team Naware") or st.secrets.get("EMAIL_SENDER_NAME"),
        "selected_model": "gpt-4o-mini",
    }

    for k, v in DEFAULTS.items():
        if v is None and k in ["openai_api_key", "pipedrive_api_token", "email_username", "email_password"]:
            st.error(f"Missing required environment variable: {k}")
            st.stop()
        st.session_state.setdefault(k, v)

    # ——— Helpers —————————————————————————————————————
    def validate_email(e):
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', e))

    def get_base_url():
        return f"https://{st.session_state.pipedrive_domain}.pipedrive.com/api/v1"

    def find_or_create_deal(org):
        try:
            resp = requests.get(
                f"{get_base_url()}/deals/search",
                params={"api_token": st.session_state.pipedrive_api_token, "term": org},
            ).json()
            if resp.get("success") and resp["data"]["items"]:
                return resp["data"]["items"][0]["item"]["id"]
            new = requests.post(
                f"{get_base_url()}/deals",
                params={"api_token": st.session_state.pipedrive_api_token},
                json={"title": f"{org} – Demo Follow-Up", "status": "open"},
            ).json()
            return new["data"]["id"] if new.get("success") else None
        except Exception as e:
            st.error(f"Error with Pipedrive: {e}")
            return None

    def log_activity(deal_id, subj, body):
        try:
            requests.post(
                f"{get_base_url()}/activities",
                params={"api_token": st.session_state.pipedrive_api_token},
                json={"subject": subj, "note": body, "deal_id": deal_id, "type": "email", "done": 1},
            )
        except Exception as e:
            st.error(f"Error logging activity: {e}")

    def gen_email(name, org, date, cta, product):
        date_str = date.strftime("%B %d, %Y")
        prompt = (
            f"SYSTEM: You are a professional sales engineer at Naware, makers of the "Wipe All Weedrupter," an innovative steam-based, AI-driven weed control solution.\n\n"
            f"USER: Write a warm, multi-paragraph thank-you email to {name} at {org} for attending our demo of {product} on {date_str}. Be sure to:\n"
            f"  . Do not include a subject line in the email body.\n"
            f"  • Express genuine appreciation for their time and thoughtful questions during the demo.\n"
            f"  • Highlight their role/industry and why their feedback matters to us as early adopters.\n"
            f"  • Invite them to share any photos or notes they took—this helps us tailor future improvements.\n"
            f"  • Clearly outline next steps, including a single call-to-action link to schedule a follow-up discussion: {cta}\n"
            f"  • Reinforce our "fail fast, learn fast" philosophy and our commitment to close collaboration.\n"
            f"  • Sign off warmly as {st.session_state.email_sender_name}, optionally adding a P.S. with a quick tip or resource relevant to their use case.\n\n"
            f"Return just the email body (no subject line) in plain text."
        )

        try:
            llm = ChatOpenAI(
                model_name=st.session_state.selected_model,
                temperature=0.7,
                max_tokens=350,
                api_key=st.session_state.openai_api_key
            )
            response = llm.predict(prompt)
            return response.strip()
        except Exception as e:
            st.error(f"Error generating email: {e}")
            return f"Error generating email content: {str(e)}"

    def send_email(to_addr, subj, body, deal_id=None):
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"], msg["From"], msg["To"] = subj, st.session_state.email_username, to_addr
            if deal_id:
                msg["Bcc"] = f"naware+deal{deal_id}@pipedrivemail.com"
            msg.attach(MIMEText(body, "plain"))
            msg.attach(MIMEText(body.replace("\n", "<br>"), "html"))
            ctx = ssl.create_default_context()
            with smtplib.SMTP(st.session_state.smtp_server, int(st.session_state.smtp_port)) as srv:
                srv.starttls(context=ctx)
                srv.login(st.session_state.email_username, st.session_state.email_password)
                srv.sendmail(
                    st.session_state.email_username,
                    [to_addr] + ([msg["Bcc"]] if deal_id else []),
                    msg.as_string()
                )
            return True
        except Exception as e:
            st.error(f"Error sending email: {e}")
            return False

    # ——— Sidebar settings —————————————————————————————
    with st.sidebar:
        st.header("⚙️ Settings")
        st.session_state.selected_model = st.selectbox("AI Model",
                                                       ["gpt-4o-mini",
                                                        "gpt-4o",
                                                        "gpt-3.5-turbo"],
                                                       index=["gpt-4o-mini",
                                                              "gpt-4o",
                                                              "gpt-3.5-turbo"].index(st.session_state.selected_model))
        st.subheader("Pipedrive")
        st.session_state.pipedrive_domain = st.text_input("Domain", st.session_state.pipedrive_domain)
        st.session_state.pipedrive_api_token = st.text_input(
            "API Token", st.session_state.pipedrive_api_token, type="password")

        st.subheader("Email SMTP")
        st.session_state.smtp_server = st.text_input("SMTP Server", st.session_state.smtp_server)
        smtp_port_str = st.text_input("SMTP Port", str(st.session_state.smtp_port))
        if smtp_port_str.isdigit():
            st.session_state.smtp_port = int(smtp_port_str)
        else:
            st.error("🚨 SMTP Port must be a number")
        st.session_state.email_sender_name = st.text_input("Sender Name", st.session_state.email_sender_name)

    # ——— Main page ————————————————————————————————
    st.title("📧 Demo Follow-Up Email Generator")

    # 1) Add contact form
    st.markdown("### ➕ Add a contact")
    with st.form("add_contact", clear_on_submit=True):
        n = st.text_input("Name")
        e = st.text_input("Email")
        o = st.text_input("Organization")
        d = st.date_input("Demo Date", datetime.today())
        cta = st.text_input("CTA Link")
        prod = st.selectbox("Product Demo'd", ["Wipe All", "AI-driven solution"])
        if st.form_submit_button("Add contact"):
            if not (n and validate_email(e) and o and cta):
                st.error("Please fill name, valid email, org & CTA.")
            else:
                st.session_state.contacts.append({
                    "name": n, "email": e, "org": o,
                    "demo_date": d, "cta": cta, "product": prod
                })

    # 2) Preview & approve
    st.markdown("### 👀 Preview & Edit Emails")
    for idx, ct in enumerate(st.session_state.contacts):
        subj = f"Thank you, {ct['org']} – Next steps"
        if idx not in st.session_state.previews:
            st.session_state.previews[idx] = gen_email(
                ct["name"], ct["org"], ct["demo_date"], ct["cta"], ct["product"]
            )

        body = st.text_area(
            f"{ct['name']} @ {ct['org']} — Edit your email:",
            value=st.session_state.previews[idx],
            height=200,
            key=f"body_{idx}"
        )
        st.session_state.previews[idx] = body

        if st.checkbox("Approve this email", key=f"ok_{idx}"):
            st.session_state.approved.add(idx)
        st.write("---")

    # 3) Send & log
    approved = sorted(st.session_state.approved)
    if approved:
        if st.button(f"✉️ Send & Log {len(approved)} emails"):
            success_count = 0
            for i in approved:
                ct = st.session_state.contacts[i]
                subj = f"Thank you, {ct['org']} – Next steps"
                body = st.session_state.previews[i]

                # find or create deal
                deal_id = find_or_create_deal(ct["org"])
                # send email
                if send_email(ct["email"], subj, body, deal_id=deal_id):
                    success_count += 1
                    # log in Pipedrive
                    if deal_id:
                        log_activity(deal_id, subj, body)
                time.sleep(0.5)

            if success_count > 0:
                st.success(f"✅ Sent & logged {success_count} emails")

                # Remove only the sent contacts and their associated data
                remaining_contacts = []
                remaining_previews = {}

                for idx, contact in enumerate(st.session_state.contacts):
                    if idx not in approved:
                        new_idx = len(remaining_contacts)
                        remaining_contacts.append(contact)
                        if idx in st.session_state.previews:
                            remaining_previews[new_idx] = st.session_state.previews[idx]

                st.session_state.contacts = remaining_contacts
                st.session_state.previews = remaining_previews
                st.session_state.approved.clear()

                # Force a rerun to refresh the UI
                time.sleep(2)
                st.rerun()
            else:
                st.error("Failed to send any emails. Please check your configuration.")

    else:
        st.info("Check ✔️ boxes above to approve emails, then click Send & Log.")
