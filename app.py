import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
import urllib.parse

# --- 1. SABSE PEHLE MEMORY (SESSION STATE) INITIALIZE KAREIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if 'items' not in st.session_state:
    st.session_state.items = [{"name": "", "rate": 0.0, "ready": False}]
if 'workers' not in st.session_state:
    st.session_state.workers = []
if 'fav_customers' not in st.session_state:
    st.session_state.fav_customers = []

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

# --- 4. MAIN CONTENT (LOGIN KE BAAD) ---
st.markdown('<p class="main-title">AL HUZAIFA DIGITAL</p>', unsafe_allow_html=True)
st.markdown('<p class="header-info">AL HUZAIFA TAILORING & EMB <br> Mob: 0554999723, 0504999723</p>', unsafe_allow_html=True)

tabs = st.tabs(["🏠 Home", "📑 Bills", "⭐ Favourite", "💳 Worker Card", "📦 Samples"])

# --- TAB 1: HOME ---
with tabs[0]:
    st.subheader("📈 Dashboard")
    c1, c2 = st.columns(2)
    c1.metric("Monthly Profit", "AED 12,500")
    c2.metric("Annual Profit", "AED 150,000")
    
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.error("🚨 URGENT ORDERS (Next 5 Days)")
        st.write("No urgent orders right now.")
    with col_b:
        st.success("📦 UNDELIVERED (Ready)")
        st.write("All orders delivered.")

# --- TAB 2: BILLS ---
with tabs[1]:
    with st.form("billing_form"):
        col1, col2, col3 = st.columns(3)
        b_no = col1.text_input("Bill No.")
        c_name = col2.text_input("Customer Name")
        c_phone = col3.text_input("Contact No.")
        
        o_date = col1.date_input("Order Date", datetime.now())
        d_date = col2.date_input("Delivery Date", datetime.now() + timedelta(days=5))
        advance = col3.number_input("Advance Paid", min_value=0.0)
        
        st.write("---")
        # Billing calculation
        total_orig = 0
        total_vat = 0
        
        for i, item in enumerate(st.session_state.items):
            ic1, ic2, ic3, ic4 = st.columns([3, 2, 2, 1])
            item['name'] = ic1.text_input(f"Item {i+1}", key=f"it{i}")
            item['rate'] = ic2.number_input(f"Rate", key=f"ir{i}", min_value=0.0)
            v = item['rate'] * 0.05
            ic3.write(f"VAT: {v:.2f}")
            item['ready'] = ic4.checkbox("Ready", key=f"rd{i}")
            total_orig += item['rate']
            total_vat += v
            
        grand_total = total_orig + total_vat
        pending = grand_total - advance
        
        st.write(f"**Total Rate:** {total_orig:.2f} | **Total VAT:** {total_vat:.2f}")
        st.success(f"**Grand Total: AED {grand_total:.2f}**")
        st.error(f"**Pending: AED {pending:.2f}**")
        
        if st.form_submit_button("💾 Save Bill"):
            st.success("Bill Saved Successfully!")

    if st.button("➕ Add More Item"):
        st.session_state.items.append({"name": "", "rate": 0.0, "ready": False})
        st.rerun()

# --- TAB 3: FAVOURITE ---
with tabs[2]:
    st.subheader("⭐ Star Customers")
    m_fields = ["Length", "Shoulder", "Sleeves", "Chest", "Hip", "Waist", "Neck", "Armhole", "Bottom", "Side"]
    with st.expander("Add Measurement"):
        f_name = st.text_input("Name")
        f_cols = st.columns(2)
        for i, f in enumerate(m_fields):
            f_cols[i%2].number_input(f, step=0.1)
        st.button("Save to Star List")

# --- TAB 4: WORKER CARD ---
with tabs[3]:
    st.subheader("💳 Karigar Card")
    w_n = st.text_input("Worker Name")
    st.write("No items assigned yet.")
    st.button("📥 Download PDF")

# --- TAB 5: SAMPLES ---
with tabs[4]:
    st.subheader("📦 Samples")
    st.camera_input("Take Photo")
    st.file_uploader("Gallery")
    st.button("Save Sample")
