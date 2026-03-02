import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Order Management System Pro", layout="wide")

# القائمة الجانبية
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go to Stage:", ["1️⃣ Sales Entry", "📊 Reports"])

# الاتصال
conn = st.connection("gsheets", type=GSheetsConnection)

if page == "1️⃣ Sales Entry":
    st.header("Order Management System Pro")
    
    with st.form("full_order_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sales_rep = st.text_input("Sales Representative Name")
            company = st.text_input("Company Name")
            contact = st.text_input("Customer Contact Name")
            phone = st.text_input("Phone Number")
        
        with col2:
            # هدول هما الخانات اللي كنتِ بتدوري عليهم يا نورا
            email = st.text_input("Email Address")
            location = st.text_input("Customer Location")
            payment = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Credit Card"])
            st.file_uploader("Upload Attachments")

        description = st.text_area("Order Description & Special Requirements")
        
        submit = st.form_submit_button("Submit Order to Cloud")

        if submit:
            if sales_rep and company:
                try:
                    # الطريقة المضمونة: بنقرأ، بنضيف، وبنرجع نكتب
                    df = conn.read(ttl=0)
                    new_data = pd.DataFrame([{
                        "Sales Rep": sales_rep, "Company": company, "Contact": contact,
                        "Phone": phone, "Email": email, "Location": location,
                        "Payment": payment, "Description": description
                    }])
                    updated_df = pd.concat([df, new_data], ignore_index=True)
                    
                    # هاي الخطوة اللي كانت بتعلق معك
                    conn.update(data=updated_df)
                    st.success("✅ أخيراً! تم إرسال الطلب بنجاح بجميع الخانات.")
                except Exception as e:
                    st.error(f"تأكدي إن ملف جوجل شيت معمول Editor. الخطأ: {e}")
            else:
                st.warning("عبي البيانات الأساسية (المندوب والشركة).")
