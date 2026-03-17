from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.config import Settings
from models import ProfileChunk, ProfileSection


@dataclass
class SearchResults:
    """Container for search results with metadata"""

    documents: List[str]
    metadata: List[Dict[str, Any]]
    distances: List[float]
    error: Optional[str] = None

    @classmethod
    def from_chroma(cls, chroma_results: Dict) -> "SearchResults":
        """Create SearchResults from ChromaDB query results"""
        return cls(
            documents=(
                chroma_results["documents"][0] if chroma_results["documents"] else []
            ),
            metadata=(
                chroma_results["metadatas"][0] if chroma_results["metadatas"] else []
            ),
            distances=(
                chroma_results["distances"][0] if chroma_results["distances"] else []
            ),
        )

    @classmethod
    def empty(cls, error_msg: str) -> "SearchResults":
        """Create empty results with error message"""
        return cls(documents=[], metadata=[], distances=[], error=error_msg)

    def is_empty(self) -> bool:
        """Check if results are empty"""
        return len(self.documents) == 0


class VectorStore:
    """Vector storage using ChromaDB for profile content and metadata"""

    def __init__(self, chroma_path: str, embedding_model: str, max_results: int = 5):
        self.max_results = max_results
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=chroma_path, settings=Settings(anonymized_telemetry=False)
        )

        # Set up sentence transformer embedding function
        self.embedding_function = (
            chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=embedding_model
            )
        )

        # Profile collections only
        self.profile_metadata = self._create_collection(
            "profile_metadata"
        )  # Profile sections (roles, projects, skills)
        self.profile_content = self._create_collection(
            "profile_content"
        )  # Searchable profile text chunks

    def _create_collection(self, name: str):
        """Create or get a ChromaDB collection"""
        return self.client.get_or_create_collection(
            name=name, embedding_function=self.embedding_function
        )

    def add_profile_section(self, section: ProfileSection):
        """Add a profile section to the metadata collection for semantic search"""
        import json

        # Create searchable text from section title
        section_text = section.title

        # Serialize metadata as JSON string for storage
        metadata_dict = {
            "section_type": section.section_type,
            "title": section.title,
            "metadata_json": json.dumps(section.metadata),
        }

        # Add common metadata fields at top level for easier filtering
        if "timeframe" in section.metadata:
            metadata_dict["timeframe"] = section.metadata["timeframe"]
        if "company" in section.metadata:
            metadata_dict["company"] = section.metadata["company"]
        if "category" in section.metadata:
            metadata_dict["category"] = section.metadata["category"]

        # Use section_type + title as unique ID
        section_id = f"{section.section_type}_{section.title.replace(' ', '_')[:50]}"

        self.profile_metadata.add(
            documents=[section_text], metadatas=[metadata_dict], ids=[section_id]
        )

    def add_profile_content(self, chunks: List[ProfileChunk]):
        """Add profile content chunks to the vector store"""
        if not chunks:
            return

        import json

        documents = [chunk.content for chunk in chunks]
        metadatas = []
        ids = []

        for chunk in chunks:
            metadata_dict = {
                "section_type": chunk.section_type,
                "section_title": chunk.section_title,
                "chunk_index": chunk.chunk_index,
                "metadata_json": json.dumps(chunk.metadata),
            }

            # Add common metadata fields at top level for easier filtering
            if "timeframe" in chunk.metadata:
                metadata_dict["timeframe"] = chunk.metadata["timeframe"]
            if "company" in chunk.metadata:
                metadata_dict["company"] = chunk.metadata["company"]
            if "category" in chunk.metadata:
                metadata_dict["category"] = chunk.metadata["category"]

            metadatas.append(metadata_dict)

            # Use section_title with chunk index for unique IDs
            chunk_id = f"{chunk.section_title.replace(' ', '_')[:40]}_{chunk.chunk_index}"
            ids.append(chunk_id)

        self.profile_content.add(documents=documents, metadatas=metadatas, ids=ids)

    def search_profile(
        self,
        query: str,
        section_type: Optional[str] = None,
        timeframe: Optional[str] = None,
        company: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> SearchResults:
        """
        Search profile content with optional filters.

        Args:
            query: What to search for in profile content
            section_type: Optional filter by section type (role, project, skill, etc.)
            timeframe: Optional filter by timeframe
            company: Optional filter by company
            limit: Maximum results to return

        Returns:
            SearchResults object with documents and metadata
        """
        # Build filter for profile content search
        filter_dict = self._build_profile_filter(section_type, timeframe, company)

        # Use provided limit or fall back to configured max_results
        search_limit = limit if limit is not None else self.max_results

        try:
            results = self.profile_content.query(
                query_texts=[query], n_results=search_limit, where=filter_dict
            )
            return SearchResults.from_chroma(results)
        except Exception as e:
            return SearchResults.empty(f"Search error: {str(e)}")

    def _build_profile_filter(
        self,
        section_type: Optional[str],
        timeframe: Optional[str],
        company: Optional[str],
    ) -> Optional[Dict]:
        """Build ChromaDB filter from profile search parameters"""
        conditions = []

        if section_type:
            conditions.append({"section_type": section_type})
        if timeframe:
            conditions.append({"timeframe": timeframe})
        if company:
            conditions.append({"company": company})

        if not conditions:
            return None

        if len(conditions) == 1:
            return conditions[0]

        return {"$and": conditions}

    def get_profile_sections_count(self) -> int:
        """Get the total number of profile sections in the vector store"""
        try:
            results = self.profile_metadata.get()
            if results and "ids" in results:
                return len(results["ids"])
            return 0
        except Exception as e:
            print(f"Error getting profile sections count: {e}")
            return 0

    def get_all_profile_sections(self) -> List[Dict[str, Any]]:
        """Get metadata for all profile sections in the vector store"""
        import json

        try:
            results = self.profile_metadata.get()
            if results and "metadatas" in results:
                # Parse metadata JSON for each section
                parsed_metadata = []
                for metadata in results["metadatas"]:
                    section_meta = metadata.copy()
                    if "metadata_json" in section_meta:
                        section_meta["metadata"] = json.loads(
                            section_meta["metadata_json"]
                        )
                        del section_meta["metadata_json"]
                    parsed_metadata.append(section_meta)
                return parsed_metadata
            return []
        except Exception as e:
            print(f"Error getting profile sections metadata: {e}")
            return []

    def clear_profile_data(self):
        """Clear all profile data from both collections"""
        try:
            self.client.delete_collection("profile_metadata")
            self.client.delete_collection("profile_content")
            # Recreate collections
            self.profile_metadata = self._create_collection("profile_metadata")
            self.profile_content = self._create_collection("profile_content")
        except Exception as e:
            print(f"Error clearing profile data: {e}")
