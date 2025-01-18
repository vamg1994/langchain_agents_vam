import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def generate_sample_metrics():
    """Generate sample metrics for demonstration"""
    return {
        "sales_agents": {
            "conversations": 150,
            "successful_sales": 45,
            "conversion_rate": 0.30,
            "average_sale_value": 250.0
        },
        "churn_prevention": {
            "at_risk_customers": 75,
            "retained_customers": 52,
            "retention_rate": 0.69,
            "average_customer_value": 1200.0
        }
    }

def create_performance_chart(metrics, agent_type):
    """Create performance visualization based on agent type"""
    if agent_type == "sales":
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=metrics["sales_agents"]["conversion_rate"] * 100,
            title={'text': "Sales Conversion Rate (%)"},
            gauge={'axis': {'range': [0, 100]},
                  'steps': [
                      {'range': [0, 30], 'color': "lightgray"},
                      {'range': [30, 70], 'color': "gray"},
                      {'range': [70, 100], 'color': "darkgray"}],
                  'threshold': {
                      'line': {'color': "red", 'width': 4},
                      'thickness': 0.75,
                      'value': 85}}))
    else:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=metrics["churn_prevention"]["retention_rate"] * 100,
            title={'text': "Customer Retention Rate (%)"},
            gauge={'axis': {'range': [0, 100]},
                  'steps': [
                      {'range': [0, 30], 'color': "lightgray"},
                      {'range': [30, 70], 'color': "gray"},
                      {'range': [70, 100], 'color': "darkgray"}],
                  'threshold': {
                      'line': {'color': "red", 'width': 4},
                      'thickness': 0.75,
                      'value': 85}}))
    return fig

def render_analytics():
    st.header("Analytics Dashboard")

    # Get metrics
    metrics = generate_sample_metrics()

    # Dashboard layout
    col1, col2 = st.columns(2)

    # Sales Agent Metrics
    with col1:
        st.subheader("Sales Agent Performance")
        st.metric(
            label="Total Conversations",
            value=metrics["sales_agents"]["conversations"]
        )
        st.metric(
            label="Successful Sales",
            value=metrics["sales_agents"]["successful_sales"]
        )
        st.metric(
            label="Average Sale Value",
            value=f"${metrics['sales_agents']['average_sale_value']:.2f}"
        )

        # Sales performance chart
        st.plotly_chart(
            create_performance_chart(metrics, "sales"),
            use_container_width=True
        )

    # Churn Prevention Metrics
    with col2:
        st.subheader("Churn Prevention Performance")
        st.metric(
            label="At-Risk Customers",
            value=metrics["churn_prevention"]["at_risk_customers"]
        )
        st.metric(
            label="Retained Customers",
            value=metrics["churn_prevention"]["retained_customers"]
        )
        st.metric(
            label="Average Customer Value",
            value=f"${metrics['churn_prevention']['average_customer_value']:.2f}"
        )

        # Retention performance chart
        st.plotly_chart(
            create_performance_chart(metrics, "churn"),
            use_container_width=True
        )

    # Historical Performance
    st.subheader("Historical Performance")

    # Generate sample historical data
    dates = pd.date_range(
        start=(datetime.now() - timedelta(days=30)),
        end=datetime.now(),
        freq='D'
    )

    historical_data = pd.DataFrame({
        'Date': dates,
        'Sales Conversion Rate': np.random.random(len(dates)) * 100,
        'Customer Retention Rate': np.random.random(len(dates)) * 100
    })

    # Plot historical performance
    fig = px.line(
        historical_data,
        x='Date',
        y=['Sales Conversion Rate', 'Customer Retention Rate'],
        title='30-Day Performance Trends'
    )
    st.plotly_chart(fig, use_container_width=True)