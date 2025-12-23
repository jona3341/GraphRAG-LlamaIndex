import os
import sys
from dotenv import load_dotenv
from llama_index.core import (
    StorageContext,
    load_index_from_storage
)

# Import des modules locaux
from src.config import init_settings
from src.prompts import CUSTOM_CHAT_PROMPT

# Dossier de la base de données
PERSIST_DIR = "./storage_graph_csv"

def start_chat():
    # 1. Chargement de l'environnement et de la clé API
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # 2. Initialisation des modèles (DeepSeek + BGE-M3)
    try:
        init_settings(api_key)
    except Exception as e:
        print(f"[ERROR] Configuration failed: {e}")
        return

    # 3. Vérification de la présence de la base de données
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

    # 4. Création du moteur de recherche (CORRECTION ICI)
    # On passe en mode "compact" pour respecter strictement le Prompt "Role"
    query_engine = index.as_query_engine(
        include_text=True,
        response_mode="compact",  # <--- CHANGEMENT CLE : "compact" au lieu de "tree_summarize"
        similarity_top_k=5,       # On récupère 5 livres potentiels pour laisser du choix au LLM
        text_qa_template=CUSTOM_CHAT_PROMPT, # On applique ton Prompt strict
        verbose=True              # Affiche les étapes dans la console
    )

    # 5. Boucle de discussion
    print("\n" + "="*40)
    print("  SYSTEME DE RECOMMANDATION (Format Strict)")
    print("  Tapez 'exit' pour quitter.")
    print("="*40 + "\n")

    while True:
        user_input = input("Votre demande : ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Au revoir !")
            break
        
        if not user_input.strip():
            continue

        print("\n[AI] Reflexion en cours...\n")
        try:
            response = query_engine.query(user_input)
            # Affichage de la réponse finale
            print(f"RÉPONSE :\n{response}\n")
            print("-" * 40)
        except Exception as e:
            print(f"Erreur lors de la réponse : {e}")

if __name__ == "__main__":
    start_chat()