import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. FIREBASE CONNECTION (One Time Setup) ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase_key.json") 
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"⚠️ Firebase Key Error: {e}. Make sure json file is uploaded.")
        st.stop()

db = firestore.client()

# --- 2. CONFIGURATION & THEME ---
st.set_page_config(page_title="AL HUZAIFA CLOUD", layout="wide")

# Session State Variables
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "email" not in st.session_state: st.session_state.email = ""
if "temp_items" not in st.session_state: st.session_state.temp_items = [{"name":"", "rate":0.0}]

# --- 3. CUSTOM CSS (Green Theme) ---
st.markdown("""
    <style>
    .main-title { color: #1E8449; font-weight: bold; font-size: 40px; text-align: center; }
    .header-info { color: #27AE60; text-align: center; font-weight: bold; margin-bottom: 20px; }
    div[data-testid="stMetricValue"] { color: #1E8449; }
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid #1E8449; }
    .stButton>button { background-color: #1E8449; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<br><h2 style='text-align:center; color:#1E8449;'>🔐 AL HUZAIFA LOGIN</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        email_input = st.text_input("Enter Email ID")
        if st.button("Login"):
            if email_input:
                st.session_state.email = email_input.lower().strip()
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 5. MAIN APP UI ---
st.markdown('<p class="main-title">AL HUZAIFA DIGITAL</p>', unsafe_allow_html=True)
st.markdown(f"<p class='header-info'>User: {st.session_state.email} | Tailoring & Embroidery</p>", unsafe_allow_html=True)

# Tabs Wapas aa gaye
tabs = st.tabs(["🏠 Dashboard", "📝 New Bill", "📜 History", "💳 Workers", "📦 Samples"])

# === TAB 1: DASHBOARD ===
with tabs[0]:
    st.subheader("📊 Business Overview")
    if st.button("🔄 Refresh Data"):
        st.rerun()
        
    # Fetch Data
    try:
        docs = db.collection('orders').where('email', '==', st.session_state.email).stream()
        orders = [doc.to_dict() for doc in docs]
        
        total_rev = sum(d.get('total', 0) for d in orders)
        count = len(orders)
        
        m1, m2 = st.columns(2)
        m1.metric("Total Income", f"AED {total_rev:,.2f}")
        m2.metric("Total Orders", count)
    except Exception as e:
        st.error(f"Data loading error: {e}")

# === TAB 2: NEW BILL ===
with tabs[1]:
    st.subheader("📝 Create New Bill")
    c1, c2, c3 = st.columns(3)
    cust_name = c1.text_input("Customer Name")
    mobile = c2.text_input("Mobile No")
    b_date = c3.date_input("Order Date", datetime.now())

    st.write("---")
    # Dynamic Items Logic
    for i, item in enumerate(st.session_state.temp_items):
        ic1, ic2 = st.columns([3, 1])
        item['name'] = ic1.text_input(f"Item {i+1}", key=f"nm_{i}", value=item['name'])
        item['rate'] = ic2.number_input(f"Rate", key=f"rt_{i}", value=item['rate'])
    
    if st.button("➕ Add Item"):
        st.session_state.temp_items.append({"name":"", "rate":0.0})
        st.rerun()
    
    total_bill = sum(item['rate'] for item in st.session_state.temp_items)
    st.metric("Total Amount (AED)", f"{total_bill:,.2f}")

    if st.button("💾 SAVE BILL (Cloud)", type="primary"):
        if cust_name:
            try:
                order_data = {
                    "email": st.session_state.email,
                    "customer": cust_name,
                    "mobile": mobile,
                    "date": str(b_date),
                    "items": st.session_state.temp_items,
                    "total": total_bill,
                    "created_at": firestore.SERVER_TIMESTAMP
                }
                # Firestore Save
                db.collection('orders').add(order_data)
                
                st.success(f"✅ Bill for {cust_name} saved successfully!")
                st.session_state.temp_items = [{"name":"", "rate":0.0}] # Reset
            except Exception as e:
                st.error(f"Error saving bill: {e}")
        else:
            st.error("Customer Name is required!")

# === TAB 3: HISTORY ===
with tabs[2]:
    st.subheader("📜 Order History")
    if st.button("📂 Load History"):
        docs = db.collection('orders').where('email', '==', st.session_state.email).order_by('date', direction=firestore.Query.DESCENDING).stream()
        data = [doc.to_dict() for doc in docs]
        
        if data:
            df = pd.DataFrame(data)
            # Formatting for display
            display_df = df[['date', 'customer', 'mobile', 'total']]
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No orders found.")

# === TAB 4: WORKERS ===
with tabs[3]:
    st.subheader("💳 Worker Management")
    w_name = st.text_input("Add New Worker")
    if st.button("Save Worker"):
        if w_name:
            db.collection('workers').add({"email": st.session_state.email, "name": w_name})
            st.success("Worker Added!")
            
    st.write("### Active Workers")
    # Fetch Workers
    w_docs = db.collection('workers').where('email', '==', st.session_state.email).stream()
    workers = [w.to_dict()['name'] for w in w_docs]
    st.write(workers if workers else "No workers added yet.")

# === TAB 5: SAMPLES ===
with tabs[4]:
    st.subheader("📦 Product Samples")
    # Placeholder for future image upload logic (requires Storage bucket setup)
    st.info("Sample Photo Upload requires Firebase Storage setup. Coming in next update.")
    st.camera_input("Take Photo (Demo)")
