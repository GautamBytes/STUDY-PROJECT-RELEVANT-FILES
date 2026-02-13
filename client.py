import requests
import json
import time

class ClientSDK:
    """Abstracts the network complexity of the P2P Inference Grid."""
    def __init__(self, worker_url: str):
        self.worker_url = worker_url

    def generate(self, prompt: str, max_tokens: int = 100):
        print(f"Sending prompt: '{prompt}'\n")
        print("Worker Response: ", end="", flush=True)

        start_time = time.time()
        first_token_time = None

        # 1. Connect to the worker node and request a stream
        try:
            response = requests.post(
                f"{self.worker_url}/v1/completions",
                json={"prompt": prompt, "max_tokens": max_tokens},
                stream=True 
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"\n[Error connecting to worker: {e}]")
            return

        # 2. Iterate over the Server-Sent Events (SSE) stream
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[6:] # Strip "data: " prefix
                    
                    if data_str == "[DONE]":
                        break
                    
                    if not first_token_time:
                        first_token_time = time.time()
                    
                    # Parse the JSON and print the token in real-time
                    token_data = json.loads(data_str)
                    print(token_data["token"], end="", flush=True)
        
        # Calculate performance metrics
        total_time = time.time() - start_time
        ttft = (first_token_time - start_time) if first_token_time else 0
        print(f"\n\n[Stream Completed | TTFT: {ttft:.2f}s | Total Time: {total_time:.2f}s]")

if __name__ == "__main__":
    # Initialize SDK pointing to the local worker node
    sdk = ClientSDK(worker_url="http://127.0.0.1:8000")
    
    # Test the network
    sdk.generate("Explain what a black hole is in two short sentences.")