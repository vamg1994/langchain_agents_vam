import streamlit as st
from agents import render_agent_creation
from chat import render_chat_page
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Default AI News Agent template
default_ainews_agent = {
    "id": 0,
    "name": "ainews_agent",
    "type": "Research Agent",
    "prompt_template": """You are an advanced research agent powered by Perplexity AI, focused on gathering and analyzing information.
        Your responses should be in JSON format.

        Guidelines:
        - Conduct thorough research on given topics
        - Provide accurate and up-to-date information
        - Cite sources when possible
        - Synthesize information from multiple sources
        - Identify key insights and patterns

        Research context: {customer_context}
        Previous findings: {interaction_history}

        Respond in JSON format with:
        {
            "response": "Your research findings and analysis",
            "key_insights": ["List of main insights"],
            "sources": ["List of relevant sources"],
            "follow_up_areas": ["Suggested areas for further research"]
        }""",
    "parameters": {
        "research_topics": "artificial intelligence",
        "research_depth": 3,
        "source_requirements": ["News", "Academic"]
    }
}

# Travel Agent template
default_travel_agent = {
    "id": 1,
    "name": "travel_agent",
    "type": "Research Agent",
    "prompt_template": """You are an advanced travel research agent powered by Perplexity AI, specialized in finding and comparing travel options.
        Your responses should be in JSON format.

        Guidelines:
        - Search for current flight prices and schedules
        - Find and compare hotel accommodations
        - Research Airbnb options in the target location
        - Consider seasonal factors and local events
        - Provide price ranges and best deals
        - Include booking links when available
        - Consider travel restrictions and requirements
        -Include complete url links for all the information you provide for example: https://www.google.com/

        Travel context: {customer_context}
        Previous findings: {interaction_history}

        Respond in JSON format with:
        {
            "travel_summary": {
                "destination": "Specified destination",
                "dates": "Travel dates",
                "budget_range": "Estimated budget range"
            },
            "flights": {
                "options": ["List of flight options with prices"],
                "best_deals": ["Highlighted best value flights"],
                "airlines": ["Featured airlines"],
                "booking_links": ["List of booking links"]
            },
            "accommodations": {
                "hotels": {
                    "options": ["List of hotel options with prices"],
                    "recommended": ["Top hotel recommendations"],
                    "booking_links": ["List of booking links"]
                },
                "airbnb": {
                    "options": ["List of Airbnb options with prices"],
                    "recommended": ["Top Airbnb recommendations"],
                    "booking_links": ["List of booking links"]
                }
            },
            "additional_info": {
                "local_insights": ["Important local information"],
                "travel_tips": ["Useful travel tips"],
                "sources": ["Data sources and booking platforms"]
            },
            "follow_up_suggestions": ["Suggested next steps or additional research areas"]
        }""",
    "parameters": {
        "research_topics": "travel, flights, accommodations",
        "research_depth": 4,
        "source_requirements": ["Travel Sites", "News", "Local Guides"],
        "price_tracking": True,
        "location_focus": "global",
        "update_frequency": "daily"
    }
}

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "agent_creation"
if "agents" not in st.session_state:
    st.session_state.agents = [default_ainews_agent, default_travel_agent]  # Initialize with both default agents
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "customer_data" not in st.session_state:
    st.session_state.customer_data = None

# Page configuration
st.set_page_config(
    page_title="AI Agent Manager",
    page_icon="🦾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Agent Creation", "Chat Interface"]
)

# Main content
st.title("AI Agent Management Platform")

if page == "Agent Creation":
    st.session_state.current_page = "agent_creation"
    render_agent_creation()
elif page == "Chat Interface":
    st.session_state.current_page = "chat"
    render_chat_page()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made by VAM")