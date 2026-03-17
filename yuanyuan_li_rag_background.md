# RAG Background Document — Yuanyuan Li

## Purpose
This document is a first-pass knowledge seed for building a personal RAG chatbot for **Yuanyuan Li (also goes by Maggie / YY)**. It is designed to help a chatbot answer questions about Yuanyuan’s background, work history, technical strengths, leadership scope, project themes, and communication style.

It combines:
- **Public website signals** from yuanyuanli.com
- **Context from prior chats** with Yuanyuan
- **Proposed structure** for chunking, metadata, and retrieval

> This is a draft foundation document, not a final source of truth. Anything marked *confirm* should be reviewed and updated by Yuanyuan.

## 1) Canonical identity
**Name:** Yuanyuan Li  
**Also goes by:** Maggie, YY  
**Primary professional brand:** Engineering leader with a rare mix of full-stack product engineering, data platform leadership, and hands-on applied AI / developer tooling interest.  
**Location context:** U.S.-based; frequently references New York / New Jersey context in planning and work-life logistics.  
**Languages:** English and Chinese; often requests bilingual phrasing or translation support.

## 2) Executive summary
Yuanyuan Li is an engineering leader whose background spans **frontend engineering, full-stack product development, and data platform leadership**. Publicly, her website describes her as a **VP of Software Engineering with 7+ years at Two Sigma (Venn)** and says she **built and led a full-stack and data engineering team from the ground up**. [Website-derived facts in this document come from public snippets on yuanyuanli.com, including: VP of Software Engineering with 7+ years at Two Sigma (Venn), built and led a full-stack and data engineering team from the ground up, and portfolio project pages covering GiveNext, MERID, Cornell Feline Health Center, and an HCI project for Cornell students with diet restrictions.]

From prior chats, Yuanyuan appears strongest at the intersection of:
- data infrastructure
- investment / analytics domain systems
- cross-functional product delivery
- engineering management
- structured communication
- turning ambiguous business needs into concrete technical plans

She is unusually effective in both **strategy and execution**: writing roadmaps and PRDs, managing teams, designing data systems, reviewing legal/HR language, drafting stakeholder communication, and still going deep on implementation details such as Athena SQL, ETL architecture, AWS services, schema design, CI/CD, and debugging.

## 3) Short professional narrative
A concise way to describe Yuanyuan:

> Yuanyuan Li is a software engineering leader with roots in frontend and product engineering who expanded into backend, data infrastructure, and engineering management. At Venn / Two Sigma, she helped build product and data capabilities from an early-stage environment into a more mature platform, with particular depth in ingestion pipelines, investment analytics data, API strategy, and cross-functional execution.

## 4) Public website highlights
The public website suggests the following high-confidence facts:

### Current / recent positioning
- Described as **VP of Software Engineering**
- Has **7+ years at Two Sigma (Venn)**
- Built and led a **full-stack and data engineering team from the ground up** [Website-derived facts in this document come from public snippets on yuanyuanli.com, including: VP of Software Engineering with 7+ years at Two Sigma (Venn), built and led a full-stack and data engineering team from the ground up, and portfolio project pages covering GiveNext, MERID, Cornell Feline Health Center, and an HCI project for Cornell students with diet restrictions.]

### Portfolio themes on the site
The site includes project pages indicating experience in:
- **GiveNext** / charitable giving product work [Website-derived facts in this document come from public snippets on yuanyuanli.com, including: VP of Software Engineering with 7+ years at Two Sigma (Venn), built and led a full-stack and data engineering team from the ground up, and portfolio project pages covering GiveNext, MERID, Cornell Feline Health Center, and an HCI project for Cornell students with diet restrictions.]
- **MERID** software engineering work involving a **video hosting and file system component** [Website-derived facts in this document come from public snippets on yuanyuanli.com, including: VP of Software Engineering with 7+ years at Two Sigma (Venn), built and led a full-stack and data engineering team from the ground up, and portfolio project pages covering GiveNext, MERID, Cornell Feline Health Center, and an HCI project for Cornell students with diet restrictions.]
- **Cornell Feline Health Center** iOS development [Website-derived facts in this document come from public snippets on yuanyuanli.com, including: VP of Software Engineering with 7+ years at Two Sigma (Venn), built and led a full-stack and data engineering team from the ground up, and portfolio project pages covering GiveNext, MERID, Cornell Feline Health Center, and an HCI project for Cornell students with diet restrictions.]
- An HCI project for **Cornell students with diet restrictions** [Website-derived facts in this document come from public snippets on yuanyuanli.com, including: VP of Software Engineering with 7+ years at Two Sigma (Venn), built and led a full-stack and data engineering team from the ground up, and portfolio project pages covering GiveNext, MERID, Cornell Feline Health Center, and an HCI project for Cornell students with diet restrictions.]

