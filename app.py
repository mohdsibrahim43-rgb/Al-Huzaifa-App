import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. INITIALIZATION (ERROR FIX) ---
# Ye hissa sabse zaroori hai error hatane ke liye
if 'items' not in st.session_state or callable(st.session_state.items):
    st.session_state['items'] = [{"name": "", "rate": 0.0, "ready": False}]
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 2. THEME & CONFIG ---
st.set_page_config(page_title="AL HUZAIFA DIGITAL", layout="wide")

st.markdown("""
    <style>
    .main-title { color: #1E8449; font-weight: bold; font-size: 45px; text-align: center; }
    .header-info { color: #27AE60; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { position: fixed; bottom: 0; left: 0; width: 100%; background: white; z-index: 1000; border-top: 2px solid #1E8449; display: flex; justify-content: space-around; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>🔐 AL HUZAIFA LOGIN</h2>", unsafe_allow_html=True)
    pw = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if pw == "HUZAIFA2026":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Galat Password!")
    st.stop()

# --- 4. MAIN APP ---
st.markdown('<p class="main-title">AL HUZAIFA DIGITAL</p>', unsafe_allow_html=True)
st.markdown('<p class="header-info">AL HUZAIFA TAILORING & EMB <br> Mob: 0554999723, 0504999723</p>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 Home", "📑 Bills", "⭐ Favourite", "💳 Card", "📦 Samples"])

# --- TAB: BILLS ---
with tabs[1]:
    with st.form("new_bill_form"):
        col1, col2, col3 = st.columns(3)
        b_no = col1.text_input("Bill No.")
        c_name = col2.text_input("Customer Name")
        c_phone = col3.text_input("Contact No.")
        
        st.write("---")
        total_orig = 0
        
        # Error fix: loop through the list safely
        current_items = st.session_state['items']
        for i, item in enumerate(current_items):
            ic1, ic2, ic3, ic4 = st.columns([3, 2, 2, 1])
            item['name'] = ic1.text_input(f"Item {i+1}", key=f"name_{i}")
            item['rate'] = ic2.number_input(f"Rate AED", key=f"rate_{i}", min_value=0.0)
            vat_val = item['rate'] * 0.05
            ic3.write(f"VAT: {vat_val:.2f}")
            item['ready'] = ic4.checkbox("Ready", key=f"ready_{i}")
            total_orig += item['rate']

        if st.form_submit_button("💾 Save Bill"):
            st.success(f"Bill #{b_no} Save ho gaya!")

    if st.button("➕ Add New Item"):
        st.session_state['items'].append({"name": "", "rate": 0.0, "ready": False})
        st.rerun()

# --- OTHER TABS (Placeholders) ---
with tabs[0]: st.subheader("📈 Dashboard Coming Soon")
with tabs[2]: st.subheader("⭐ Favourite List")
with tabs[3]: st.subheader("💳 Worker Management")
with tabs[4]: st.subheader("📦 Product Samples")
