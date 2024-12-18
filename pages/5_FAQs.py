# pages/5_FAQs.py
import streamlit as st

st.set_page_config(page_title="FAQs", layout="wide")

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] li:first-child {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Frequently Asked Questions")

faqs = {
    "What is the purpose of this platform?": 
        "This platform helps businesses analyze their financial health through various financial ratios and metrics.",
    
    "How often should I update my financial data?":
        "It's recommended to update your data monthly for accurate tracking and analysis.",
    
    "What do the different ratios mean?":
        "Each ratio provides insights into different aspects of your business - profitability, liquidity, efficiency, and solvency.",
    
    "How can I interpret the results?":
        "The platform provides visual representations and explanations for each metric to help you understand your financial position."
}

for question, answer in faqs.items():
    with st.expander(question):
        st.write(answer)

