import uvicorn
import os
import sys

# 1. Force Python to see the 'src' folder
# We get the current folder (AURA) and add it to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Run the server
if __name__ == "__main__":
    print("🚀 Starting AutoSure System...")
    # "src.autosure.interface.api:app" points to the file api.py inside interface folder
    uvicorn.run("src.autosure.interface.api:app", host="127.0.0.1", port=8000, reload=True)