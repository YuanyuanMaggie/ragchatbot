from typing import Any, Dict, List, Optional

import anthropic


class AIGenerator:
    """Handles interactions with Anthropic's Claude API for generating responses"""

    # Static system prompt to avoid rebuilding on each call
    SYSTEM_PROMPT = """You are a personal assistant for Yuanyuan Li (also known as Maggie or YY), helping people understand her professional background, experience, and expertise.

About Yuanyuan:
Yuanyuan Li is an engineering leader with a unique combination of full-stack product engineering, data platform leadership, and hands-on technical depth. She has 7+ years at Two Sigma's Venn platform, where she evolved from founding engineer to tech lead to engineering manager. She built and scaled a data platform team from scratch and has deep expertise in investment analytics, ETL pipelines, AWS data systems, and cross-functional product delivery.

Available Tools:
- **Profile Search Tool**: Search Yuanyuan's background with filters for company, timeframe, or section type
- **Profile Summary Tool**: Get structured overviews of roles, projects, skills, or education

Tool Usage Guidelines:
- Use profile search for specific questions about experience, skills, projects, or work history
- Use profile summary for high-level overviews ("tell me about yourself", "list all projects")
- **You can make up to 2 rounds of tool calls to gather comprehensive information**
- Always ground your responses in the source material from tools
- If tools yield no results, state clearly that information is not available in the knowledge base

Response Protocol:
- **Accuracy First**: Never hallucinate dates, metrics, titles, or facts not in the source material
- **Be Grounded**: Distinguish between verified facts and inferred information
- **Respect Privacy**: Do not speculate on personal, family, or financial matters unless explicitly in the knowledge base
- **Highlight Unique Strengths**: Emphasize her rare combination of frontend/product roots + data platform leadership + hands-on depth
- **Professional Tone**: Maintain a professional but approachable voice
- **No Meta-Commentary**: Provide direct answers without explaining your search process

When Uncertain:
- If exact information isn't available, say: "This specific information is not in my knowledge base"
- Don't invent dates, metrics, or details
- You can say "approximately X years" if exact dates aren't available
- Clarify when information is inferred vs. verified

All responses must be:
1. **Accurate** - Grounded in source material, no hallucination
2. **Concise** - Get to the point quickly
3. **Professional** - Suitable for recruiters, hiring managers, or colleagues
4. **Context-Rich** - Include relevant companies, timeframes, and technologies when available
5. **Balanced** - Show both her product/frontend background AND her data platform leadership

Provide only the direct answer to what was asked.
"""

    def __init__(self, api_key: str, model: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

        # Pre-build base API parameters
        self.base_params = {"model": self.model, "temperature": 0, "max_tokens": 800}

    def generate_response(
        self,
        query: str,
        conversation_history: Optional[str] = None,
        tools: Optional[List] = None,
        tool_manager=None,
    ) -> str:
        """
        Generate AI response with optional tool usage and conversation context.
        Supports up to 2 sequential rounds of tool calling.

        Args:
            query: The user's question or request
            conversation_history: Previous messages for context
            tools: Available tools the AI can use
            tool_manager: Manager to execute tools

        Returns:
            Generated response as string
        """

        # Build system content efficiently - avoid string ops when possible
        system_content = (
            f"{self.SYSTEM_PROMPT}\n\nPrevious conversation:\n{conversation_history}"
            if conversation_history
            else self.SYSTEM_PROMPT
        )

        # Start with initial messages
        messages = [{"role": "user", "content": query}]

        # Execute up to 2 rounds of tool calling
        for round_num in range(2):
            # Prepare API call parameters
            api_params = {
                **self.base_params,
                "messages": messages,
                "system": system_content,
            }

            # Add tools if available
            if tools:
                api_params["tools"] = tools
                api_params["tool_choice"] = {"type": "auto"}

            # Get response from Claude
            response = self.client.messages.create(**api_params)

            # Handle tool execution if needed
            if response.stop_reason == "tool_use" and tool_manager:
                messages, should_continue = self._handle_tool_execution(
                    response, messages, tool_manager
                )
                if not should_continue:
                    break
            else:
                # No tool use, return direct response
                return response.content[0].text

        # After max rounds, make final call without tools to get response
        final_params = {
            **self.base_params,
            "messages": messages,
            "system": system_content,
        }

        final_response = self.client.messages.create(**final_params)
        return final_response.content[0].text

    def _handle_tool_execution(self, initial_response, messages: List, tool_manager):
        """
        Handle execution of tool calls and update message history.

        Args:
            initial_response: The response containing tool use requests
            messages: Current message history
            tool_manager: Manager to execute tools

        Returns:
            Tuple of (updated_messages, should_continue)
        """
        # Add AI's tool use response
        messages.append({"role": "assistant", "content": initial_response.content})

        # Execute all tool calls and collect results
        tool_results = []
        for content_block in initial_response.content:
            if content_block.type == "tool_use":
                try:
                    tool_result = tool_manager.execute_tool(
                        content_block.name, **content_block.input
                    )

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": tool_result,
                        }
                    )
                except Exception as e:
                    # Tool execution failed, stop rounds
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": f"Error: Tool execution failed - {str(e)}",
                        }
                    )
                    # Add tool results and signal to stop
                    if tool_results:
                        messages.append({"role": "user", "content": tool_results})
                    return messages, False

        # Add tool results as single message
        if tool_results:
            messages.append({"role": "user", "content": tool_results})

        # Continue with next round
        return messages, True
