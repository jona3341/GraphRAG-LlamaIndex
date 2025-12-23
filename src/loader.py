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
        # The main content to analyze is the summary
        text_content = row['book_summary']
        
        # Attach title and ID as metadata
        metadata = {
            'book_name': row['book_name'],
            'book_id': str(row['book_id'])
        }
        
        doc = Document(text=text_content, metadata=metadata)
        documents.append(doc)
    
    print(f">> [LOADER] {len(documents)} books loaded and prepared for indexing.")
    return documents