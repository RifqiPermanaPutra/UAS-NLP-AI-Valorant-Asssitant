from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from .graph import langgraph_app

app = FastAPI(title="AI Valorant Assistant Backend")

# Mengizinkan koneksi dari Next.js frontend (port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    inputs = {"question": req.message}
    result = langgraph_app.invoke(inputs)
    
    return {
        "reply": result["generation"],
        "intent": result["intent"],
        "documents": result.get("documents", [])
    }

@app.get("/api/stats")
async def get_stats():
    # Placeholder data untuk ditampilkan di Dashboard Next.js
    return {
        "total_agents": 24, # Sesuai jumlah agent di Valorant saat ini
        "total_weapons": 18,
        "total_patch_notes": 12,
        "total_documents": 54,
        "total_chunks": 180,
        "langsmith_status": "Active",
        "chroma_status": "Connected"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
