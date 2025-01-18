import streamlit as st
from datetime import datetime
import json

def format_chat_message(message, timestamp=None):
    """Format chat messages for display"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "content": message,
        "timestamp": timestamp
    }

def load_agent_template(agent_type):
    """Load predefined agent templates"""
    templates = {
        "sales": {
            "name": "Sales Agent",
            "description": "Specialized in product recommendations and upselling",
            "prompt_template": """You are a skilled sales agent. Your goal is to help customers 
            find the best products while maximizing sales opportunities. 
            
            Current customer context: {customer_context}
            Previous interaction history: {interaction_history}
            
            Provide personalized recommendations and identify upselling opportunities.
            Response should be professional and helpful."""
        },
        "churn": {
            "name": "Churn Prevention Agent",
            "description": "Specialized in identifying and preventing customer churn",
            "prompt_template": """You are a customer retention specialist. Your goal is to identify 
            signs of potential churn and provide solutions to retain customers.
            
            Customer status: {customer_context}
            Interaction history: {interaction_history}
            
            Analyze the situation and suggest retention strategies."""
        }
    }
    return templates.get(agent_type, None)

def validate_agent_config(config):
    """Validate agent configuration"""
    required_fields = ["name", "type", "prompt_template"]
    return all(field in config for field in required_fields)

def generate_agent_id():
    """Generate unique agent ID"""
    return f"agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def save_chat_history(messages, agent_id):
    """Save chat history to session state"""
    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = {}
    
    st.session_state.chat_histories[agent_id] = messages

def load_chat_history(agent_id):
    """Load chat history from session state"""
    if "chat_histories" not in st.session_state:
        return []
    
    return st.session_state.chat_histories.get(agent_id, [])
