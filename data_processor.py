import streamlit as st
import pandas as pd
from io import StringIO
import json
from vector_store import VectorStore

# Initialize vector store in session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()

def process_customer_data(uploaded_file):
    """Process uploaded customer data file"""
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)

        # Basic validation
        required_columns = ['customer_id', 'interaction_history', 'purchase_history']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"

        # Process and structure the data
        processed_data = []
        for _, row in df.iterrows():
            customer_data = {
                "customer_id": row["customer_id"],
                "interaction_history": json.loads(row["interaction_history"]) 
                    if isinstance(row["interaction_history"], str) else row["interaction_history"],
                "purchase_history": json.loads(row["purchase_history"]) 
                    if isinstance(row["purchase_history"], str) else row["purchase_history"]
            }
            processed_data.append(customer_data)

        # Add to vector store
        st.session_state.vector_store.add_customers(processed_data)
        st.session_state.customer_data = processed_data

        return True, processed_data

    except Exception as e:
        return False, f"Error processing file: {str(e)}"

def render_data_upload():
    """Render data upload interface"""
    st.subheader("Upload Customer Data")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file containing customer data"
    )

    if uploaded_file is not None:
        # Process the uploaded file
        success, result = process_customer_data(uploaded_file)

        if success:
            st.success("Data uploaded and processed successfully!")

            # Display data preview
            st.subheader("Data Preview")
            df = pd.DataFrame(result)
            st.dataframe(df.head())

            # Display basic statistics
            st.subheader("Data Statistics")
            st.write(f"Total customers: {len(result)}")

            # Show similar customer patterns
            if len(result) > 0:
                st.subheader("Customer Similarity Analysis")
                sample_customer = result[0]
                similar_customers = st.session_state.vector_store.search_similar_customers(
                    st.session_state.vector_store._create_text_representation(sample_customer)
                )
                st.write("Similar customer patterns found:", len(similar_customers))

        else:
            st.error(f"Error: {result}")

def get_customer_data(customer_id):
    """Retrieve customer data by ID with context"""
    if not customer_id or st.session_state.customer_data is None:
        return None

    return st.session_state.vector_store.get_customer_context(customer_id)