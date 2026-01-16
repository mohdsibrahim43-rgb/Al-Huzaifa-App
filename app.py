import streamlit as st
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. FIREBASE SETUP ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase_key.json") 
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"⚠️ Error: Key file missing. {e}")
        st.stop()

db = firestore.client()

# --- 2. CONFIG ---
st.set_page_config(page_title="AL HUZAIFA CLOUD", layout="wide")
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "email" not in st.session_state: st.session_state.email = ""
if "temp_items" not in st.session_state: st.session_state.temp_items = [{"name":"", "rate":0.0}]

# --- 3. CSS STYLING ---
st.markdown("""
    <style>
    .main-title { color: #1E8449; font-weight: bold; font-size: 35px; text-align: center; }
    .stButton>button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<br><h2 style='text-align:center; color:#1E8449;'>🔐 AL HUZAIFA LOGIN</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        email = st.text_input("Apna Email ID Dalein")
        if st.button("Login"):
            if email:
                st.session_state.email = email.lower().strip()
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# --- 5. MAIN APP ---
st.markdown(f"<p class='main-title'>AL HUZAIFA DIGITAL</p>", unsafe_allow_html=True)
st.success(f"👤 User: {st.session_state.email}")

tabs = st.tabs(["🏠 Dashboard", "📝 New Bill", "📜 History"])

# --- TAB 1: DASHBOARD (Updated to prevent stuck) ---
with tabs[0]:
    st.subheader("📊 Business Overview")
    st.info("Agar data nahi dikh raha, to 'Refresh' dabayein.")
    
    # Data tabhi layenge jab button dabega (To prevent hanging)
    if st.button("🔄 Load Dashboard Data"):
        try:
            docs = db.collection('orders').where('email', '==', st.session_state.email).stream()
            my_data = [doc.to_dict() for doc in docs]
            
            if my_data:
                total_rev = sum(d['total'] for d in my_data)
                c1, c2 = st.columns(2)
                c1.metric("Total Income", f"AED {total_rev:,.2f}")
                c2.metric("Total Orders", len(my_data))
            else:
                st.warning("Abhi koi data nahi hai. 'New Bill' tab mein jakar pehla bill banayein!")
        except Exception as e:
            st.error(f"Connection Error: {e}")

# --- TAB 2: NEW BILL ---
with tabs[1]:
    st.subheader("📝 Naya Bill Banayein")
    c1, c2 = st.columns(2)
    cust = c1.text_input("Customer Name")
    mobile = c2.text_input("Mobile No")
    
    for i, item in enumerate(st.session_state.temp_items):
        ic1, ic2 = st.columns([3, 1])
        item['name'] = ic1.text_input(f"Item {i+1}", key=f"n{i}", value=item['name'])
        item['rate'] = ic2.number_input(f"Rate", key=f"r{i}", value=item['rate'])
    
    if st.button("➕ Ek aur item"):
        st.session_state.temp_items.append({"name":"", "rate":0.0})
        st.rerun()
        
    total = sum(i['rate'] for i in st.session_state.temp_items)
    st.metric("Total Bill Amount", f"AED {total}")

    if st.button("💾 SAVE BILL (Cloud)", type="primary"):
        if cust:
            order = {
                "email": st.session_state.email,
                "customer": cust,
                "mobile": mobile,
                "items": st.session_state.temp_items,
                "total": total,
                "date": str(datetime.now())
            }
            db.collection('orders').add(order)
            st.success("✅ Bill Save Ho Gaya!")
            st.session_state.temp_items = [{"name":"", "rate":0.0}]
        else:
            st.error("Customer Name zaroori hai.")

# --- TAB 3: HISTORY ---
with tabs[2]:
    st.subheader("📜 Bill History")
    if st.button("📂 Show History"):
        docs = db.collection('orders').where('email', '==', st.session_state.email).stream()
        history_data = [doc.to_dict() for doc in docs]
        if history_data:
            df = pd.DataFrame(history_data)
            st.dataframe(df[['date', 'customer', 'total']])
        else:
            st.write("No records found.")
