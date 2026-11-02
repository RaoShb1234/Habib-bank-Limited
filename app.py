import streamlit as st
import random
st.set_page_config(page_title="Habib Bank Limited", page_icon="🏦")
if 'balance' not in st.session_state:
    st.session_state.balance = 0
    st.session_state.name = ""
    st.session_state.account_no = random.randint(100000,999999)
    st.session_state.history = []
st.title("🏦 Habib Bank Limited")
menu = st.sidebar.selectbox("Menu", ["Account Banao","Paise Jama Karo","Paise Nikalo","Balance Dekho"])
if menu == "Account Banao":
    name = st.text_input("Naam likho")
    initial = st.number_input("Pehli raqam", value=500)
    if st.button("Account Bana Do"):
        st.session_state.name=name
        st.session_state.balance=initial
        st.session_state.history.append(f"Account bana - {initial} Rs")
        st.success(f"Mubarak ho {name}! Account No: {st.session_state.account_no}")
        st.balloons()
elif menu == "Paise Jama Karo":
    amount = st.number_input("Kitne jama?", min_value=1)
    if st.button("Jama Karo"):
        st.session_state.balance+=amount
        st.success(f"{amount} Rs jama! Balance: {st.session_state.balance}")
elif menu == "Paise Nikalo":
    amount = st.number_input("Kitne nikalne?", min_value=1)
    if st.button("Nikalo"):
        if amount <= st.session_state.balance:
            st.session_state.balance-=amount
            st.success(f"Balance bacha: {st.session_state.balance}")
        else:
            st.error("Paise kam hain! 😂")
elif menu == "Balance Dekho":
    st.metric("Account No", st.session_state.account_no)
    st.metric("Balance", f"{st.session_state.balance} Rs")
