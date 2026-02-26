from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llama_cpp import Llama
import json
import requests

app = FastAPI(title="P2P AI Worker Node")

# Configuration 
WORKER_URL = "http://127.0.0.1:8000"
REGISTRY_URL = "http://127.0.0.1:9000"

# 1. Load the quantized model into memory
print("Loading model into memory... Please wait.")
llm = Llama(model_path="./model.gguf", verbose=False)
print("Model loaded successfully! Ready for inference.")

@app.on_event("startup")
async def register_with_network():
    """Automatically registers this node with the central discovery registry."""
    print(f"Attempting to register with network at {REGISTRY_URL}...")
    try:
        response = requests.post(f"{REGISTRY_URL}/register", json={"url": WORKER_URL})
        if response.status_code == 200:
            print("[Network] Successfully registered worker node with the directory!")
    except Exception as e:
        print(f"[Network] Failed to connect to registry. Is registry.py running? Error: {e}")

@app.on_event("shutdown")
async def deregister_from_network():
    """Politely tells the central registry this node is going offline."""
    print("Shutting down... Deregistering from network.")
    try:
        response = requests.post(f"{REGISTRY_URL}/deregister", json={"url": WORKER_URL})
        if response.status_code == 200:
            print("[Network] Successfully removed from registry.")
    except Exception as e:
        print(f"[Network] Failed to deregister: {e}")

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.post("/v1/completions")
async def generate_completion(req: PromptRequest):
    """Handles incoming prompts and streams the response via SSE."""
    def stream_tokens():
        stream = llm(
            f"<|user|>\n{req.prompt}\n<|assistant|>\n", 
            max_tokens=req.max_tokens,
            stream=True
        )
        for output in stream:
            token = output["choices"][0]["text"]
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream_tokens(), media_type="text/event-stream")