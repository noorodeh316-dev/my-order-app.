import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# إعدادات واجهة المستخدم (لتعود كما كانت في جهازك)
st.set_page_config(page_title="Order Management System Pro", layout="wide")

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.title("🚀 Navigation Menu")
    st.markdown("---")
    page = st.radio("Go to Stage:", [
        "1️⃣ Stage 1: Sales Entry", 
        "2️⃣ Stage 2: Coordination", 
        "3️⃣ Stage 3: Quality Control (QC)", 
        "4️⃣ Stage 4: Logistics",
        "📊 Final Reports"
    ])

# الاتصال بجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

if page == "1️⃣ Stage 1: Sales Entry":
    st.header("Order Management System Pro")
    
    with st.form("order_form"):
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
        
        submit_button = st.form_submit_button("Submit Order to Cloud")

        if submit_button:
            if sales_rep and company: # تأكد من ملء البيانات الأساسية
                # تجهيز البيانات الجديدة
                new_row = pd.DataFrame([{
                    "Sales Rep": sales_rep,
                    "Company": company,
                    "Contact": contact,
                    "Phone": phone,
                    "Email": email,
                    "Location": location,
                    "Payment": payment,
                    "Description": description
                }])
                
                try:
                    # قراءة البيانات القديمة أولاً
                    existing_data = conn.read(ttl=0)
                    # دمج البيانات الجديدة مع القديمة
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                    # تحديث الشيت
                    conn.update(data=updated_df)
                    st.success("✅ تم إرسال الطلب بنجاح وظهر في جدول البيانات!")
                except Exception as e:
                    st.error(f"خطأ في الصلاحيات: تأكدي أن ملف الجوجل شيت متاح 'Anyone with the link can EDIT'")
            else:
                st.warning("الرجاء إدخال اسم المندوب واسم الشركة على الأقل.")

else:
    st.info(f"Welcome to {page}. This section is being updated.")
