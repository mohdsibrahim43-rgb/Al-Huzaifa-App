import streamlit as st
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. FIREBASE SETUP (AUTO-CONNECT) ---
# Ye check karta hai ki key file hai ya nahi
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase_key.json") 
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"⚠️ Error: 'firebase_key.json' file nahi mili! Usse GitHub par upload karein. Error: {e}")
        st.stop()

db = firestore.client()

# --- 2. CONFIGURATION ---
st.set_page_config(page_title="AL HUZAIFA DIGITAL", layout="wide")
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "email" not in st.session_state: st.session_state.email = ""
if "temp_items" not in st.session_state: st.session_state.temp_items = [{"name":"", "rate":0.0}]

# --- 3. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center; color:#1E8449;'>🔐 AL HUZAIFA CLOUD LOGIN</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        email = st.text_input("Apna Email ID Dalein")
        if st.button("Login & Connect Data", use_container_width=True):
            if email:
                st.session_state.email = email.lower().strip()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Email likhna zaroori hai.")
    st.stop()

# --- 4. MAIN APP ---
st.markdown(f"<h3 style='color:#1E8449;'>👤 User: {st.session_state.email}</h3>", unsafe_allow_html=True)
tabs = st.tabs(["🏠 Dashboard", "📝 New Bill", "📜 History"])

# --- TAB 1: DASHBOARD ---
with tabs[0]:
    # Cloud se data laana
    docs = db.collection('orders').where('email', '==', st.session_state.email).stream()
    my_data = [doc.to_dict() for doc in docs]
    
    total_rev = sum(d['total'] for d in my_data)
    st.metric("Total Income (AED)", f"{total_rev:,.2f}")
    st.metric("Total Bills", len(my_data))

# --- TAB 2: NEW BILL ---
with tabs[1]:
    st.subheader("Naya Bill Banayein")
    c1, c2 = st.columns(2)
    cust = c1.text_input("Customer Name")
    mobile = c2.text_input("Mobile No")
    
    # Add Items Logic
    for i, item in enumerate(st.session_state.temp_items):
        ic1, ic2 = st.columns([3, 1])
        item['name'] = ic1.text_input(f"Item {i+1}", key=f"n{i}", value=item['name'])
        item['rate'] = ic2.number_input(f"Rate", key=f"r{i}", value=item['rate'])
    
    if st.button("➕ Ek aur item jodein"):
        st.session_state.temp_items.append({"name":"", "rate":0.0})
        st.rerun()
        
    total = sum(i['rate'] for i in st.session_state.temp_items)
    st.info(f"Total Amount: AED {total}")

    if st.button("💾 SAVE TO CLOUD (Permanent)"):
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
            st.success("✅ Bill Cloud Par Save Ho Gaya!")
            st.session_state.temp_items = [{"name":"", "rate":0.0}] # Reset
        else:
            st.error("Customer ka naam likhein.")

# --- TAB 3: HISTORY ---
with tabs[2]:
    st.subheader("📜 Purane Bills")
    if my_data:
        df = pd.DataFrame(my_data)
        st.dataframe(df[['date', 'customer', 'total', 'mobile']], use_container_width=True)
    else:
        st.info("Abhi koi data nahi hai.")
