# Decentralized Intelligence: Phase 3 Extended Prototype

This repository contains the core software prototype for the Phase 3 submission of the Study Project: **Decentralized Intelligence: Peer-to-Peer AI Inference Networks in the Indian Context**.

Building upon the Phase 2 PoC, this Phase 3 implementation introduces **Dynamic Peer Discovery and Fault-Tolerant Routing**. It proves that consumer-grade machines can not only load and stream quantized Large Language Models (LLMs) with near-zero latency, but can also dynamically discover available nodes via a Service Registry and handle graceful node shutdowns without crashing the network.

## 📁 Repository Contents

* **`registry.py` (NEW):** The Service Registry. Acts as a centralized discovery directory (Port 9000). It tracks active worker nodes, handles dynamic IP registration, and safely deregisters nodes when they go offline.
* **`worker.py` (UPDATED):** The AI Compute Node (Port 8000). Built with `FastAPI` and `llama-cpp-python`. It loads a `.gguf` model, automatically registers itself with the network on startup, streams generated text via Server-Sent Events (SSE), and features a graceful shutdown hook to deregister when closed.
* **`client.py` (UPDATED):** The Developer SDK. It now queries the Service Registry first to find an active worker node, establishes a direct P2P connection to that node, and parses the SSE stream in real-time.

## ⚙️ Prerequisites and Setup

To run this prototype locally, you will need Python 3 installed.

**1. Install Dependencies:**
```bash
pip install fastapi uvicorn llama-cpp-python requests pydantic
```

**2. Download the Model:**

This system is configured to use a lightweight quantized model for fast local testing.

* Download `TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf` (approx 680 MB).
* Rename the downloaded file to `model.gguf` and place it in the same directory as the Python scripts.

## 🚀 How to Run the Phase 3 Demo

You will need to open three separate terminal windows to simulate the complete network interaction.

**Terminal 1: Start the Service Registry**
```bash
python3 -m uvicorn registry:app --host 127.0.0.1 --port 9000
```

**Terminal 2: Start the Worker Node**
```bash
python3 -m uvicorn worker:app --host 127.0.0.1 --port 8000
```

Wait for the terminal to output: `[Network] Successfully registered worker node with the directory!`

**Terminal 3: Run the Client SDK**
```bash
python3 client.py
```

> 💡 **Optional:** You can test the fault tolerance by pressing `CTRL+C` in Terminal 2 to kill the worker, and then running Terminal 3 again to see the client safely abort!

## 📊 Expected Output & Metrics

Once the client script is executed, it will dynamically discover the worker's IP and route the prompt. During Phase 3 local network testing, this dynamic architecture achieved:

* **Time-To-First-Token (TTFT):** ~0.11 seconds *(Includes registry hop)*
* **Total Generation Time:** ~0.65 seconds
* **Memory Allocation:** Stable (No OOM crashes)
* **Lifecycle Management:** 100% Graceful Shutdown & Deregistration

> **Note:** Transitioning the centralized `registry.py` into a fully trustless Kademlia DHT, alongside NAT traversal for public internet routing, is reserved for future Capstone scope extension.
