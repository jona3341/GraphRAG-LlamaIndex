import os
import sys
from dotenv import load_dotenv
from llama_index.core import (
    StorageContext,
    load_index_from_storage
)

# Import local modules
from src.config import init_settings
# Note: This imports the prompt we defined in src/prompts.py
# (which might be the Chinese one or English one depending on your last edit)
from src.prompts import CUSTOM_CHAT_PROMPT

# Directory where the database is stored
PERSIST_DIR = "./storage_graph_csv"

def start_chat():
    # 1. Load Environment Variables & API Key
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # 2. Initialize Models (DeepSeek + BGE-M3)
    try:
        init_settings(api_key)
    except Exception as e:
        print(f"[ERROR] Configuration failed: {e}")
        return

    # 3. Check if the database exists
    if not os.path.exists(PERSIST_DIR):
        print(f"\n[ERROR] The folder '{PERSIST_DIR}' does not exist.")
        print(">> Please run 'python index.py' first to build the database.")
        return

    print(f"\n>> [SYSTEM] Loading graph from disk '{PERSIST_DIR}'...")
    try:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    except Exception as e:
        print(f"[ERROR] Could not load index: {e}")
        return

    # 4. Create Query Engine
    # We use 'compact' mode to pass retrieved context directly to the LLM
    # adhering strictly to the 'Role' defined in src/prompts.py
    query_engine = index.as_query_engine(
        include_text=True,
        response_mode="compact",  
        similarity_top_k=5,       # Retrieve top 5 matches
        text_qa_template=CUSTOM_CHAT_PROMPT, # Apply strict prompt rules
        verbose=True              # Show internal reasoning in console
    )

    # 5. Chat Loop
    print("\n" + "="*40)
    print("  BOOK RECOMMENDATION SYSTEM")
    print("  Type 'exit', 'quit' or 'q' to stop.")
    print("="*40 + "\n")

    while True:
        user_input = input("Your Query: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        
        if not user_input.strip():
            continue

        print("\n[AI] Thinking...\n")
        try:
            response = query_engine.query(user_input)
            # Display Final Response
            print(f"RESPONSE:\n{response}\n")
            print("-" * 40)
        except Exception as e:
            print(f"Error during query: {e}")

if __name__ == "__main__":
    start_chat()import os
import sys
from dotenv import load_dotenv
from llama_index.core import (
    StorageContext,
    load_index_from_storage
)

# Import local modules
from src.config import init_settings
# Note: This imports the prompt we defined in src/prompts.py
# (which might be the Chinese one or English one depending on your last edit)
from src.prompts import CUSTOM_CHAT_PROMPT

# Directory where the database is stored
PERSIST_DIR = "./storage_graph_csv"

def start_chat():
    # 1. Load Environment Variables & API Key
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # 2. Initialize Models (DeepSeek + BGE-M3)
    try:
        init_settings(api_key)
    except Exception as e:
        print(f"[ERROR] Configuration failed: {e}")
        return

    # 3. Check if the database exists
    if not os.path.exists(PERSIST_DIR):
        print(f"\n[ERROR] The folder '{PERSIST_DIR}' does not exist.")
        print(">> Please run 'python index.py' first to build the database.")
        return

    print(f"\n>> [SYSTEM] Loading graph from disk '{PERSIST_DIR}'...")
    try:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    except Exception as e:
        print(f"[ERROR] Could not load index: {e}")
        return

    # 4. Create Query Engine
    # We use 'compact' mode to pass retrieved context directly to the LLM
    # adhering strictly to the 'Role' defined in src/prompts.py
    query_engine = index.as_query_engine(
        include_text=True,
        response_mode="compact",  
        similarity_top_k=5,       # Retrieve top 5 matches
        text_qa_template=CUSTOM_CHAT_PROMPT, # Apply strict prompt rules
        verbose=True              # Show internal reasoning in console
    )

    # 5. Chat Loop
    print("\n" + "="*40)
    print("  BOOK RECOMMENDATION SYSTEM")
    print("  Type 'exit', 'quit' or 'q' to stop.")
    print("="*40 + "\n")

    while True:
        user_input = input("Your Query: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        
        if not user_input.strip():
            continue

        print("\n[AI] Thinking...\n")
        try:
            response = query_engine.query(user_input)
            # Display Final Response
            print(f"RESPONSE:\n{response}\n")
            print("-" * 40)
        except Exception as e:
            print(f"Error during query: {e}")

if __name__ == "__main__":
    start_chat()