### What this implies for retrieval
A good chatbot should understand that Yuanyuan’s background is **not only data engineering**. It should also know she has history in:
- product/UI work
- academic/team project collaboration
- mobile or app development exposure
- human-centered design / usability-oriented work

## 5) Professional background from prior chats
The following themes come from prior conversations and should be treated as **user-confirmed working context** unless Yuanyuan wants edits.

### 5.1 Leadership and scope
Yuanyuan is an engineering manager / senior engineering leader who has:
- led the **Data Platform Team** at Venn Engineering
- owned quarterly roadmap planning for her team
- collaborated on yearly engineering roadmap work
- mentored engineers and supported promotions / performance reviews
- worked closely with product, quant, business stakeholders, and senior leadership

### 5.2 Domain expertise
Strong recurring domain areas include:
- investment data onboarding
- portfolio / holdings / returns ingestion
- factor models and factor analytics
- risk and performance analytics
- advisor / client onboarding workflows
- vendor data integration for financial products

### 5.3 Common business context
Her work often involves translating business or client needs into data platform capabilities, such as:
- new data sources
- onboarding pipelines
- file format specifications
- APIs for analytics or integration
- incident response and data quality improvement
- scalable ingestion and historical data support

## 6) Technical expertise map
A RAG chatbot should be able to associate Yuanyuan with the following technical areas.

### Data & platform
- ETL / ELT pipelines
- batch and stream ingestion
- relational storage and data lakes
- schema design and data contracts
- data quality checks and monitoring
- metadata-driven ingestion workflows
- vendor file processing and normalization

### Cloud & infrastructure
- AWS (especially S3, Athena, Glue, Lambda, Step Functions, and related tooling)
- CI/CD and deployment workflows
- operational debugging and production support
- lifecycle / storage management for large data sets

### Product & application engineering
- frontend engineering foundations
- React / JavaScript / TypeScript familiarity
- backend/API collaboration
- designing for stakeholder usability and client workflows

### Applied AI / engineering productivity
Based on prior chats, Yuanyuan is highly interested in:
- LLM-assisted engineering workflows
- AI for developer productivity
- RAG-like systems for internal knowledge or data QA
- structured prompting and tool use
- agent-style workflows such as bots for Athena queries or GitLab automation

## 7) Example project clusters the bot should understand
Instead of storing dozens of project names without structure, organize knowledge into reusable project clusters.

### Cluster A — Data ingestion and onboarding
Representative themes:
- integrating third-party partner data
- client uploads through API or SFTP
- transforming external data into internal product-ready models
- handling file specs, timestamp rules, and operational edge cases

### Cluster B — Investment analytics and factor data
Representative themes:
- factor model pipeline maintenance
- vendor migrations for factor or style data
- risk analytics outputs for investors
- index and forecast data integration

### Cluster C — Platform reliability and incident management
Representative themes:
- data incident management process improvements
- review groups / retrospectives
- quality and performance improvements
- better client communication around incidents

### Cluster D — API and product platform expansion
Representative themes:
- analytics APIs
- factor APIs
- integration APIs
- commercialization / productization of platform capabilities

### Cluster E — Early-stage full-stack product building
Representative themes:
- startup-style product building
- frontend architecture and UX improvements
- end-to-end feature delivery
- close partnership with product, design, marketing, sales, and clients

## 8) Working style and communication style
This section is especially useful for a personal chatbot because it helps tone-match.

### Working style
Yuanyuan tends to be:
- highly structured
- detail-oriented
- execution-focused
- pragmatic under constraints
- thoughtful about business impact
- proactive in planning and follow-through

### Communication preferences
The assistant should expect that Yuanyuan often prefers outputs that are:
- ready to paste into Slack / email / docs / JIRA
- clearly structured with sections
- concise but concrete
- polished and professional
- actionable rather than abstract
- sometimes bilingual or easy to translate

### Common output formats she likes
- bullet-point summaries
- one-pagers
- roadmap / PRD outlines
- JIRA ticket templates with AC / tasks
- SQL or Python snippets
- tables with clear headers
- speech notes for presentations
- email drafts and stakeholder messages

## 9) Personal context the bot may optionally know
This section should live in a **private collection** and should be removable if Yuanyuan wants a more work-only bot.

Suggested private-but-useful context:
- She is family-oriented and balances senior technical leadership with parenting responsibilities.
- She often plans carefully across work, travel, childcare, and household logistics.
- She has a dog named Ruby.
- She frequently uses ChatGPT as both a technical copilot and a life admin assistant.

Do **not** over-index on private life in normal answers unless the user’s question is explicitly personal.

## 10) What the chatbot should be able to answer well
A good Yuanyuan chatbot should answer questions like:
- What is Yuanyuan’s professional background?
- How did she move from frontend / full-stack work into data platform leadership?
- What domains has she worked in at Venn / Two Sigma?
- What kinds of data systems has she built or led?
- What is her management and leadership style?
- What tools and platforms does she commonly use?
- What kinds of projects best represent her experience?
- How should a message or bio be written in her voice?
- What are recurring themes in her technical work?

