#!/usr/bin/env python3
"""
Startup script — runs FastAPI backend and Streamlit frontend concurrently.
"""
import subprocess
import sys
import os
import time
import signal

def main():
    procs = []

    print("🚀 Starting AI Travel Planner...\n")

    # Start FastAPI backend
    backend_cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
    ]
    print("🔧 Starting FastAPI backend on http://localhost:8000")
    backend = subprocess.Popen(backend_cmd, cwd=os.path.dirname(__file__))
    procs.append(backend)

    time.sleep(2)  # Give backend a moment to bind

    # Start Streamlit frontend
    frontend_cmd = [
        sys.executable, "-m", "streamlit", "run",
        "frontend/Home.py",
        "--server.port", "8501",
        "--server.address", "localhost",
    ]
    print("🎨 Starting Streamlit frontend on http://localhost:8501\n")
    frontend = subprocess.Popen(frontend_cmd, cwd=os.path.dirname(__file__))
    procs.append(frontend)

    print("✅ Both services are starting up.")
    print("   Backend  → http://localhost:8000")
    print("   Frontend → http://localhost:8501")
    print("   API Docs → http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all services.\n")

    def shutdown(sig, frame):
        print("\n🛑 Shutting down...")
        for p in procs:
            p.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for p in procs:
        p.wait()


if __name__ == "__main__":
    main()
