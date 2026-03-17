from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ProfileSection(BaseModel):
    """
    Represents a high-level section of the profile (role, project, skill, etc.)
    Stored in the profile_metadata collection for semantic search.
    """

    section_type: str  # e.g., "role", "project", "skill", "education", "background"
    title: str  # Section title (e.g., "VP, Software Engineering Manager", "Factor API")
    metadata: Dict[str, Any] = {}  # Flexible metadata dict
    # Common metadata fields:
    # - timeframe: str (e.g., "2018-07 to Present", "Q4 2024")
    # - company: str (e.g., "Two Sigma (Venn)")
    # - category: str (e.g., "API / analytics", "data platform")
    # - technologies: List[str] (e.g., ["AWS", "Python", "React"])
    # - domain: str (e.g., "fintech", "investment analytics")
    # - visibility: str (e.g., "public", "private", "restricted")


class ProfileChunk(BaseModel):
    """
    Represents a text chunk from the profile for vector storage.
    Stored in the profile_content collection for semantic search.
    """

    content: str  # The actual text content
    section_type: str  # Which type of section this belongs to
    section_title: str  # Which specific section (for context)
    metadata: Dict[str, Any] = {}  # Metadata inherited from parent section
    chunk_index: int  # Position of this chunk in the document
