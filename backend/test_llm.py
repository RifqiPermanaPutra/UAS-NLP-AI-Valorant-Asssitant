from .config import llm
print("Testing LLM...")
try:
    response = llm.invoke("Hello, test!")
    print(response)
except Exception as e:
    print("Error:", e)
