from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="P2P Discovery Registry")

# In-memory database of active workers
active_workers = set()

class WorkerInfo(BaseModel):
    url: str

@app.post("/register")
async def register_worker(worker: WorkerInfo):
    """Worker nodes call this to announce they are online."""
    active_workers.add(worker.url)
    print(f"[Registry] New Worker Registered: {worker.url}")
    return {"message": "Registered successfully", "active_workers": list(active_workers)}

@app.get("/workers", response_model=List[str])
async def get_workers():
    """Client SDK calls this to find available workers."""
    if not active_workers:
        raise HTTPException(status_code=404, detail="No active workers available on the network.")
    return list(active_workers)

@app.post("/deregister")
async def deregister_worker(worker: WorkerInfo):
    """Worker nodes call this when shutting down to remove themselves."""
    if worker.url in active_workers:
        active_workers.remove(worker.url)
        print(f"[Registry] Worker Offline/Removed: {worker.url}")
    return {"message": "Deregistered successfully"}