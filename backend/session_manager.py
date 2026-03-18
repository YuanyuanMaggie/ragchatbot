from typing import Dict, List, Optional


class SessionManager:
    """Manages conversation sessions and message history"""

    def __init__(self, max_history: int = 5):
        self.max_history = max_history
        self.sessions: Dict[str, List[dict]] = {}
        self.session_counter = 0

    def create_session(self) -> str:
        """Create a new conversation session"""
        self.session_counter += 1
        session_id = f"session_{self.session_counter}"
        self.sessions[session_id] = []
        return session_id

    def add_exchange(self, session_id: str, user_message: str, assistant_message: str):
        """Add a complete question-answer exchange"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({"role": "user", "content": user_message})
        self.sessions[session_id].append({"role": "assistant", "content": assistant_message})

        # Keep within limits (max_history pairs = max_history * 2 messages)
        if len(self.sessions[session_id]) > self.max_history * 2:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history * 2:]

    def get_conversation_history(self, session_id: Optional[str]) -> Optional[List[dict]]:
        """Get conversation history as a list of message dicts for the API"""
        if not session_id or session_id not in self.sessions:
            return None
        messages = self.sessions[session_id]
        return messages if messages else None

    def clear_session(self, session_id: str):
        """Clear all messages from a session"""
        if session_id in self.sessions:
            self.sessions[session_id] = []
