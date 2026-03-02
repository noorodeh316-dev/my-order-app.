import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# إعدادات الصفحة لتظهر بشكل احترافي
st.set_page_config(page_title="Order Management System Pro", layout="wide")

st.title("🚀 Navigation Menu")

# القائمة الجانبية (Sidebar) للتنقل بين المراحل
st.sidebar.title("Go to Stage:")
page = st.sidebar.radio("Stages", [
    "1️⃣ Stage 1: Sales Entry", 
    "2️⃣ Stage 2: Coordination", 
    "3️⃣ Stage 3: Quality Control (QC)", 
    "4️⃣ Stage 4: Logistics",
    "📊 Final Reports"
])

# الربط مع جوجل شيت (مع دعم التحديث الفوري)
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

if page == "1️⃣ Stage 1: Sales Entry":
    st.header("Order Details")
    
    col1, col2 = st.columns(2)
    with col1:
        sales_rep = st.text_input("Sales Representative Name")
        company = st.text_input("Company Name")
        contact = st.text_input("Customer Contact Name")
        phone = st.text_input("Phone Number")
    
    with col2:
        email = st.text_input("Email Address")
        location = st.text_input("Customer Location (Link or Address)")
        payment = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Credit Card"])
        upload = st.file_uploader("Upload Attachments (LPO, License, etc.)")

    description = st.text_area("Order Description & Special Requirements")

    if st.button("Submit Order to Cloud"):
        # قراءة البيانات مع دعم Unicode (لتجنب خطأ اللغة العربية)
        try:
            new_data = pd.DataFrame([{
                "Sales Rep": sales_rep,
                "Company": company,
                "Contact": contact,
                "Phone": phone,
                "Description": description
            }])
            
            # تحديث البيانات في الشيت
            conn.create(spreadsheet=url, data=new_data)
            st.success("✅ Order Submitted Successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.info(f"Welcome to {page}. This section is being updated.")
