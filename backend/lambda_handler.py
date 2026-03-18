"""
Just loads profile JSON and passes full context to Claude
"""
import os
import sys
from pathlib import Path

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent))

print("🚀 Lambda cold start")

# Import FastAPI app
print("📦 Importing FastAPI app...")
from app import app

# Import Mangum adapter for Lambda
print("🔌 Importing Mangum adapter...")
from mangum import Mangum

# Create Lambda handler
print("✅ Lambda handler ready - profile loaded in memory")
handler = Mangum(app, lifespan="off")
