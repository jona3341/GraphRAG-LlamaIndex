import os
from dotenv import load_dotenv
from llama_index.core import (
    StorageContext,
    KnowledgeGraphIndex
)

# Import local modules
from src.config import init_settings
from src.loader import load_documents_from_csv
from src.prompts import CUSTOM_KG_TRIPLET_EXTRACT_TMPL

# Constants
PERSIST_DIR = "./storage_graph_csv"
DATA_FILE = "data/clean_data_100.csv"

def build_graph():
    # 1. Load Environment Variables
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # 2. Initialize Models
    init_settings(api_key)

    print(f"\n=== STARTING INDEXATION PROCESS ===")
    
    # 3. Load Data
    if not os.path.exists(DATA_FILE):
        print(f"[ERROR] Data file not found at: {DATA_FILE}")
        return

    documents = load_documents_from_csv(DATA_FILE)

    # 4. Build Graph (Calls DeepSeek API)
    print("\n>> [BUILD] Calling DeepSeek to extract relationships (Please wait)...")
    
    storage_context = StorageContext.from_defaults()
    
    index = KnowledgeGraphIndex.from_documents(
        documents,
        storage_context=storage_context,
        max_triplets_per_chunk=10, 
        include_embeddings=True, # Enable Hybrid Search (Vector + Graph)
        kg_triple_extract_template=CUSTOM_KG_TRIPLET_EXTRACT_TMPL,
        show_progress=True
    )

    # 5. Save to Disk
    print(f"\n>> [SAVE] Persisting index to folder '{PERSIST_DIR}'...")
    if not os.path.exists(PERSIST_DIR):
        os.makedirs(PERSIST_DIR)
        
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print("=== INDEXATION COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    build_graph()