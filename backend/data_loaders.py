import pandas as pd
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def load_agents_data(file_path="./dataset/valorant_agents1.xlsx"):
    print("Loading agents...")
    if not os.path.exists(file_path):
        return []
    df = pd.read_excel(file_path)
    docs = []
    for index, row in df.iterrows():
        content = f"Agent: {row.get('Agent', '')}\nRole: {row.get('Role', '')}\nDescription: {row.get('Agent Description', '')}\nAbility {row.get('Ability Slot', '')} ({row.get('Ability Type', '')}): {row.get('Ability Name', '')} - {row.get('Ability Description', '')}"
        metadata = {"source": "valorant_agents1.xlsx", "agent": row.get('Agent', '')}
        docs.append(Document(page_content=content, metadata=metadata))
    return docs

def load_weapons_data(file_path="./dataset/weapons.xlsx"):
    print("Loading weapons...")
    if not os.path.exists(file_path):
        return []
    df = pd.read_excel(file_path)
    docs = []
    for index, row in df.iterrows():
        content = f"Weapon: {row.get('Weapon', '')}\nCategory: {row.get('Category', '')}\nCost: {row.get('Cost', '')}\nMagazine Size: {row.get('Magazine Size', '')}\nFire Rate: {row.get('Fire Rate', '')}\nReload Time: {row.get('Reload Time', '')}\nWall Penetration: {row.get('Wall Penetration', '')}\nHead Damage: {row.get('Head Damage', '')}\nBody Damage: {row.get('Body Damage', '')}\nLeg Damage: {row.get('Leg Damage', '')}"
        metadata = {"source": "weapons.xlsx", "weapon": row.get('Weapon', '')}
        docs.append(Document(page_content=content, metadata=metadata))
    return docs

def load_patch_notes(directory_path="./dataset/patch_notes"):
    print("Loading patch notes...")
    if not os.path.exists(directory_path):
        return []
    
    docs = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(directory_path, filename))
            pdf_docs = loader.load()
            for doc in pdf_docs:
                doc.metadata["source"] = filename
            docs.extend(pdf_docs)
            
    # Text splitting khusus untuk patch notes karena dokumennya bisa panjang
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits
