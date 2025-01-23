import streamlit as st
from langchain_community.chat_models import ChatOpenAI, ChatPerplexity
from langchain_core.prompts import PromptTemplate
import json

def create_sales_agent_template():
    return {
        "name": "Sales Agent",
        "description": "Specialized in product recommendations and upselling",
        "prompt_template": """You are a skilled sales agent focused on providing personalized recommendations 
        and identifying upselling opportunities. Your responses should be in JSON format.

        Guidelines:
        - Analyze customer purchase history and preferences
        - Suggest relevant products or upgrades
        - Provide clear value propositions
        - Be professional and helpful
        - Include personalized recommendations

        Current customer context: {customer_context}
        Previous interaction history: {interaction_history}

        Respond in JSON format with:
        {
            "response": "Your customer-facing message",
            "analysis": "Internal analysis of customer behavior",
            "recommendations": ["List of recommended products/services"],
            "upsell_opportunities": ["Identified upselling opportunities"]
        }"""
    }

def create_churn_prevention_template():
    return {
        "name": "Churn Prevention Agent",
        "description": "Specialized in identifying and preventing customer churn",
        "prompt_template": """You are a customer retention specialist focused on identifying churn risks 
        and providing retention strategies. Your responses should be in JSON format.

        Guidelines:
        - Analyze customer engagement patterns
        - Identify potential churn indicators
        - Suggest personalized retention strategies
        - Address customer concerns proactively
        - Recommend relevant loyalty programs or incentives

        Customer status: {customer_context}
        Interaction history: {interaction_history}

        Respond in JSON format with:
        {
            "response": "Your customer-facing message",
            "churn_risk_analysis": "Internal analysis of churn risk factors",
            "retention_strategies": ["List of recommended retention strategies"],
            "engagement_suggestions": ["Suggested ways to increase engagement"]
        }"""
    }

def create_research_agent_template():
    return {
        "name": "Research Agent",
        "description": "Specialized in research and information gathering",
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
        }"""
    }

def render_agent_creation():
    st.header("Create New AI Agent")

    # Agent type selection
    agent_type = st.selectbox(
        "Select Agent Type",
        ["Sales Agent", "Churn Prevention Agent", "Research Agent"]
    )

    # Agent configuration form
    with st.form("agent_creation_form"):
        agent_name = st.text_input("Agent Name")

        # Custom parameters based on agent type
        if agent_type == "Research Agent":
            research_topics = st.text_area(
                "Research Topics",
                help="Enter key topics or areas of focus"
            )
            research_depth = st.slider(
                "Research Depth",
                min_value=1,
                max_value=5,
                value=3,
                help="1: Basic overview, 5: Deep analysis"
            )
            source_requirements = st.multiselect(
                "Source Requirements",
                ["Academic", "News", "Industry Reports", "Social Media", "Patents"]
            )
            template = create_research_agent_template()
        elif agent_type == "Sales Agent":
            product_knowledge = st.text_area(
                "Product Knowledge Base",
                help="Enter key product information and selling points"
            )
            sales_strategies = st.multiselect(
                "Sales Strategies",
                ["Cross-selling", "Upselling", "Bundle Offers", "Seasonal Promotions"]
            )
            template = create_sales_agent_template()
        else:  # Churn Prevention Agent
            churn_indicators = st.text_area(
                "Churn Indicators",
                help="Enter key indicators that suggest potential churn"
            )
            retention_strategies = st.multiselect(
                "Retention Strategies",
                ["Special Offers", "Premium Support", "Product Education", "Loyalty Programs"]
            )
            template = create_churn_prevention_template()

        # Custom prompt template
        prompt_template = st.text_area(
            "Custom Prompt Template",
            value=template["prompt_template"],
            height=200
        )

        submitted = st.form_submit_button("Create Agent")

        if submitted and agent_name:
            # Initialize parameters based on agent type
            parameters = {}
            if agent_type == "Research Agent":
                parameters = {
                    "research_topics": research_topics,
                    "research_depth": research_depth,
                    "source_requirements": source_requirements,
                }
            elif agent_type == "Sales Agent":
                parameters = {
                    "product_knowledge": product_knowledge,
                    "sales_strategies": sales_strategies,
                }
            else:  # Churn Prevention Agent
                parameters = {
                    "churn_indicators": churn_indicators,
                    "retention_strategies": retention_strategies,
                }

            new_agent = {
                "id": len(st.session_state.agents),
                "name": agent_name,
                "type": agent_type,
                "prompt_template": prompt_template,
                "parameters": parameters
            }

            st.session_state.agents.append(new_agent)
            st.success(f"Agent '{agent_name}' created successfully!")

    # Display existing agents
    if st.session_state.agents:
        st.subheader("Existing Agents")
        for agent in st.session_state.agents:
            with st.expander(f"{agent['name']} ({agent['type']})"):
                st.json(agent)