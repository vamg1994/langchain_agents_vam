import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json
from typing import List, Dict, Any

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Output dimension of all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.dimension)
        self.stored_data = []

    def _create_text_representation(self, customer_data: Dict[str, Any]) -> str:
        """Create a textual representation of customer data for embedding"""
        return (
            f"Customer ID: {customer_data['customer_id']} "
            f"Interaction History: {json.dumps(customer_data['interaction_history'])} "
            f"Purchase History: {json.dumps(customer_data['purchase_history'])}"
        )

    def add_customers(self, customers: List[Dict[str, Any]]) -> None:
        """Add customer data to the vector store"""
        if not customers:
            return

        # Create text representations
        texts = [self._create_text_representation(customer) for customer in customers]
        
        # Generate embeddings
        embeddings = self.model.encode(texts)
        
        # Add to FAISS index
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Store original data
        self.stored_data.extend(customers)

    def search_similar_customers(self, query_text: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar customers based on a query"""
        if not self.stored_data:
            return []

        # Generate query embedding
        query_embedding = self.model.encode([query_text])
        
        # Search in FAISS
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            min(k, len(self.stored_data))
        )
        
        # Return similar customers
        return [self.stored_data[idx] for idx in indices[0]]

    def get_customer_context(self, customer_id: str) -> Dict[str, Any]:
        """Get customer context including similar customer patterns"""
        customer = next(
            (c for c in self.stored_data if c["customer_id"] == customer_id),
            None
        )
        
        if not customer:
            return None
            
        # Find similar customers
        similar_customers = self.search_similar_customers(
            self._create_text_representation(customer),
            k=3
        )
        
        # Remove the current customer from similar customers
        similar_customers = [
            c for c in similar_customers 
            if c["customer_id"] != customer_id
        ]
        
        return {
            "customer": customer,
            "similar_patterns": similar_customers
        }
