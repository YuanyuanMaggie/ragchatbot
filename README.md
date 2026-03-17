# Yuanyuan Li - Personal Profile RAG Chatbot

A personal assistant powered by RAG (Retrieval-Augmented Generation) that answers questions about Yuanyuan Li's professional background, experience, and expertise.

## 🎯 What This Does

This chatbot can answer questions like:
- "Tell me about yourself"
- "What data systems have you built?"
- "What's your experience with AWS?"
- "What is your leadership style?"
- "What makes you different from typical data engineering managers?"

It provides accurate, grounded responses with proper source attribution.

## ✨ Key Features

- **Accurate & Grounded**: All responses based on source documents, no hallucination
- **Rich Source Attribution**: Sources include company, timeframe, and context
- **Privacy-Aware**: Respects boundaries, doesn't speculate on personal matters
- **Professional Tone**: Suitable for recruiters, hiring managers, or colleagues
- **Intelligent Search**: Filters by company, timeframe, technology, or section type
- **Conversation History**: Multi-turn conversations with context

## 📚 Knowledge Base

The system loads one comprehensive profile document on startup:

**yuanyuan_li_profile.json** - Combined comprehensive profile
   - Structured profile data: roles, projects, skills, education
   - Narrative content: tell-me-about-yourself, short bio, career arc
   - Domain expertise and project themes
   - Leadership and working style
   - Communication preferences
   - 3 work experience entries (Two Sigma, Jet.com, SupplyHouse)
   - 12+ key projects with metadata

**Total Knowledge:** 75+ sections, 270+ searchable chunks

## 🚀 Quick Start

### 1. Prerequisites

- Python environment with `uv` installed
- Anthropic API key
- yuanyuan_li_profile.json in root directory

### 2. Set API Key

Create `.env` file in project root:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. Start Server

```bash
./run.sh
```

### 4. Open Browser

Navigate to: http://localhost:8000

## 📖 Documentation

- **[START_SERVER.md](START_SERVER.md)** - Server startup guide with troubleshooting
- **[QUICK_START.md](QUICK_START.md)** - Quick testing guide with example queries
- **[REFACTOR_PLAN.md](REFACTOR_PLAN.md)** - Complete refactoring plan
- **[TEST_PLAN.md](TEST_PLAN.md)** - Comprehensive testing strategy
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - Implementation summary
- **[BEFORE_AFTER.md](BEFORE_AFTER.md)** - Comparison with course bot
- **[CLAUDE.md](CLAUDE.md)** - Development commands and architecture

## 🧪 Test Queries

Try these queries to test the system:

### Basic
- "Tell me about yourself"
- "Give me a short professional bio"
- "What is your background?"

### Technical
- "What data systems have you built?"
- "What's your experience with AWS?"
- "What programming languages do you know?"

### Projects
- "Tell me about the Factor API project"
- "What projects did you work on in 2024?"
- "Show me your analytics API work"

### Leadership
- "What is your leadership style?"
- "How do you build and mentor teams?"
- "Describe your management experience"

### Unique Strengths
- "What makes you different from typical data engineering managers?"
- "What's unique about your background?"

## 🏗️ Architecture

```
Profile Documents (Markdown + JSON)
         ↓
ProfileDocumentProcessor
    ↓               ↓
ProfileSection  ProfileChunk
    ↓               ↓
profile_metadata  profile_content (ChromaDB)
         ↓
ProfileSearchTool / ProfileSummaryTool
         ↓
AI Generator (Claude with personal assistant prompt)
         ↓
RAG System → FastAPI → Frontend
```

## 🔧 Technology Stack

**Backend:**
- FastAPI - Web framework
- ChromaDB - Vector database
- Anthropic Claude - AI model
- SentenceTransformers - Embeddings
- Python 3.11+

**Frontend:**
- Vanilla JavaScript
- Marked.js - Markdown rendering
- Modern CSS with dark/light themes

**Infrastructure:**
- uv - Package manager
- Uvicorn - ASGI server

## 📂 Project Structure

