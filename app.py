import streamlit as st
import random
import datetime
import pandas as pd

st.set_page_config(page_title="Habib Bank Limited", page_icon="🏦", layout="centered")

# --- Initialize Session State ---
if 'balance' not in st.session_state:
    st.session_state.balance = 0
    st.session_state.name = ""
    st.session_state.account_no = random.randint(100000, 999999)
    st.session_state.history = []
    st.session_state.account_created = False

def add_history(action, amount):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append({
        "Date": time,
        "Action": action,
        "Amount": f"{amount} Rs",
        "Balance": f"{st.session_state.balance} Rs"
    })

# --- Header ---
st.title("🏦 Habib Bank Limited")
st.caption("Secure • Digital • Trusted Banking")

# --- Sidebar Menu ---
menu = st.sidebar.selectbox("Select Service", 
    ["Create Account", "Deposit Money", "Withdraw Money", "Fund Transfer", "Check Balance", "Transaction History", "Loan Calculator", "Account Details"])
st.sidebar.divider()
st.sidebar.info(f"**Customer:** {st.session_state.name if st.session_state.name else 'Guest'}\n\n**Account No:** {st.session_state.account_no}")

# 1. Create Account
if menu == "Create Account":
    st.header("Create New Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    account_type = st.selectbox("Account Type", ["Savings", "Current", "Business"])
    initial = st.number_input("Initial Deposit (Min 500 Rs)", min_value=500, value=1000, step=100)

    if st.button("Create Account", type="primary"):
        if name:
            st.session_state.name = name
            st.session_state.balance = initial
            st.session_state.account_created = True
            add_history("Account Created", initial)
            st.success(f"Congratulations {name}! Your account is created.")
            st.balloons()
            st.metric("Your Account Number", st.session_state.account_no)
        else:
            st.error("Please enter your full name.")

# 2. Deposit
elif menu == "Deposit Money":
    if not st.session_state.account_created:
        st.warning("Please create an account first.")
    else:
        st.header("Deposit Money")
        amount = st.number_input("Enter Amount to Deposit", min_value=1, step=100)
        if st.button("Deposit Now", type="primary"):
            st.session_state.balance += amount
            add_history("Deposit", amount)
            st.success(f"Successfully deposited {amount} Rs. New Balance: {st.session_state.balance} Rs")

# 3. Withdraw
elif menu == "Withdraw Money":
    if not st.session_state.account_created:
        st.warning("Please create an account first.")
    else:
        st.header("Withdraw Money")
        amount = st.number_input("Enter Amount to Withdraw", min_value=1, step=100)
        if st.button("Withdraw Now", type="primary"):
            if amount <= st.session_state.balance:
                st.session_state.balance -= amount
                add_history("Withdrawal", amount)
                st.success(f"Withdrawal successful. Remaining Balance: {st.session_state.balance} Rs")
            else:
                st.error(f"Insufficient Balance! Your balance is only {st.session_state.balance} Rs")

# 4. Fund Transfer
elif menu == "Fund Transfer":
    if not st.session_state.account_created:
        st.warning("Please create an account first.")
    else:
        st.header("Fund Transfer")
        to_account = st.text_input("Receiver Account Number")
        transfer_amount = st.number_input("Transfer Amount", min_value=1, step=100)
        if st.button("Transfer Money", type="primary"):
            if not to_account:
                st.error("Please enter receiver account number.")
            elif transfer_amount > st.session_state.balance:
                st.error("Insufficient Balance for transfer.")
            else:
                st.session_state.balance -= transfer_amount
                add_history(f"Transfer to {to_account}", transfer_amount)
                st.success(f"Successfully transferred {transfer_amount} Rs to {to_account}")

# 5. Check Balance
elif menu == "Check Balance":
    st.header("Account Balance")
    col1, col2 = st.columns(2)
    col1.metric("Account Number", st.session_state.account_no)
    col2.metric("Current Balance", f"{st.session_state.balance} Rs")
    st.info(f"Account Holder: {st.session_state.name if st.session_state.name else 'No Account Created Yet'}")

# 6. Transaction History
elif menu == "Transaction History":
    st.header("Transaction History")
    if not st.session_state.history:
        st.info("No transactions yet.")
    else:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
        st.download_button("Download Statement CSV", df.to_csv(index=False), "bank_statement.csv", "text/csv")

# 7. Loan Calculator
elif menu == "Loan Calculator":
    st.header("Loan Calculator")
    loan_amount = st.number_input("Loan Amount (Rs)", min_value=10000, value=100000, step=10000)
    interest = st.slider("Interest Rate %", 1, 20, 8)
    years = st.slider("Loan Tenure (Years)", 1, 20, 5)
    if st.button("Calculate EMI"):
        monthly_rate = interest / 12 / 100
        months = years * 12
        emi = (loan_amount * monthly_rate * (1+monthly_rate)**months) / ((1+monthly_rate)**months - 1) if monthly_rate > 0 else loan_amount/months
        st.success(f"Estimated Monthly EMI: {emi:.2f} Rs")
        st.metric("Total Payable", f"{emi*months:.2f} Rs")

# 8. Account Details
elif menu == "Account Details":
    st.header("Account Details")
    st.write(f"**Name:** {st.session_state.name}")
    st.write(f"**Account Number:** {st.session_state.account_no}")
    st.write(f"**Balance:** {st.session_state.balance} Rs")
    st.write(f"**Bank:** Habib Bank Limited")
    st.write(f"**Branch:** Karachi Main Branch")
    st.write(f"**Status:** {'Active' if st.session_state.account_created else 'Not Created'}")
