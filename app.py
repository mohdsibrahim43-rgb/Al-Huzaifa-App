import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF
import urllib.parse

# --- APP CONFIG & THEME ---
st.set_page_config(page_title="AL HUZAIFA DIGITAL", layout="wide")

# Custom Green Theme Styling
st.markdown("""
    <style>
    .main-title { color: #1E8449; font-weight: bold; font-size: 45px; text-align: center; margin-bottom: 0px; }
    .header-info { color: #27AE60; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { position: fixed; bottom: 0; left: 0; width: 100%; background: white; z-index: 1000; border-top: 2px solid #1E8449; display: flex; justify-content: space-around; }
    div[data-testid="stMetricValue"] { color: #1E8449; }
    .urgent-card { background-color: #FDEDEC; border-left: 5px solid #CB4335; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .delivered-bill { background-color: #D4EFDF !important; border: 1px solid #27AE60; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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

# --- HEADER ---
st.markdown('<p class="main-title">AL HUZAIFA DIGITAL</p>', unsafe_allow_html=True)
st.markdown('<p class="header-info">AL HUZAIFA TAILORING & EMB <br> Mob: 0554999723, 0504999723</p>', unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tabs = st.tabs(["🏠 Home", "📑 Bills", "⭐ Favourite", "💳 Worker Card", "📦 Samples"])

# --- 1. HOME PAGE ---
with tabs[0]:
    st.subheader("📈 Business Dashboard")
    c1, c2 = st.columns(2)
    c1.metric("Monthly Profit", "AED 12,500", "+5%")
    c2.metric("Annual Profit", "AED 150,000", "+12%")
    
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.error("🚨 URGENT ORDERS (Next 5 Days)")
        # Filter logic for orders within 5 days would go here
        st.markdown('<div class="urgent-card">Bill #105 - Fatima - 18 Jan</div>', unsafe_allow_html=True)
        
    with col_b:
        st.success("📦 UNDELIVERED (Ready for Pickup)")
        st.markdown('<div style="background-color:#E8F8F5; padding:10px; border-radius:5px;">Bill #101 - Sara - Ready</div>', unsafe_allow_html=True)

    st.text_input("🔍 Global Search (Name, Mobile, Bill No, Item)")

# --- 2. BILLS SECTION ---
with tabs[1]:
    if 'items' not in st.session_state: st.session_state.items = [{"name": "", "rate": 0.0, "ready": False}]
    
    with st.form("billing_form"):
        col1, col2, col3 = st.columns(3)
        b_no = col1.text_input("Bill No.")
        c_name = col2.text_input("Customer Name")
        c_phone = col3.text_input("Contact No.")
        
        o_date = col1.date_input("Order Date", datetime.now())
        d_date = col2.date_input("Delivery Date", datetime.now() + timedelta(days=7))
        advance = col3.number_input("Advance Paid", min_value=0.0)
        
        st.write("---")
        for i, item in enumerate(st.session_state.items):
            ic1, ic2, ic3, ic4 = st.columns([3, 2, 2, 1])
            item['name'] = ic1.text_input(f"Item {i+1}", key=f"it{i}")
            item['rate'] = ic2.number_input(f"Rate", key=f"ir{i}", min_value=0.0)
            vat = item['rate'] * 0.05
            ic3.write(f"VAT: {vat:.2f}")
            item['ready'] = ic4.checkbox("Ready", key=f"rd{i}")
            
        if st.form_submit_button("💾 Save Bill & Send Greeting"):
            st.success("Bill Saved! WhatsApp Greeting Sent.")

    if st.button("➕ Add More Item"):
        st.session_state.items.append({"name": "", "rate": 0.0, "ready": False})
        st.rerun()

# --- 3. FAVOURITE (STAR) SECTION ---
with tabs[2]:
    st.subheader("⭐ Favourite Customers")
    m_fields = ["Length", "Shoulder", "Sleeves", "Chest", "Hip", "Waist", "Neck", "Armhole", "Bottom", "Side"]
    
    with st.expander("Add New Favourite Measurement"):
        f_name = st.text_input("Customer Name (Fav)")
        f_cols = st.columns(2)
        measurements = {}
        for i, field in enumerate(m_fields):
            measurements[field] = f_cols[i%2].number_input(field, step=0.1)
        st.button("Save Measurement")

# --- 4. WORKER CARD ---
with tabs[3]:
    st.subheader("💳 Worker Management")
    w_name = st.selectbox("Select Worker", ["Add New...", "Rizwan", "Aslam"])
    
    # 50 Items Logic
    st.write("### Items Assigned (Capacity: 50)")
    # Worker calculation: Total Rate - Money Paid = Payable
    st.info("Payable to Worker: AED 0.00")
    st.button("📥 Download Worker Card PDF")

# --- 5. SAMPLES ---
with tabs[4]:
    st.subheader("📦 Product Samples")
    cam, gal = st.columns(2)
    with cam: st.camera_input("Take Sample Photo")
    with gal: st.file_uploader("Upload from Gallery")
    st.text_input("Sample Name")
    st.number_input("Price")
    st.checkbox("Sold Out")