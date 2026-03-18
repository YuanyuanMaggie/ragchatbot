"""
Simplified AI Generator - Passes full profile in system prompt
No tools, no vector search, just direct context
"""
from typing import Optional

import anthropic


class AIGenerator:
    """Handles interactions with Claude API with full profile context"""

    # Base system prompt
    BASE_SYSTEM_PROMPT = """You are a personal assistant for Yuanyuan Li (also known as Maggie or YY), helping people understand her professional background, experience, and expertise.

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

        # Build complete system prompt with profile
        self.system_prompt = f"{self.BASE_SYSTEM_PROMPT}\n\n{profile_context}"

        # Check token count (approximately)
        token_estimate = len(self.system_prompt.split())
        print(f"📊 System prompt size: ~{token_estimate} words (~{int(token_estimate * 1.3)} tokens)")

        # Claude can handle up to 200k context, so even 10k words is fine
        if token_estimate > 150000:
            print("⚠️  Warning: System prompt is very large and may impact performance")

        # Base API parameters
        self.base_params = {
            "model": self.model,
            "temperature": 0,
            "max_tokens": 1000,
        }

    def generate_response(
        self, query: str, conversation_history: Optional[str] = None
    ) -> str:
        """
        Generate AI response with full profile context

        Args:
            query: The user's question or request
            conversation_history: Previous messages for context

        Returns:
            Generated response as string
        """
        # Add conversation history to system prompt if provided
        system_content = self.system_prompt
        if conversation_history:
            system_content = (
                f"{self.system_prompt}\n\n"
                f"--- Previous Conversation ---\n{conversation_history}\n"
                f"--- End Previous Conversation ---\n\n"
                f"Continue the conversation naturally, referring back to previous exchanges when relevant."
            )

        # Build messages
        messages = [{"role": "user", "content": query}]

        # Make API call
        try:
            response = self.client.messages.create(
                **self.base_params, messages=messages, system=system_content
            )

            return response.content[0].text

        except anthropic.APIError as e:
            print(f"❌ Anthropic API error: {e}")
            return "I apologize, but I encountered an error processing your request. Please try again."
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return "An unexpected error occurred. Please try again."
