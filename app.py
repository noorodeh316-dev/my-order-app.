import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Order Management System Pro", layout="wide")

# القائمة الجانبية
with st.sidebar:
    st.title("🚀 Navigation Menu")
    page = st.radio("Go to Stage:", ["1️⃣ Stage 1: Sales Entry", "📊 Final Reports"])

conn = st.connection("gsheets", type=GSheetsConnection)

if page == "1️⃣ Stage 1: Sales Entry":
    st.header("Order Management System Pro")
    
    with st.form("order_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sales_rep = st.text_input("Sales Representative Name")
            company = st.text_input("Company Name")
        with col2:
            contact = st.text_input("Customer Contact Name")
            phone = st.text_input("Phone Number")
        
        description = st.text_area("Order Description")
        submit = st.form_submit_button("Submit Order to Cloud")

        if submit:
            if sales_rep and company:
                try:
                    # قراءة البيانات الحالية
                    df = conn.read(ttl=0)
                    # إضافة السطر الجديد
                    new_row = pd.DataFrame([{
                        "Sales Rep": sales_rep,
                        "Company": company,
                        "Contact": contact,
                        "Phone": phone,
                        "Description": description
                    }])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    # تحديث الجدول
                    conn.update(data=updated_df)
                    st.success("✅ تم تسجيل الطلب بنجاح في السحابة!")
                except Exception as e:
                    st.error(f"تأكدي من إعداد ملف جوجل كـ Editor. الخطأ: {e}")
            else:
                st.warning("الرجاء ملء البيانات الأساسية.")
