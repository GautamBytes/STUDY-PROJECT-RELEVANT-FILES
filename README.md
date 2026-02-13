**Decentralized Intelligence: Phase 2 Proof of Concept (PoC)**

This repository contains the core software prototype for the Phase 2 submission of the Study Project: Decentralized Intelligence: Peer-to-Peer AI Inference Networks in the Indian Context.
This PoC demonstrates the technical feasibility of the "Whole-Model Replication" architecture. It proves that a consumer-grade machine can load a quantized Large Language Model (LLM) and stream inference results over an HTTP network with near-zero latency (Time-To-First-Token < 0.2s).

**📁 Repository Contents**

**worker.py:** The lightweight API Gateway and Inference Engine. Built with FastAPI and llama-cpp-python, it loads a .gguf model into memory and streams generated text via Server-Sent Events (SSE).
**client.py:** The Developer SDK. Built with the requests library, it formats user prompts, handles the network connection to the worker, and parses the SSE stream to print tokens in real-time.

**⚙️ Prerequisites and Setup**
To run this PoC locally, you will need Python 3 installed.

1. Install Dependencies:
`pip install fastapi uvicorn llama-cpp-python requests pydantic`

3. Download the Model:
This PoC is configured to use a lightweight quantized model for fast local testing.

Download TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf (approx 680 MB).
Rename the downloaded file to model.gguf and place it in the same directory as the Python scripts.

**🚀 How to Run the Demo**
You will need to open two separate terminal windows to simulate the P2P network interaction.

**Terminal 1: Start the Worker Node**
`python3 -m uvicorn worker:app --host 127.0.0.1 --port 8000`
Wait for the terminal to output: Model loaded successfully! Ready for inference.

**Terminal 2: Run the Client SDK**
`python3 client.py`

**📊 Expected Output & Metrics**
Once the client script is executed, the prompt is routed to the worker, and the AI's response will stream onto the screen token-by-token.
During local network testing, this architecture achieved:

Time-To-First-Token (TTFT): ~0.12 seconds
Total Generation Time: ~0.67 seconds
Memory Allocation: Stable (No OOM crashes)

(Note: Decentralized peer discovery via DHT and dynamic NAT traversal are excluded from this PoC and will be implemented in Phase 3).
