<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/f/fc/Valorant_logo_-_pink_color_version.svg" alt="Valorant Logo" width="100"/>
  <h1>🎮 AI Valorant Assistant</h1>
  <p><strong>UAS Natural Language Processing (NLP) Project</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
    <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white" alt="LangChain" />
  </p>
</div>

---

## 📝 Deskripsi Proyek
**AI Valorant Assistant** adalah sebuah chatbot cerdas berbasis AI yang dirancang layaknya asisten atau *coach* bagi pemain Valorant. Sistem ini dapat menjawab pertanyaan spesifik seputar detail agen, spesifikasi senjata, dan *patch notes* terbaru dengan keakuratan tinggi dan **bebas halusinasi**.

Proyek ini tidak menggunakan arsitektur RAG konvensional, melainkan mengusung inovasi **Multi-RAG dengan Intent-based Routing** yang dibalut dalam ekosistem aplikasi *Full-Stack*.

---

## ✨ Fitur Utama (Keunikan Proyek)
1. **Agentic Workflow (LangGraph)**: Memiliki kecerdasan untuk mengklasifikasi niat pengguna (*detect_intent*) sebelum melakukan pencarian data.
2. **Multi-RAG Architecture**: Pemisahan laci memori menjadi 3 *Vector Store* independen (`Agent`, `Weapon`, `Patch`) untuk mencegah polusi konteks.
3. **Source Citation**: Menyertakan metadata dan referensi asal data (*Retrieved Documents*) di setiap jawaban.
4. **Full-Stack Premium UI**: Antarmuka web modern dengan Next.js 15 dan Tailwind CSS bernuansa *Valorant Dark Mode*.
5. **Observability**: Terintegrasi penuh dengan LangSmith untuk pemantauan latensi dan konsumsi token.

---

## 📸 Screenshots

| System Dashboard | New Chat (AI Interface) |
| :---: | :---: |
| <img src="docs/dashboard.png" alt="Dashboard" width="400" /> | <img src="docs/chat-ui.png" alt="Chat UI" width="400" /> |

| Architecture | RAG Pipeline |
| :---: | :---: |
| <img src="docs/architecture.png" alt="Architecture" width="400" /> | <img src="docs/rag-pipeline.png" alt="RAG Pipeline" width="400" /> |

| Knowledge Base | LangGraph Flow |
| :---: | :---: |
| <img src="docs/knowledge-base.png" alt="Knowledge Base" width="400" /> | <img src="docs/langgraph.png" alt="LangGraph Flow" width="400" /> |

| LangSmith Monitor | |
| :---: | :---: |
| <img src="docs/langsmith.png" alt="LangSmith Monitor" width="400" /> | |

---

## 📚 Library NLP Wajib yang Digunakan
Sesuai dengan kriteria tugas, proyek ini mengimplementasikan:
- **[LangChain]**: Bertugas untuk proses *Data Ingestion* (menggunakan `PyPDFLoader`, `RecursiveCharacterTextSplitter`) dan *Retrieval* dari *HuggingFaceEmbeddings*.
- **[LangGraph]**: Bertugas mengatur logika *routing* menggunakan `StateGraph` dan *Conditional Edges* untuk arsitektur Multi-RAG.
- **[LangSmith]**: Bertugas untuk melacak dan mengevaluasi setiap *trace*, latensi, dan token (*Observability*).

---

## 🚀 Cara Menjalankan Program (Localhost)

1️⃣ Menjalankan Backend (FastAPI)
Buka Terminal pertama, lalu jalankan perintah berikut:
```bash
# 1. Masuk ke direktori utama
cd D:\VLR

# 2. Aktifkan Virtual Environment
.\venv\Scripts\activate

# 3. Jalankan server FastAPI
python -m backend.main

2️⃣ Menjalankan Frontend (Next.js)
Buka Terminal kedua (biarkan terminal Backend tetap menyala), lalu jalankan:
```bash
# 1. Masuk ke folder frontend
cd D:\VLR\frontend

# 2. Instal dependensi (jika belum)
npm install

# 3. Jalankan server Next.js
npm run dev
```

### 3️⃣ Memulai Aplikasi
Buka Web Browser Anda dan kunjungi: **`http://localhost:3000`**
