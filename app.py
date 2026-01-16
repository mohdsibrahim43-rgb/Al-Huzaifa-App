import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
import urllib.parse

# --- 1. INITIALIZE SESSION STATE (IMPORTANT FIX) ---
# Ye code sabse upar hona chahiye taaki error na aaye
if 'items' not in st.session_state:
    st.session_state.items = [{"name": "", "rate": 0.0, "ready": False}]
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 2. APP CONFIG & THEME ---
st.set_page_config(page_title="AL HUZAIFA DIGITAL", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #1E8449; font-weight: bold; font-size: 45px; text-align: center; margin-bottom: 0px; }
    .header-info { color: #27AE60; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { position: fixed; bottom: 0; left: 0; width: 100%; background: white; z-index: 1000; border-top: 2px solid #1E8449; display: flex; justify-content: space-around; }
    div[data-testid="stMetricValue"] { color: #1E8449; }
    .urgent-card { background-color: #FDEDEC; border-left: 5px solid #CB4335; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>🔐 AL HUZAIFA LOGIN</h2>", unsafe_allow_html=True)
    password = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if password == "HUZAIFA2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong Password!")
    st.stop()

# --- 4. MAIN APP CONTENT ---
st.markdown('<p class="main-title">AL HUZAIFA DIGITAL</p>', unsafe_allow_html=True)
st.markdown('<p class="header-info">AL HUZAIFA TAILORING & EMB <br> Mob: 0554999723, 0504999723</p>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 Home", "📑 Bills", "⭐ Favourite", "💳 Worker Card", "📦 Samples"])

# --- TAB: BILLS (Updated with fix) ---
with tabs[1]:
    with st.form("billing_form"):
        col1, col2, col3 = st.columns(3)
        b_no = col1.text_input("Bill No.")
        c_name = col2.text_input("Customer Name")
        c_phone = col3.text_input("Contact No.")
        
        o_date = col1.date_input("Order Date", datetime.now())
        d_date = col2.date_input("Delivery Date", datetime.now() + timedelta(days=7))
        advance = col3.number_input("Advance Paid", min_value=0.0)
        
        st.write("---")
        # Ab ye loop error nahi dega
        for i, item in enumerate(st.session_state.items):
            ic1, ic2, ic3, ic4 = st.columns([3, 2, 2, 1])
            item['name'] = ic1.text_input(f"Item {i+1}", key=f"it{i}")
            item['rate'] = ic2.number_input(f"Rate", key=f"ir{i}", min_value=0.0)
            vat = item['rate'] * 0.05
            ic3.write(f"VAT: {vat:.2f}")
            item['ready'] = ic4.checkbox("Ready", key=f"rd{i}")
            
        if st.form_submit_button("💾 Save Bill & Send Greeting"):
            st.success("Bill Saved!")

    if st.button("➕ Add More Item"):
        st.session_state.items.append({"name": "", "rate": 0.0, "ready": False})
        st.rerun()

# (Baki sections: Home, Favourite, Worker, Samples ka purana code niche add kar sakte hain)
