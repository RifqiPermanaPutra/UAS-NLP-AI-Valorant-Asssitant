from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .config import llm, llm_generator
from .vectorstores import agent_retriever, weapon_retriever, patch_retriever

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[dict]
    intent: str

def detect_intent(state):
    question = state["question"]
    print(f"\n--- DETECT INTENT: '{question}' ---")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Kamu adalah analis intent AI Valorant. Klasifikasikan pertanyaan pengguna ke salah satu intent berikut:\n"
                   "- AGENT_QUERY: Bertanya tentang agent, ability, role, dll.\n"
                   "- WEAPON_QUERY: Bertanya tentang senjata, damage, harga, recoil, wall penetration, dll.\n"
                   "- PATCH_QUERY: Bertanya tentang patch notes, update, nerf, buff terbaru.\n"
                   "- UNKNOWN_QUERY: Tidak terkait Valorant atau terlalu umum.\n"
                   "Jawab HANYA dengan nama intent (misal: AGENT_QUERY)."),
        ("human", "{question}")
    ])
    chain = prompt | llm | StrOutputParser()
    intent = chain.invoke({"question": question}).strip().upper()
    
    if intent not in ["AGENT_QUERY", "WEAPON_QUERY", "PATCH_QUERY"]:
        intent = "UNKNOWN_QUERY"
        
    print(f"-> Detected Intent: {intent}")
    return {"intent": intent, "question": question}

def agent_node(state):
    question = state["question"]
    intent = state["intent"]
    print(f"--- AGENT NODE ---")
    docs = agent_retriever.invoke(question)
    
    formatted_docs = [{"content": d.page_content, "source": d.metadata.get("source", "agents.xlsx")} for d in docs]
    return {"documents": formatted_docs, "question": question, "intent": intent}

def weapon_node(state):
    question = state["question"]
    intent = state["intent"]
    print(f"--- WEAPON NODE ---")
    docs = weapon_retriever.invoke(question)
    
    formatted_docs = [{"content": d.page_content, "source": d.metadata.get("source", "weapons.xlsx")} for d in docs]
    return {"documents": formatted_docs, "question": question, "intent": intent}

def patch_node(state):
    question = state["question"]
    intent = state["intent"]
    print(f"--- PATCH NOTES NODE ---")
    docs = patch_retriever.invoke(question)
    
    formatted_docs = [{"content": d.page_content, "source": d.metadata.get("source", "Unknown PDF")} for d in docs]
    return {"documents": formatted_docs, "question": question, "intent": intent}

def generate_answer(state):
    question = state["question"]
    documents = state.get("documents", [])
    intent = state["intent"]
    
    print("--- GENERATE ANSWER ---")
    
    if intent == "UNKNOWN_QUERY":
        generation = "Maaf, saya hanya difokuskan untuk menjawab pertanyaan terkait Agent, Weapon, dan Patch Notes Valorant."
        return {"generation": generation, "documents": [], "intent": intent}
    
    context = ""
    for idx, d in enumerate(documents):
        source_name = d['source']
        if "patch" in source_name.lower() or source_name.endswith(".pdf"):
            source_name = "https://playvalorant.com/en-us/news/game-updates/"
        elif "agent" in source_name.lower():
            source_name = "https://playvalorant.com/en-us/agents/"
        elif "weapon" in source_name.lower():
            source_name = "https://playvalorant.com/en-us/arsenal/"
            
        context += f"Source [{idx+1}] ({source_name}):\n{d['content']}\n\n"
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Kamu adalah 'AI Valorant Assistant'. Jawab pertanyaan secara langsung, natural, dan to-the-point menggunakan informasi dari konteks berikut.\n"
                   "PENTING: JANGAN PERNAH menggunakan kalimat kaku seperti 'Berdasarkan konteks RAG' atau merinci 'Sumber [1]'. Langsung berikan jawabannya layaknya manusia berbicara.\n"
                   "Jika informasinya tidak ada, katakan saja dengan singkat bahwa informasi tersebut tidak ditemukan.\n"
                   "Di bagian paling akhir jawaban, cukup tambahkan satu baris kecil: '*Sumber: [Link URL Website]*'.\n\n"
                   "Context:\n{context}"),
        ("human", "{question}")
    ])
    
    chain = prompt | llm_generator | StrOutputParser()
    generation = chain.invoke({"context": context, "question": question})
    
    return {"generation": generation, "documents": documents, "intent": intent, "question": question}

def route_intent(state):
    intent = state["intent"]
    if intent == "AGENT_QUERY":
        return "agent_node"
    elif intent == "WEAPON_QUERY":
        return "weapon_node"
    elif intent == "PATCH_QUERY":
        return "patch_node"
    else:
        return "generate_answer"

# Build Graph
print("Building LangGraph Workflow...")
workflow = StateGraph(GraphState)

workflow.add_node("detect_intent", detect_intent)
workflow.add_node("agent_node", agent_node)
workflow.add_node("weapon_node", weapon_node)
workflow.add_node("patch_node", patch_node)
workflow.add_node("generate_answer", generate_answer)

workflow.set_entry_point("detect_intent")

workflow.add_conditional_edges(
    "detect_intent",
    route_intent,
    {
        "agent_node": "agent_node",
        "weapon_node": "weapon_node",
        "patch_node": "patch_node",
        "generate_answer": "generate_answer"
    }
)

workflow.add_edge("agent_node", "generate_answer")
workflow.add_edge("weapon_node", "generate_answer")
workflow.add_edge("patch_node", "generate_answer")
workflow.add_edge("generate_answer", END)

langgraph_app = workflow.compile()
