import openai
from g_config import create_openai_config

def create_vector_store(file_ids: list):
    """Creates a vector store with the provided file IDs."""
    try:
        # Create the vector store
        vector_store = openai.vector_stores.create(
            name="MY_CV_VECTOR_STORE",
            file_ids=file_ids
        )
        # Access the 'id' attribute directly
        vector_store_id = vector_store.id
        print(f"Vector store created successfully. Vector Store ID: {vector_store_id}")
        return vector_store_id
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

# Create a vector store with the uploaded CV
file_ids = ["file-Vw1Kd4UJ88b341e4F8Zqqt"]  # Replace with your actual file ID
vector_store_id = create_vector_store(file_ids)
print(f"Vector Store ID: {vector_store_id}")
