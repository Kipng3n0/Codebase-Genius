"""FastAPI server to expose Jac walkers as REST API endpoints"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Codebase Genius API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    repo_url: str

@app.get("/status")
async def get_status():
    return {
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/analyze")
async def analyze_repository(request: AnalyzeRequest):
    # TODO: Integrate with Jac walkers
    return {
        "status": "success",
        "repo_url": request.repo_url,
        "documentation": {
            "markdown": f"# Documentation for {request.repo_url}\n\nAnalysis in progress...",
            "diagrams": []
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)