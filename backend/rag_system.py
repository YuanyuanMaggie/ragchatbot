import os
from typing import Dict, List, Optional, Tuple

from ai_generator import AIGenerator
from models import ProfileChunk, ProfileSection
from profile_document_processor import ProfileDocumentProcessor
from profile_search_tools import ProfileSearchTool, ProfileSummaryTool
from search_tools import ToolManager
from session_manager import SessionManager
from vector_store import VectorStore


class RAGSystem:
    """Main orchestrator for the Retrieval-Augmented Generation system"""

    def __init__(self, config):
        self.config = config

        # Initialize core components
        self.profile_document_processor = ProfileDocumentProcessor(
            chunk_size=700, chunk_overlap=100
        )
        self.vector_store = VectorStore(
            config.CHROMA_PATH, config.EMBEDDING_MODEL, config.MAX_RESULTS
        )
        self.ai_generator = AIGenerator(
            config.ANTHROPIC_API_KEY, config.ANTHROPIC_MODEL
        )
        self.session_manager = SessionManager(config.MAX_HISTORY)

        # Initialize profile search tools
        self.tool_manager = ToolManager()
        self.profile_search_tool = ProfileSearchTool(self.vector_store)
        self.profile_summary_tool = ProfileSummaryTool(self.vector_store)

        # Register profile tools
        self.tool_manager.register_tool(self.profile_search_tool)
        self.tool_manager.register_tool(self.profile_summary_tool)

    def query(
        self, query: str, session_id: Optional[str] = None
    ) -> Tuple[str, List[str], List[str]]:
        """
        Process a user query using the RAG system with tool-based search.

        Args:
            query: User's question
            session_id: Optional session ID for conversation context

        Returns:
            Tuple of (response, sources list, source_links list)
        """
        # Create prompt for the AI - the system prompt handles context
        prompt = query

        # Get conversation history if session exists
        history = None
        if session_id:
            history = self.session_manager.get_conversation_history(session_id)

        # Generate response using AI with tools
        response = self.ai_generator.generate_response(
            query=prompt,
            conversation_history=history,
            tools=self.tool_manager.get_tool_definitions(),
            tool_manager=self.tool_manager,
        )

        # Get sources and source links from the search tool
        sources = self.tool_manager.get_last_sources()
        source_links = self.tool_manager.get_last_source_links()

        # Reset sources after retrieving them
        self.tool_manager.reset_sources()

        # Update conversation history
        if session_id:
            self.session_manager.add_exchange(session_id, query, response)

        # Return response with sources and links from tool searches
        return response, sources, source_links

    def add_profile_document(self, file_path: str) -> Tuple[int, int]:
        """
        Add a single profile document (Markdown or JSON) to the knowledge base.

        Args:
            file_path: Path to the profile document

        Returns:
            Tuple of (number of sections created, number of chunks created)
        """
        try:
            # Process the document
            sections, chunks = self.profile_document_processor.process_profile_document(
                file_path
            )

            # Add profile sections to vector store for semantic search
            for section in sections:
                self.vector_store.add_profile_section(section)

            # Add profile content chunks to vector store
            self.vector_store.add_profile_content(chunks)

            return len(sections), len(chunks)
        except Exception as e:
            print(f"Error processing profile document {file_path}: {e}")
            return 0, 0

    def add_profile_folder(
        self, folder_path: str, clear_existing: bool = False
    ) -> Tuple[int, int]:
        """
        Add all profile documents from a folder.

        Args:
            folder_path: Path to folder containing profile documents
            clear_existing: Whether to clear existing profile data first

        Returns:
            Tuple of (total sections added, total chunks created)
        """
        total_sections = 0
        total_chunks = 0

        # Clear existing data if requested
        if clear_existing:
            print("Clearing existing profile data for fresh rebuild...")
            self.vector_store.clear_profile_data()

        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist")
            return 0, 0

        # Process each file in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith(
                (".md", ".json")
            ):
                try:
                    sections, chunks = self.add_profile_document(file_path)
                    total_sections += sections
                    total_chunks += chunks
                    print(
                        f"Added profile document: {file_name} ({sections} sections, {chunks} chunks)"
                    )
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")

        return total_sections, total_chunks

    def get_profile_analytics(self) -> Dict:
        """Get analytics about the profile knowledge base"""
        all_sections = self.vector_store.get_all_profile_sections()

        # Count sections by type
        section_counts = {}
        for section in all_sections:
            stype = section.get("section_type", "general")
            section_counts[stype] = section_counts.get(stype, 0) + 1

        # Get key highlights
        highlights = []

        # Add role count
        role_count = section_counts.get("role", 0)
        if role_count > 0:
            highlights.append(f"{role_count} work experience entries")

        # Add project count
        project_count = section_counts.get("project", 0)
        if project_count > 0:
            highlights.append(f"{project_count} key projects")

        # Add skill categories
        skill_count = section_counts.get("skill", 0)
        if skill_count > 0:
            highlights.append(f"{skill_count} skill categories")

        return {
            "total_sections": len(all_sections),
            "section_types": list(section_counts.keys()),
            "section_counts": section_counts,
            "key_highlights": highlights,
        }
