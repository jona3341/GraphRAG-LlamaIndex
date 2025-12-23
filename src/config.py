import os
import sys

# 1. FORCE HUGGING FACE MIRROR (Essential for users in China)
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from llama_index.core import Settings
# Using OpenAILike to avoid "Unknown model" errors with DeepSeek
from llama_index.llms.openai_like import OpenAILike 
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def init_settings(deepseek_api_key: str):
    """
    Initializes global settings with DeepSeek (LLM) and BGE-M3 (Embedding).
    """
    if not deepseek_api_key:
        raise ValueError("DeepSeek API Key is missing. Please check your .env file.")

    print(">> [CONFIG] Initializing DeepSeek LLM & BGE-M3 Embeddings...")

    # 2. DeepSeek-V3 Configuration via OpenAILike
    # We manually set context_window to avoid auto-detection errors
    llm = OpenAILike(
        model="deepseek-chat",
        api_key=deepseek_api_key,
        api_base="https://api.deepseek.com", 
        is_chat_model=True,
        context_window=64000, 
        max_tokens=3000,
        temperature=0.0
    )

    # 3. Safe GPU Detection
    # Prevents crashes on Windows if CUDA is not available
    device_type = "cpu"
    try:
        import torch
        if torch.cuda.is_available():
            device_type = "cuda"
    except ImportError:
        pass 

    print(f">> [CONFIG] Compute Device Detected: {device_type.upper()}")
    print(">> [CONFIG] Loading BGE-M3 model from HF Mirror (this may take time on first run)...")
    
    # 4. BGE-M3 Embedding Model
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-m3",
        device=device_type
    )

    # 5. Apply Global Settings
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.chunk_size = 512
    
    print(f">> [CONFIG] Settings initialized successfully.")