```
ragchatbot-codebase-main/
├── backend/
│   ├── app.py                          # FastAPI application
│   ├── rag_system.py                   # Main RAG orchestrator
│   ├── profile_document_processor.py   # Document processing
│   ├── profile_search_tools.py         # Search tools
│   ├── vector_store.py                 # ChromaDB interface
│   ├── ai_generator.py                 # Claude API integration
│   ├── models.py                       # Data models
│   └── ...
├── frontend/
│   ├── index.html                      # Main UI
│   ├── script.js                       # Frontend logic
│   └── style.css                       # Styling
├── yuanyuan_li_profile.json            # Comprehensive profile (combines narrative + structured data)
├── .env                                # API keys (not in repo)
├── run.sh                              # Startup script
└── README_PROFILE.md                   # This file
```

## 🎨 UI Features

- **Dark/Light Theme**: Toggle with button or Ctrl+Shift+T
- **Profile Overview**: Sidebar with section counts and highlights
- **Suggested Queries**: Click to quickly ask common questions
- **Source Attribution**: Collapsible sources with company/timeframe context
- **Conversation History**: Multi-turn conversations
- **New Chat**: Start fresh conversation anytime
- **Markdown Support**: Formatted responses with lists, bold, code

## 🔒 Privacy & Safety

- ✅ Only uses information explicitly in knowledge base
- ✅ Never hallucinates dates, metrics, or facts
- ✅ Respects privacy boundaries (no speculation on personal/family/financial)
- ✅ Clear distinction between verified and inferred information
- ✅ Professional, accurate responses suitable for any audience

## 📊 API Endpoints

- `POST /api/query` - Submit query and get response
- `GET /api/profile-stats` - Get profile statistics
- `POST /api/clear-session` - Clear conversation history

## 🧑‍💻 Development

### Install Dependencies
```bash
uv sync
```

### Run Tests (when available)
```bash
uv run pytest
```

### Format Code
```bash
./scripts/format.sh
```

### Lint Code
```bash
./scripts/lint.sh
```

## 🔄 Updating Profile

### Add New Information

1. **Edit the profile file:**
   - Edit `yuanyuan_li_profile.json`
   - Update roles, projects, skills, education, or canonical_story sections
   - Add new content following the existing JSON structure

2. **Reload:**
   - Restart the server to reload the updated profile

### Best Practices

- Use clear section headers
- Include timeframes and company names
- Tag with technologies used
- Keep chunks focused and atomic
- Maintain consistent metadata

## ❓ Troubleshooting

### Server Won't Start
See [START_SERVER.md](START_SERVER.md) for detailed troubleshooting.

Common issues:
- `uv` not in PATH → Install or use full path
- Port 8000 in use → Kill existing process
- API key missing → Create `.env` file
- Dependencies missing → Run `uv sync`

### Profile Not Loading
- Verify yuanyuan_li_profile.json exists in root directory
- Check file permissions
- Validate JSON syntax
- Look for errors in server logs

### Bad Responses
- Check source attribution
- Verify query matches knowledge base
- Try more specific questions
- Check conversation history isn't polluted

## 🚀 Production Deployment

For production use, consider:

1. **Security:**
   - Use environment variables for secrets
   - Enable HTTPS
   - Add authentication if needed

2. **Performance:**
   - Cache embeddings
   - Use persistent ChromaDB storage
   - Add rate limiting

3. **Monitoring:**
   - Log queries and responses
   - Track token usage
   - Monitor response times

## 📈 Future Enhancements

Potential improvements:
- [ ] Add more profile documents (resume, reviews, presentations)
- [ ] Implement unit and integration tests
- [ ] Add conversation modes (recruiter, technical, executive)
- [ ] Support bilingual responses (English/Chinese)
- [ ] "Draft in her voice" capability
- [ ] Export conversations to PDF
- [ ] Analytics dashboard for queries

## 🤝 Contributing

This is a personal project, but suggestions are welcome:
1. Open an issue for bugs or feature requests
2. Submit PRs for improvements
3. Follow existing code style
4. Add tests for new features

## 📄 License

Private project - not licensed for public use.

## 👤 About

This personal profile assistant was built to accurately represent Yuanyuan Li's professional background using state-of-the-art RAG technology. It's designed to help recruiters, hiring managers, and colleagues learn about her experience, skills, and unique strengths.

**Built with:** Claude 4.5, FastAPI, ChromaDB, and modern web technologies.

---

**Questions or Issues?**
- See [START_SERVER.md](START_SERVER.md) for startup help
- See [QUICK_START.md](QUICK_START.md) for testing guide
- Check [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) for technical details

✨ **Your professional profile, powered by AI** ✨
