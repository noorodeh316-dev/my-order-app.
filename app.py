import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- Page Config ---
st.set_page_config(page_title="Global Order System", layout="wide")

# --- Connect to Google Sheets ---
# ملاحظة: سنضع الرابط في إعدادات الموقع لاحقاً، حالياً سنستخدمه للاختبار
url = "ضع_رابط_جوجل_شيت_هنا" # استبدل هذا بـ Copy Link الذي أخذته من جوجل

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🚀 Global Order Management System")
st.info("Connected to Google Cloud Database")

# --- Stage 1: Sales Entry Form ---
with st.form("main_form"):
    col1, col2 = st.columns(2)
    with col1:
        salesman = st.text_input("Salesman Name")
        company = st.text_input("Company Name")
    with col2:
        customer = st.text_input("Customer Name")
        payment = st.selectbox("Payment", ["Cash", "Credit", "Bank Transfer"])
    
    desc = st.text_area("Order Description")
    
    if st.form_submit_button("Submit Order to Cloud"):
        if salesman and company:
            # هنا الكود الذي يرسل البيانات لجوجل شيت
            new_data = pd.DataFrame([{
                "Salesman": salesman,
                "Company": company,
                "Customer": customer,
                "Payment": payment,
                "Description": desc,
                "Status": "Pending"
            }])
            # تحديث الشيت
            existing_data = conn.read(spreadsheet=url)
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(spreadsheet=url, data=updated_df)
            st.success("✅ Order Synced to Google Sheets!")
        else:
            st.error("Please fill required fields")