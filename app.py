import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Financial Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide "app" from sidebar
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] li:first-child {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Main content
st.title("Welcome to Financial Analytics Platform")

if 'user' not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.write("Please login to access all features")
    st.info("Use the Financial Dashboard to explore basic features or login for advanced analytics")
else:
    st.write(f"Welcome back, {st.session_state.user['username']}!")
    st.write("Use the sidebar to navigate through different modules:")
    
    # Display available modules
    st.markdown("""
    - **Financial Dashboard**: Basic financial metrics and ratios
    - **Advanced Financial Dashboard**: Historical data analysis and trends
    - **Admin Dashboard**: User and data management (Admin only)
    - **Tutorial**: Learn how to use the platform
    - **FAQs**: Common questions and answers
    - **Financial Guide**: Detailed explanations of financial metrics
    """)

# Footer
st.markdown("---")
st.markdown("### Getting Started")
st.write("Select a module from the sidebar to begin your financial analysis journey.")
