import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
from data_processor import get_customer_data, render_data_upload

def render_chat_page():
    """Render the chat interface page"""
    st.header("Chat Interface")

    # Data Upload Section
    with st.expander("Upload Customer Data"):
        render_data_upload()

    # Agent selection
    if not st.session_state.agents:
        st.warning("Please create an agent first in the Agent Creation section.")
        return

    selected_agent = st.selectbox(
        "Select Agent",
        options=st.session_state.agents,
        format_func=lambda x: f"{x['name']} ({x['type']})"
    )

    # Customer Context
    customer_id = st.text_input("Enter Customer ID", help="Enter the ID of the customer you want to analyze")
    customer_data = get_customer_data(customer_id) if customer_id else None

    if customer_id and not customer_data:
        st.warning("Customer not found. Please check the ID or upload customer data.")

    # Initialize chat model
    # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
    chat_model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        response_format={"type": "json_object"}
    )

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                try:
                    # Parse JSON response for better formatting
                    content = json.loads(message["content"])
                    st.markdown(content.get("response", message["content"]))
                except json.JSONDecodeError:
                    st.markdown(message["content"])
            else:
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Enter your message"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Prepare context for the agent
                context = {
                    "agent_type": selected_agent["type"],
                    "parameters": selected_agent["parameters"],
                    "customer_data": customer_data
                }

                # Generate response using the agent's prompt template
                messages = [
                    SystemMessage(content=selected_agent["prompt_template"]),
                    HumanMessage(content=json.dumps({
                        "user_message": prompt,
                        "context": context
                    }))
                ]

                response = chat_model.invoke(messages)

                try:
                    # Ensure response is properly formatted JSON
                    response_content = json.loads(response.content)
                    if isinstance(response_content, str):
                        response_content = {"response": response_content}
                except json.JSONDecodeError:
                    response_content = {"response": response.content}

                # Display response
                st.markdown(response_content.get("response", response.content))
                st.session_state.messages.append(
                    {"role": "assistant", "content": json.dumps(response_content)}
                )

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()