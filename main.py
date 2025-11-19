from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from database import db, database_url, database_name

app = FastAPI(title="Unified AI Automation Platform API", version="1.0.0")

# Allow all origins during development (Frontend uses Vite on 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "API is running", "version": "1.0.0"}


@app.get("/test")
async def test_database():
    try:
        collections = []
        status = "unavailable"
        if db is not None:
            collections = sorted(db.list_collection_names())
            # Simple ping via list collections
            status = "connected"
        return {
            "backend": "ok",
            "database": "mongodb",
            "database_url": "set" if database_url else "not_set",
            "database_name": database_name or "not_set",
            "connection_status": status,
            "collections": collections,
        }
    except Exception as e:
        return {
            "backend": "error",
            "error": str(e),
            "database": "mongodb",
            "database_url": "set" if database_url else "not_set",
            "database_name": database_name or "not_set",
            "connection_status": "error",
            "collections": [],
        }


@app.get("/schema")
async def get_schema_file():
    """Return the contents of schemas.py so clients can read defined models."""
    try:
        with open("schemas.py", "r", encoding="utf-8") as f:
            return {"filename": "schemas.py", "content": f.read()}
    except Exception as e:
        return {"error": str(e)}
