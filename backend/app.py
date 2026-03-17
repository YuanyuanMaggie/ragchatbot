import warnings

warnings.filterwarnings("ignore", message="resource_tracker: There appear to be.*")

import os
from typing import List, Optional

from config import config
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rag_system import RAGSystem

# Initialize FastAPI app
app = FastAPI(title="Yuanyuan Li - Personal Profile Assistant", root_path="")

# Add trusted host middleware for proxy
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Enable CORS with proper settings for proxy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize RAG system
rag_system = RAGSystem(config)


# Pydantic models for request/response
class QueryRequest(BaseModel):
    """Request model for profile queries"""

    query: str
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    """Response model for profile queries"""

    answer: str
    sources: List[str]
    source_links: List[Optional[str]]
    session_id: str


class ProfileStats(BaseModel):
    """Response model for profile statistics"""

    total_sections: int
    section_types: List[str]
    key_highlights: List[str]


class ClearSessionRequest(BaseModel):
    """Request model for clearing a session"""

    session_id: str


# API Endpoints


@app.post("/api/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Process a query and return response with sources"""
    try:
        # Create session if not provided
        session_id = request.session_id
        if not session_id:
            session_id = rag_system.session_manager.create_session()

        # Process query using RAG system
        answer, sources, source_links = rag_system.query(request.query, session_id)

        return QueryResponse(
            answer=answer,
            sources=sources,
            source_links=source_links,
            session_id=session_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/profile-stats", response_model=ProfileStats)
async def get_profile_stats():
    """Get profile analytics and statistics"""
    try:
        analytics = rag_system.get_profile_analytics()
        return ProfileStats(
            total_sections=analytics["total_sections"],
            section_types=analytics["section_types"],
            key_highlights=analytics["key_highlights"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/clear-session")
async def clear_session(request: ClearSessionRequest):
    """Clear a conversation session"""
    try:
        rag_system.session_manager.clear_session(request.session_id)
        return {"status": "success", "message": "Session cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
async def startup_event():
    """Load initial profile documents on startup"""
    print("Loading profile documents...")
    try:
        # Load profile file from root directory
        profile_files = [
            "../yuanyuan_li_profile.json",
        ]
        total_sections = 0
        total_chunks = 0
        for file_path in profile_files:
            if os.path.exists(file_path):
                sections, chunks = rag_system.add_profile_document(file_path)
                total_sections += sections
                total_chunks += chunks
                print(
                    f"Loaded {os.path.basename(file_path)}: {sections} sections, {chunks} chunks"
                )
        print(
            f"✓ Total profile data loaded: {total_sections} sections with {total_chunks} chunks"
        )
    except Exception as e:
        print(f"Error loading profile documents: {e}")


# Custom static file handler with no-cache headers for development
class DevStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if isinstance(response, FileResponse):
            # Add no-cache headers for development
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response


# Serve static files for the frontend
app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
