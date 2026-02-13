from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llama_cpp import Llama
import json

app = FastAPI(title="P2P AI Worker Node")

# 1. Load the quantized model into memory
print("Loading model into memory... Please wait.")
llm = Llama(model_path="./model.gguf", verbose=False)
print("Model loaded successfully! Ready for inference.")

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

@app.post("/v1/completions")
async def generate_completion(req: PromptRequest):
    """Handles incoming prompts and streams the response via SSE."""
    
    def stream_tokens():
        # 2. Start the inference engine generator
        stream = llm(
            f"<|user|>\n{req.prompt}\n<|assistant|>\n", # TinyLlama prompt format
            max_tokens=req.max_tokens,
            stream=True
        )
        
        # 3. Yield tokens as Server-Sent Events (SSE)
        for output in stream:
            token = output["choices"][0]["text"]
            yield f"data: {json.dumps({'token': token})}\n\n"
        
        # End of stream indicator
        yield "data: [DONE]\n\n"

    # Return the streaming response to the client
    return StreamingResponse(stream_tokens(), media_type="text/event-stream")