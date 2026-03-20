#!/usr/bin/env python3
"""
Fix #3: Model Setup Script

This script auto-generates training data and trains the Isolation Forest model
if the .pkl files are missing. Run this ONCE after cloning the repo before
starting the backend server.

Usage:
    python setup_model.py
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, "ai-model", "isolation_forest_model.pkl")
ENCODERS_FILE = os.path.join(BASE_DIR, "ai-model", "encoders.pkl")
DATA_FILE = os.path.join(BASE_DIR, "data", "generated_logs.csv")

def main():
    print("=" * 50)
    print("AI Security Monitor - Model Setup")
    print("=" * 50)

    # Step 1: Generate training data if missing
    if not os.path.exists(DATA_FILE):
        print("[1/2] Generating training data...")
        sys.path.insert(0, os.path.join(BASE_DIR, "backend"))
        try:
            from log_generator import generate_logs
            generate_logs()
            print(f"     Data saved to: {DATA_FILE}")
        except ImportError:
            print("     Running log_generator.py directly...")
            os.system(f"{sys.executable} backend/log_generator.py")
    else:
        print(f"[1/2] Training data already exists: {DATA_FILE}")

    # Step 2: Train model if .pkl files are missing
    if not os.path.exists(MODEL_FILE) or not os.path.exists(ENCODERS_FILE):
        print("[2/2] Training Isolation Forest model...")
        os.system(f"{sys.executable} ai-model/train_model.py")
        if os.path.exists(MODEL_FILE):
            print(f"     Model saved to: {MODEL_FILE}")
            print(f"     Encoders saved to: {ENCODERS_FILE}")
        else:
            print("     ERROR: Model training failed. Check the output above.")
            sys.exit(1)
    else:
        print(f"[2/2] Model files already exist:")
        print(f"      {MODEL_FILE}")
        print(f"      {ENCODERS_FILE}")

    print("")
    print("Setup complete! You can now run:")
    print("  docker-compose up --build    # Full Docker setup")
    print("  OR")
    print("  cd backend && uvicorn main:app --reload   # Local backend")
    print("  cd frontend && npm run dev               # Local frontend")

if __name__ == "__main__":
    main()
