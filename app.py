import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. SYSTEM INITIALIZATION (DATABASE MEMORY) ---
# Ye ensure karta hai ki data tab tak rahe jab tak aap refresh na karein
if 'db_orders' not in st.session_state:
    st.session_state.db_orders = [] # Saare saved bills yahan rahenge
if 'db_workers' not in st.session_state:
    st.session_state.db_workers = ["Rizwan", "Aslam"] # Default workers
if 'db_customers' not in st.session_state:
    st.session_state.db_customers = [] # Fav customers
if 'temp_items' not in st.session_state:
    st.session_state.temp_items = [{"name": "", "rate": 0.0, "ready": False}] # Current bill ke items
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 2. THEME SETUP ---
st.set_page_config(page_title="AL HUZAIFA DIGITAL", layout="wide")
st.markdown("""
    <style>
    .main-title { color: #1E8449; font-weight: bold; font-size: 40px; text-align: center; margin-bottom: 0px; }
    .header-info { color: #27AE60; text-align: center; font-weight: bold; margin-bottom: 20px; }
    .metric-card { background-color: #f0fdf4; border: 1px solid #1E8449; padding: 15px; border-radius: 10px; text-align: center; }
    div[data-testid="stMetricValue"] { color: #1E8449; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<br><br><h2 style='text-align: center; color: #1E8449;'>🔐 AL HUZAIFA SECURE LOGIN</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        password = st.text_input("Enter Password", type="password")
        if st.button("Login", use_container_width=True):
            if password == "HUZAIFA2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect Password")
    st.stop()

# --- 4. SIDEBAR (DATA BACKUP) ---
with st.sidebar:
    st.header("💾 Data Backup")
    st.warning("Refresh karne se pehle data download zaroor karein!")
    
    if st.session_state.db_orders:
        df_backup = pd.DataFrame(st.session_state.db_orders)
        csv = df_backup.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Excel/CSV", data=csv, file_name="al_huzaifa_backup.csv", mime="text/csv")
    else:
        st.info("Abhi koi data nahi hai save karne ko.")

# --- 5. MAIN APP HEADER ---
st.markdown('<p class="main-title">AL HUZAIFA DIGITAL</p>', unsafe_allow_html=True)
st.markdown('<p class="header-info">Tailoring & Embroidery Management System<br>Sharjah, UAE | Mob: 0554999723</p>', unsafe_allow_html=True)

# --- 6. TABS LOGIC ---
tabs = st.tabs(["🏠 Dashboard", "📑 New Bill", "📜 Bill History", "💳 Workers", "⭐ Favourite", "📦 Samples"])

# ================= TAB 1: DASHBOARD =================
with tabs[0]:
    st.subheader("📊 Business Overview")
    
    # Live Calculations
    total_orders = len(st.session_state.db_orders)
    total_revenue = sum(order['grand_total'] for order in st.session_state.db_orders) if total_orders > 0 else 0
    pending_dlv = len([o for o in st.session_state.db_orders if not o['delivered']])
    
    # Metrics Display
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Orders", total_orders)
    m2.metric("Total Revenue", f"AED {total_revenue:,.2f}")
    m3.metric("Pending Delivery", pending_dlv)
    
    st.divider()
    
    # Urgent Orders Logic
    st.write("### 🚨 Urgent & Pending Deliveries")
    if total_orders > 0:
        df = pd.DataFrame(st.session_state.db_orders)
        # Show simple table
        st.dataframe(df[['bill_no', 'customer', 'delivery_date', 'status', 'balance']], use_container_width=True)
    else:
        st.info("No orders yet. Go to 'New Bill' tab to create one.")

# ================= TAB 2: NEW BILL (ENTRY) =================
with tabs[1]:
    st.subheader("📝 Create New Bill")
    
    with st.container(border=True):
        # Customer Details
        c1, c2, c3 = st.columns(3)
        bill_no = c1.text_input("Bill No.", value=f"100{len(st.session_state.db_orders)+1}")
        cust_name = c2.text_input("Customer Name")
        cust_mob = c3.text_input("Mobile No.")
        
        # Dates
        d1, d2, d3 = st.columns(3)
        ord_date = d1.date_input("Order Date", datetime.now())
        del_date = d2.date_input("Delivery Date", datetime.now() + timedelta(days=7))
        advance = d3.number_input("Advance Payment (AED)", min_value=0.0)
        
        st.markdown("---")
        st.write("### 👗 Add Items")
        
        # Dynamic Item List
        for i, item in enumerate(st.session_state.temp_items):
            ic1, ic2, ic3, ic4 = st.columns([3, 2, 2, 1])
            item['name'] = ic1.text_input(f"Item {i+1} Name", key=f"nm_{i}", value=item['name'])
            item['rate'] = ic2.number_input(f"Rate (AED)", key=f"rt_{i}", min_value=0.0, value=item['rate'])
            
            vat_amt = item['rate'] * 0.05
            ic3.write(f"VAT (5%): {vat_amt:.2f}")
            
            # Remove button logic (simplified)
            if ic4.button("❌", key=f"del_{i}"):
                st.session_state.temp_items.pop(i)
                st.rerun()

        # Add Item Button
        if st.button("➕ Add Another Item"):
            st.session_state.temp_items.append({"name": "", "rate": 0.0, "ready": False})
            st.rerun()
            
        st.markdown("---")
        
        # Final Calculations
        subtotal = sum(i['rate'] for i in st.session_state.temp_items)
        total_vat = subtotal * 0.05
        grand_total = subtotal + total_vat
        balance = grand_total - advance
        
        c_calc1, c_calc2 = st.columns(2)
        with c_calc1:
            st.info(f"Subtotal: {subtotal:.2f} | Total VAT: {total_vat:.2f}")
        with c_calc2:
            st.success(f"**GRAND TOTAL: AED {grand_total:.2f}**")
            st.error(f"**Balance Pending: AED {balance:.2f}**")
            
        # SAVE BUTTON
        if st.button("💾 SAVE BILL & PRINT", type="primary", use_container_width=True):
            if cust_name and st.session_state.temp_items:
                # Save to Database
                new_order = {
                    "bill_no": bill_no,
                    "customer": cust_name,
                    "mobile": cust_mob,
                    "order_date": str(ord_date),
                    "delivery_date": str(del_date),
                    "items": [i['name'] for i in st.session_state.temp_items],
                    "grand_total": grand_total,
                    "advance": advance,
                    "balance": balance,
                    "status": "In Progress",
                    "delivered": False
                }
                st.session_state.db_orders.append(new_order)
                
                # Reset Form
                st.session_state.temp_items = [{"name": "", "rate": 0.0, "ready": False}]
                st.toast("✅ Bill Saved Successfully!")
                st.success(f"Bill #{bill_no} saved! Check 'Bill History' tab.")
            else:
                st.error("Please enter Customer Name and at least one Item.")

# ================= TAB 3: BILL HISTORY =================
with tabs[2]:
    st.subheader("📜 All Saved Bills")
    if st.session_state.db_orders:
        df_history = pd.DataFrame(st.session_state.db_orders)
        st.dataframe(df_history, use_container_width=True)
        
        # Search functionality placeholder
        search = st.text_input("🔍 Search Bill by Name or No.")
        if search:
            st.write("Search results will appear here...")
    else:
        st.info("No bills saved yet.")

# ================= TAB 4: WORKER MANAGEMENT =================
with tabs[3]:
    st.subheader("💳 Karigar / Worker Management")
    
    # Add New Worker
    with st.expander("➕ Add New Worker"):
        new_worker = st.text_input("Worker Name")
        if st.button("Add Worker"):
            if new_worker:
                st.session_state.db_workers.append(new_worker)
                st.success(f"{new_worker} added!")
                st.rerun()

    # Assign Work
    w_col1, w_col2 = st.columns(2)
    with w_col1:
        worker_select = st.selectbox("Select Worker", st.session_state.db_workers)
        st.write(f"### Job Card: {worker_select}")
        st.info("No active jobs assigned yet.")
        
    with w_col2:
        st.write("### Actions")
        st.button("📲 Send WhatsApp Alert")
        st.button("📥 Download Job Card PDF")

# ================= TAB 5: FAVOURITE CUSTOMERS =================
with tabs[4]:
    st.subheader("⭐ Favourite Customers (Measurements)")
    # Simple form to add measurements
    with st.form("fav_form"):
        f_name = st.text_input("Customer Name")
        # 10 Measurement points
        m_cols = st.columns(5)
        m_fields = ["Length", "Shoulder", "Chest", "Waist", "Hip", "Sleeves", "Neck", "Armhole", "Cuff", "Bottom"]
        m_vals = {}
        for i, f in enumerate(m_fields):
            m_vals[f] = m_cols[i%5].number_input(f, step=0.1)
            
        if st.form_submit_button("Save Measurements"):
            st.session_state.db_customers.append({"name": f_name, **m_vals})
            st.success("Measurement Saved!")
            
    if st.session_state.db_customers:
        st.write("### Saved Measurements")
        st.dataframe(pd.DataFrame(st.session_state.db_customers))

# ================= TAB 6: SAMPLES =================
with tabs[5]:
    st.subheader("📦 Showroom Samples")
    c_cam, c_up = st.columns(2)
    with c_cam:
        st.camera_input("Take Photo")
    with c_up:
        st.file_uploader("Upload Image")
    st.button("Save Sample to Gallery")
