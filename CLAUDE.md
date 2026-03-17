# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Quick start using shell script
chmod +x run.sh
./run.sh

# Manual start
cd backend && uv run uvicorn app:app --reload --port 8000
```

### Environment Setup
```bash
# Python version requirement: >= 3.13 (specified in pyproject.toml)

# Install dependencies
uv sync

# Add new dependencies (use uv instead of pip)
uv add package_name

# Environment variables required
# Create .env file with:
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### Python Execution
Always use `uv` for running Python files and commands:
```bash
# Run Python scripts
uv run python script.py

# Run any Python command
uv run command_name
```

### Code Quality Tools

#### Prerequisites
Install development dependencies before using code quality tools:
```bash
uv sync --group dev
```

#### Available Scripts

**Format Script (Modifies Files)**
```bash
./scripts/format.sh
```
Use this script when you want to automatically fix code style issues. It will:
1. Sort imports with isort
2. Format code with Black 
3. Run flake8 linting (reports remaining issues)
4. Run mypy type checking

**Lint Script (Read-Only Checks)**
```bash
./scripts/lint.sh
```
Use this script to verify code quality without modifying files. Perfect for:
- Pre-commit checks
- CI/CD pipelines
- Verifying code before submitting PRs

Exit code 0 = all checks pass, non-zero = issues found.

#### Troubleshooting
If scripts aren't executable: `chmod +x scripts/*.sh`

### Application Access
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Testing

The project uses pytest for testing. Currently available tests:

**Run all tests:**
```bash
uv run pytest
```

**Run specific test file:**
```bash
uv run pytest backend/tests/test_config.py
```

**Run tests with coverage:**
```bash
uv run pytest --cov=backend --cov-report=html
```

**Current test coverage:**
- `backend/tests/test_config.py` - Configuration validation tests

**Note:** Profile-specific tests (RAG system, search tools, API endpoints) are planned for future implementation.

## Architecture Overview

This is a Retrieval-Augmented Generation (RAG) system for Yuanyuan Li's personal profile with a FastAPI backend and vanilla JavaScript frontend.

### Core Components

**RAGSystem (backend/rag_system.py)**: Main orchestrator that coordinates all components
- Manages document processing, vector storage, AI generation, and search tools
- Handles profile document ingestion (Markdown and JSON files)
- Processes queries using tool-based search approach

**VectorStore (backend/vector_store.py)**: ChromaDB-based vector storage with dual collections
- `profile_metadata`: Stores profile sections (roles, projects, skills, education)
  - Metadata: section_type, title, timeframe, company, category, metadata_json
- `profile_content`: Stores searchable text chunks
  - Metadata: section_type, section_title, chunk_index, timeframe, company, category
- Supports filtered search by section type, timeframe, and company

**ProfileDocumentProcessor (backend/profile_document_processor.py)**: Document processing
- Processes JSON profile file (yuanyuan_li_profile.json)
- Handles structured profile data: roles, projects, skills, education, canonical story
- Smart chunking with context preservation (800 char chunks, 100 char overlap)
- Extracts metadata automatically (company, timeframe, technologies)

**AIGenerator (backend/ai_generator.py)**: Anthropic Claude API integration
- Uses claude-sonnet-4-20250514 model
- Personal assistant system prompt for Yuanyuan Li
- Implements tool calling for profile search functionality
- Maintains conversation history via SessionManager

**SessionManager (backend/session_manager.py)**: Conversation state management
- Tracks conversation history per session
- Manages message pairs (user/assistant)
- Limits history to configurable max (default: 5 exchanges)
- Provides session creation, message storage, and clearing

**Profile Search Tools (backend/profile_search_tools.py)**: Tool-based search system
- ProfileSearchTool: Search with filters for company, timeframe, section type
- ProfileSummaryTool: Get structured summaries of roles, projects, skills
- ToolManager: Manages tool registration and execution for AI model

### API Endpoints

**POST /api/query**: Submit a question and get AI-generated response
- Request: `{ query: str, session_id?: str }`
- Response: `{ answer: str, sources: List[str], source_links: List[str], session_id: str }`

**GET /api/profile-stats**: Get profile statistics
- Response: `{ total_sections: int, section_types: List[str], key_highlights: List[str] }`

**POST /api/clear-session**: Clear conversation history for a session
- Request: `{ session_id: str }`
- Response: `{ status: str, message: str }`

### Data Flow
1. Profile document (yuanyuan_li_profile.json) is loaded on startup
2. ProfileDocumentProcessor chunks content and extracts profile metadata
3. VectorStore stores both metadata and content in separate ChromaDB collections
4. User queries trigger AI generation with access to profile search tools
5. AI uses ProfileSearchTool/ProfileSummaryTool to find relevant information
6. Frontend displays responses with source attribution (section, company, timeframe)

### Key Configuration (backend/config.py)
- Profile chunk size: 800 characters with 100 character overlap
- Embedding model: all-MiniLM-L6-v2 (SentenceTransformers)
- Max search results: 5 per query
- Conversation history: 2 message pairs

### Frontend Architecture
- Single-page application with vanilla JavaScript
- Real-time profile statistics display
- Markdown rendering support for AI responses
- Responsive design with sidebar for profile overview and suggested queries
- Dark/light theme toggle

## Development Notes

- The system automatically loads yuanyuan_li_profile.json from root directory on startup
- ChromaDB data persists in backend/chroma_db/
- FastAPI serves both API endpoints (/api/*) and static frontend files
- CORS is configured for development with broad permissions
- No-cache headers are set for static files during development
- Profile data includes: roles, projects, skills, education, canonical story, and comprehensive metadata