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

This is a simplified RAG system for Yuanyuan Li's personal profile. The entire profile (~37KB, 1,500 tokens) is loaded into Claude's context, eliminating the need for vector search.

### Core Components

**RAGSystem (backend/rag_system.py)**: Main orchestrator
- Loads full profile JSON on initialization
- Converts profile to readable text format
- Passes complete profile to Claude in system prompt
- Manages conversation sessions

**AIGenerator (backend/ai_generator.py)**: Anthropic Claude API integration
- Uses claude-sonnet-4-20250514 model
- Full profile loaded in system prompt (~1,500 tokens)
- No tool calling needed - Claude has complete context
- Maintains conversation history via SessionManager

**SessionManager (backend/session_manager.py)**: Conversation state management
- Tracks conversation history per session
- Manages message pairs (user/assistant)
- Limits history to configurable max (default: 2 exchanges)
- Provides session creation, message storage, and clearing

**Why No Vector Database?**
- Profile is only 37KB (~1,500 tokens)
- Claude's context window is 200,000 tokens
- Profile uses < 1% of available context
- Benefits: 50% faster, 60% smaller package, simpler code

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
2. RAGSystem converts JSON to readable text format
3. Full profile text is passed to Claude in system prompt
4. User queries are sent directly to Claude with complete context
5. Claude generates responses using full profile knowledge
6. API returns responses with source attribution

### Key Configuration (backend/config.py)
- Profile path: ../yuanyuan_li_profile.json
- Claude model: claude-haiku-4-5-20251001
- Conversation history: 2 message pairs
- Lambda memory: 512MB (production)

## Development Notes

- The system automatically loads yuanyuan_li_profile.json on startup
- Full profile is loaded into memory (~7KB text, 1,500 tokens)
- FastAPI serves API endpoints (/api/*)
- CORS is configured for development
- Profile data includes: roles, projects, skills, education, canonical story

## Deployment

- **Local**: `uv run uvicorn backend.app:app --reload --port 8000`
- **Lambda**: `sam build && sam deploy` (uses template.yaml)