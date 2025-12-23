import os
import pandas as pd
from llama_index.core import Document

def load_documents_from_csv(file_path: str):
    """
    Reads a CSV file and converts it into LlamaIndex Document objects.
    Expects columns: book_id, book_name, book_summary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
    
    print(f">> [LOADER] Reading CSV file: {file_path}")
    df = pd.read_csv(file_path)
    
    documents = []
    # Iterate over each row to create a clean Document object
    for _, row in df.iterrows():
        # CRITICAL TRICK: We inject the title directly into the text body.
        # This ensures the LLM 'sees' the title immediately when reading the chunk,
        # preventing it from getting lost in metadata.
        text_content = (
            f"BOOK TITLE: {row['book_name']}\n"
            f"SOURCE ID: {row['book_id']}\n"
            f"SUMMARY:\n{row['book_summary']}"
        )
        
        # We still keep metadata for system-level filtering if needed later
        metadata = {
            'book_name': row['book_name'],
            'book_id': str(row['book_id'])
        }
        
        doc = Document(text=text_content, metadata=metadata)
        documents.append(doc)
    
    print(f">> [LOADER] {len(documents)} books loaded with embedded titles.")
    return documents