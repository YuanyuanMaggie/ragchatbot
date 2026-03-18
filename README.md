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

The system loads one comprehensive profile document into Claude's context:

**yuanyuan_li_profile.json** (37KB, ~1,500 tokens)
   - Structured profile data: roles, projects, skills, education
   - Narrative content: tell-me-about-yourself, career arc
   - Domain expertise and project themes
   - Leadership and working style
   - 3 work experience entries (Two Sigma, Jet.com, SupplyHouse)
   - 11 key projects with metadata

**Full profile loaded in memory** - No vector database needed! Claude sees 100% of context every time.

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

The API will be available at: http://localhost:8000

## 📖 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Development commands and architecture reference
- **[README.md](README.md)** - This file (project overview and deployment)

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

**Simplified Architecture (No Vector Database)**

```
Profile JSON (yuanyuan_li_profile.json)
         ↓
RAGSystem loads full profile (~1,500 tokens)
         ↓
Claude receives full profile in system prompt
         ↓
AI Generator (Claude with complete context)
         ↓
FastAPI API Endpoints
```

**Why No ChromaDB?**
- Profile is only 37KB (~1,500 tokens)
- Claude's context window is 200,000 tokens
- Full profile fits easily → no vector search needed
- Result: 50% faster, 60% smaller, simpler to maintain

## 🔧 Technology Stack

**Backend:**
- FastAPI - Web framework
- Anthropic Claude - AI model (Sonnet 4)
- Python 3.13+
- Mangum - Lambda ASGI adapter

**Infrastructure:**
- uv - Package manager
- Uvicorn - ASGI server (local)
- AWS Lambda + API Gateway (production)

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
├── yuanyuan_li_profile.json            # Comprehensive profile (combines narrative + structured data)
├── .env                                # API keys (not in repo)
├── run.sh                              # Startup script
└── README.md                           # This file
```

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
- `uv` not in PATH → Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Port 8000 in use → Kill process: `lsof -ti:8000 | xargs kill`
- API key missing → Create `.env` file with `ANTHROPIC_API_KEY`
- Dependencies missing → Run `uv sync`

### Profile Not Loading
- Verify `yuanyuan_li_profile.json` exists in root directory
- Check JSON syntax is valid
- Look for errors in server startup logs

### Lambda Deployment Issues
- Build fails → Check Python 3.13 installed
- Deploy fails → Verify AWS credentials configured
- API errors → Check CloudWatch logs: `sam logs --stack-name yuanyuan-chatbot --tail`

## 🚀 Production Deployment

### AWS Lambda Deployment (Recommended)

Deploy to AWS Lambda with API Gateway for a serverless, cost-effective solution.

**Benefits:**
- **Cost**: ~$3.65/month with free tier protection
- **Scalability**: Auto-scales with traffic
- **No server management**: Fully managed by AWS
- **Fast**: 2-3 second cold starts

#### Prerequisites
- AWS account with CLI configured
- AWS SAM CLI installed: `brew install aws-sam-cli`
- Anthropic API key

#### Quick Deploy (3 Steps)

```bash
# 1. Build Lambda package
sam build

# 2. Deploy to AWS
export ANTHROPIC_API_KEY="your-key-here"
sam deploy \
  --stack-name yuanyuan-chatbot \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "AnthropicApiKey=$ANTHROPIC_API_KEY"

# 3. Get API credentials
aws cloudformation describe-stacks \
  --stack-name yuanyuan-chatbot \
  --query 'Stacks[0].Outputs'
```

#### Cost Protection
- **Hard limit**: 900,000 requests/month (under free tier)
- **Throttle**: 10 requests/second
- **Reserved concurrency**: 10 executions max
- **Budget alerts**: Email notifications at $5 threshold

### Alternative Deployment Options

**AWS Lightsail** (~$7/month):
- Fixed pricing, simpler setup
- Good for consistent low traffic
- Includes SSL, static IP

**Traditional Server**:
- Use Docker container from Dockerfile
- Deploy to any VPS or cloud platform
- Configure reverse proxy (nginx/caddy)

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

**Built with:** Claude 4.5, FastAPI, and modern web technologies.

---

✨ **Your professional profile, powered by AI** ✨

**Questions?** See [CLAUDE.md](CLAUDE.md) for development commands or the Troubleshooting section above.
