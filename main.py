import streamlit as st
from agents import render_agent_creation
from analytics import render_analytics

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "agent_creation"
if "agents" not in st.session_state:
    st.session_state.agents = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "customer_data" not in st.session_state:
    st.session_state.customer_data = None

# Page configuration
st.set_page_config(
    page_title="AI Agent Manager",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Agent Creation", "Chat Interface"]
    #["Agent Creation", "Chat Interface", "Analytics Dashboard"]
)

# Main content
st.title("AI Agent Management Platform")

if page == "Agent Creation":
    st.session_state.current_page = "agent_creation"
    render_agent_creation()
elif page == "Chat Interface":
    st.session_state.current_page = "chat"
    # Import chat module here to avoid circular imports
    from chat import render_chat_page
    render_chat_page()
else:
    st.session_state.current_page = "analytics"
    render_analytics()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made by VAM")