## 11) What the chatbot should avoid doing
The chatbot should not:
- invent exact dates, titles, or metrics that are not grounded in source material
- state personal or sensitive facts unless they are intentionally included in a private knowledge base
- overfit to only one identity (for example: “only a data engineer” or “only a manager”)
- answer legal, HR, compensation, or family questions with certainty unless the supporting documents are actually indexed

## 12) Recommended RAG source collections
Use separate collections instead of one giant mixed corpus.

### Collection 1 — Public profile
Sources:
- personal website
- resume
- LinkedIn export
- public portfolio pages
- talk abstracts / public writing

Use for:
- bios
- recruiter questions
- interview prep
- public-facing summaries

### Collection 2 — Work knowledge (private)
Sources:
- project docs
- PRDs
- architecture notes
- roadmap docs
- performance review notes
- presentations
- meeting notes that are safe to index

Use for:
- internal project recall
- detailed accomplishment summaries
- examples for interviews
- leadership narratives

### Collection 3 — Personal operating context (private, optional)
Sources:
- preferred writing samples
- travel templates
- life admin templates
- family scheduling notes
- repeated personal preferences

Use for:
- drafting in her voice
- personalized planning help
- recurring routines and preferences

## 13) Chunking and metadata suggestions
Each chunk should carry metadata like:
- `source_type`: website / resume / performance_review / project_doc / email_draft / presentation / note
- `topic`: leadership / data-platform / factor-model / api / onboarding / incident-management / personal-brand
- `time_period`: e.g. 2016, 2024-Q3, 2025
- `visibility`: public / private / restricted
- `confidence`: verified / inferred / draft-to-confirm
- `audience`: recruiter / hiring-manager / teammate / self / family

Recommended chunk sizes:
- 300–700 words for narrative docs
- smaller chunks for project bullets or bios
- preserve section headers during splitting

## 14) Canonical entities and aliases
Useful aliases for retrieval:
- `Yuanyuan Li`
- `Maggie`
- `YY`
- `Venn`
- `Two Sigma`
- `Data Platform Team`
- `Factor API`
- `Analytics API`
- `Integration API`
- `RCM`
- `Addepar`
- `FactSet`
- `Morningstar`
- `Axioma`
- `AWS`
- `Athena`
- `Glue`
- `Step Functions`

## 15) Seed Q&A pairs for evaluation
### Q1
**Question:** Give me a short professional bio for Yuanyuan Li.
**Good answer should include:** engineering leader, full-stack + data platform background, Venn / Two Sigma, cross-functional execution, investment analytics/data domain.

### Q2
**Question:** What makes Yuanyuan different from a typical data engineering manager?
**Good answer should include:** frontend/product roots, end-to-end product sense, leadership plus hands-on technical depth, strong communication and planning discipline.

### Q3
**Question:** What kinds of projects has Yuanyuan led?
**Good answer should include:** ingestion pipelines, analytics APIs, factor/risk data work, incident management improvements, onboarding and integration systems.

### Q4
**Question:** How should I draft a message in Yuanyuan’s style?
**Good answer should include:** structured, direct, polite, concrete, easy to paste, business-aware, minimal fluff.

### Q5
**Question:** What should I be careful about when answering questions about Yuanyuan?
**Good answer should include:** do not hallucinate dates/metrics; distinguish public vs private facts; avoid oversharing personal context; clarify uncertain items.

## 16) Suggested system prompt guidance
You are a personal assistant for Yuanyuan Li. Represent her background accurately and conservatively. Prefer grounded answers over impressive-sounding ones. When discussing her career, reflect both her product/full-stack roots and her later data platform leadership. Separate public facts from private context. When uncertain, say what is known, what is inferred, and what still needs confirmation.

## 17) Open questions to improve the bot
These are the highest-value gaps to fill next:
1. What exact headline does Yuanyuan want as her canonical current title?
2. Which achievements are safe to state publicly with metrics?
3. Which resume / LinkedIn version is the source of truth?
4. Which private docs should be indexed first: resume, self-reviews, PRDs, slide decks, or project docs?
5. Should the bot include personal life context, or stay mostly career-focused?
6. What tone modes should exist: recruiter-ready, manager-ready, casual, executive, bilingual?
7. Which topics are off-limits or require extra caution?

## 18) Recommended next ingestion set
Best immediate files to add for a much stronger bot:
1. latest resume
2. LinkedIn profile export or copy
3. “tell me about yourself” interview answer
4. 3–5 representative project docs or one-pagers
5. recent performance review / self-review
6. a few polished emails or docs that reflect her writing voice

---

## One-line summary for builders
**Yuanyuan Li is a product-minded engineering leader who evolved from frontend/full-stack development into data platform leadership, with deep strength in investment data systems, cross-functional delivery, structured communication, and practical AI-enabled engineering workflows.**
