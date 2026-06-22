import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from .data_loaders import load_agents_data, load_weapons_data, load_patch_notes

# Initialize Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_agent_retriever():
    persist_dir = "./chroma_atsgen_v3"
    if os.path.exists(persist_dir) and os.path.exists(os.path.join(persist_dir, "chroma.sqlite3")):
        print("Loading existing agent ChromaDB...")
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        print("Creating new agent ChromaDB...")
        docs = load_agents_data()
        if not docs:
            print("WARNING: No agent documents found. Retriever might be empty.")
            vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_dir)
        else:
            vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def get_weapon_retriever():
    persist_dir = "./chroma_weapons_v2"
    if os.path.exists(persist_dir) and os.path.exists(os.path.join(persist_dir, "chroma.sqlite3")):
        print("Loading existing weapon ChromaDB...")
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        print("Creating new weapon ChromaDB...")
        docs = load_weapons_data()
        if not docs:
            print("WARNING: No weapon documents found. Retriever might be empty.")
            vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_dir)
        else:
            vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def get_patch_retriever():
    persist_dir = "./chroma_patches_v2"
    if os.path.exists(persist_dir) and os.path.exists(os.path.join(persist_dir, "chroma.sqlite3")):
        print("Loading existing patch ChromaDB...")
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    else:
        print("Creating new patch ChromaDB...")
        docs = load_patch_notes()
        if not docs:
            print("WARNING: No patch documents found. Retriever might be empty.")
            vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_dir)
        else:
            vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

# Global instances for reuse
agent_retriever = get_agent_retriever()
weapon_retriever = get_weapon_retriever()
patch_retriever = get_patch_retriever()
