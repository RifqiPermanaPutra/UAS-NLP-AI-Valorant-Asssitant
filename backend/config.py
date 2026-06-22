import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT", "UAS-Valorant-AI-Coach")

nvidia_api_key = os.environ.get("NVIDIA_API_KEY", "")

llm = ChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key,
    model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
    temperature=0
)

llm_generator = ChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key,
    model="nvidia/llama-3.3-nemotron-super-49b-v1.5",
    temperature=0.6,
    top_p=0.95,
    max_tokens=65536
)
