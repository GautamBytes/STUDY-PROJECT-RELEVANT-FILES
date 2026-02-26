import requests
import json
import time
import random

class ClientSDK:
    """Abstracts the network complexity and handles dynamic peer discovery."""
    def __init__(self, registry_url: str):
        self.registry_url = registry_url

    def discover_worker(self) -> str:
        """Queries the registry to find an active worker node."""
        print(f"[*] Contacting registry at {self.registry_url} to discover workers...")
        try:
            response = requests.get(f"{self.registry_url}/workers")
            response.raise_for_status()
            workers = response.json()
            
            if not workers:
                print("[!] Registry returned an empty list. No workers online.")
                return None
                
            # Pick a random worker for basic load balancing
            selected_worker = random.choice(workers)
            print(f"[*] Discovery successful! Routing request to: {selected_worker}\n")
            return selected_worker
            
        except requests.exceptions.RequestException as e:
            print(f"\n[!] Error connecting to discovery registry: {e}")
            return None

    def generate(self, prompt: str, max_tokens: int = 100):
        # Step 1: Discover a worker dynamically!
        worker_url = self.discover_worker()
        if not worker_url:
            print("Generation aborted: No active compute nodes available.")
            return

        print(f"Sending prompt: '{prompt}'\n")
        print("Worker Response: ", end="", flush=True)

        start_time = time.time()
        first_token_time = None

        # Step 2: Connect directly to the discovered worker (P2P)
        try:
            response = requests.post(
                f"{worker_url}/v1/completions",
                json={"prompt": prompt, "max_tokens": max_tokens},
                stream=True 
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"\n[Error connecting to worker: {e}]")
            return

        # Step 3: Stream the response
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                
                if decoded_line.startswith("data: "):
                    data_str = decoded_line[6:] 
                    
                    if data_str == "[DONE]":
                        break
                    if not first_token_time:
                        first_token_time = time.time()
                    
                    token_data = json.loads(data_str)
                    print(token_data["token"], end="", flush=True)
        
        total_time = time.time() - start_time
        ttft = (first_token_time - start_time) if first_token_time else 0
        print(f"\n\n[Stream Completed | TTFT: {ttft:.2f}s | Total Time: {total_time:.2f}s]")

if __name__ == "__main__":
    # Note: We now point the SDK to the REGISTRY, not the worker!
    sdk = ClientSDK(registry_url="http://127.0.0.1:9000")
    
    sdk.generate("Explain what a black hole is in two short sentences.")