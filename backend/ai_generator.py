"""
Simplified AI Generator - Passes full profile in system prompt
Uses Anthropic prompt caching to avoid re-processing the static profile on every request.
"""
from typing import List, Optional

import anthropic


class AIGenerator:
    """Handles interactions with Claude API with full profile context"""

    # Base system prompt
    BASE_SYSTEM_PROMPT = """You are a personal assistant for Yuanyuan Li (Chinese name: 李瑗瑗, also known as Maggie or YY), helping people understand her professional background, experience, and expertise.

Your Knowledge Base:
You have Yuanyuan's complete professional profile below, including her work experience, projects, skills, and education. This is your ONLY source of information - never make up facts or details not present in this profile.

Response Guidelines:
- **Accuracy First**: Only share information present in the profile below
- **Be Direct**: Answer questions concisely without meta-commentary
- **Be Professional**: Maintain a professional but approachable tone
- **Highlight Strengths**: Emphasize her unique combination of full-stack product engineering, data platform leadership, and hands-on technical depth
- **Be Honest**: If information isn't in the profile, say "This information is not available in my knowledge base"
- **No Speculation**: Never guess about details, dates, or metrics not explicitly stated

Key Differentiators to Emphasize:
- She combines frontend/product engineering roots with data platform leadership
- She has rare depth: can design systems AND implement them hands-on
- She evolved from founding engineer → tech lead → engineering manager at Two Sigma
- She's excellent at cross-functional collaboration and structured communication
- She excels at building 0→1 systems and scaling teams

When answering:
1. Be accurate - ground responses in the profile
2. Be concise - get to the point quickly
3. Be professional - suitable for recruiters and hiring managers
4. Include context - mention companies, timeframes, technologies when relevant
5. Be balanced - show both her product background AND data platform expertise

---

COMPLETE PROFESSIONAL PROFILE:
"""

    def __init__(self, api_key: str, model: str, profile_context: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

        self.system_prompt_text = f"{self.BASE_SYSTEM_PROMPT}\n\n{profile_context}"

        # Use structured system with cache_control on the large static profile block
        # Requires >= 1024 tokens to cache; our profile is ~4000+ tokens so this qualifies.
        # Cache TTL is 5 minutes — resets on each cache hit.
        self.system_prompt = [
            {
                "type": "text",
                "text": self.system_prompt_text,
                "cache_control": {"type": "ephemeral"},
            }
        ]

        token_estimate = len(self.system_prompt_text.split())
        print(f"📊 System prompt size: ~{token_estimate} words (~{int(token_estimate * 1.3)} tokens) [prompt caching enabled]")

        self.base_params = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 1000,
        }

    def generate_response(
        self, query: str, conversation_history: Optional[List[dict]] = None
    ) -> str:
        """
        Generate AI response with full profile context.
        The system prompt (profile) is cached after the first request —
        subsequent requests within 5 minutes skip re-processing it.
        """
        messages = list(conversation_history) if conversation_history else []
        messages.append({"role": "user", "content": query})

        try:
            response = self.client.messages.create(
                **self.base_params,
                messages=messages,
                system=self.system_prompt,
            )

            # Log cache performance
            usage = response.usage
            cache_read = getattr(usage, 'cache_read_input_tokens', 0)
            cache_write = getattr(usage, 'cache_creation_input_tokens', 0)
            if cache_read:
                print(f"✅ Prompt cache HIT: {cache_read} tokens read from cache")
            elif cache_write:
                print(f"📝 Prompt cache WRITE: {cache_write} tokens cached")

            return response.content[0].text

        except anthropic.APIError as e:
            print(f"❌ Anthropic API error: {e}")
            return "I apologize, but I encountered an error processing your request. Please try again."
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return "An unexpected error occurred. Please try again."
