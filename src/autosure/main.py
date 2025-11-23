import uvicorn

if __name__ == "__main__":
    print("🚀 Starting AutoSure API Server...")
    # Runs the FastAPI app located in interface/api.py
    uvicorn.run("src.autosure.interface.api:app", port=8000, reload=True)