import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الصفحة
st.set_page_config(page_title="Order Management System", layout="wide")

# القائمة الجانبية
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go to:", ["1️⃣ Sales Entry", "📊 Reports"])

# الاتصال بالجوجل شيت
conn = st.connection("gsheets", type=GSheetsConnection)

if page == "1️⃣ Sales Entry":
    st.header("Order Management System Pro")
    
    with st.form("main_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sales_rep = st.text_input("Sales Representative Name")
            company = st.text_input("Company Name")
            contact = st.text_input("Customer Contact Name")
            phone = st.text_input("Phone Number")
        with col2:
            email = st.text_input("Email Address")
            location = st.text_input("Customer Location")
            payment = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Credit Card"])
            st.file_uploader("Upload Attachments")
            
        description = st.text_area("Order Description & Special Requirements")
        
        # زر الإرسال
        submit = st.form_submit_button("Submit Order to Cloud")

        if submit:
            if sales_rep and company:
                # تجهيز البيانات
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
                    # هذه هي الطريقة السحرية: نقرأ ثم ندمج ثم نحدث
                    existing_data = conn.read(ttl=0)
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                    
                    # ملاحظة: إذا ظهر خطأ الصلاحيات هنا، سنستخدم طريقة الرابط المباشر
                    conn.update(data=updated_df)
                    st.success("✅ مبروك! تم إرسال الطلب بنجاح.")
                except Exception as e:
                    st.error("عذراً، جوجل ما زال يرفض التعديل. تأكدي من ضبط الملف كـ Editor.")
            else:
                st.warning("الرجاء إدخال البيانات الأساسية.")
