"""
Simplified RAG System - Loads full profile and passes to Claude
No vector database, no complex chunking, just direct context
"""
import json
import os
from typing import Dict, List, Optional, Tuple

from ai_generator import AIGenerator
from session_manager import SessionManager


class RAGSystem:
    """Simplified orchestrator that passes full profile to Claude"""

    def __init__(self, config):
        self.config = config
        self.profile_data = None
        self.profile_text = None

        # Load profile on initialization
        self._load_profile()

        # Initialize components
        self.ai_generator = AIGenerator(
            api_key=config.ANTHROPIC_API_KEY,
            model=config.ANTHROPIC_MODEL,
            profile_context=self.profile_text,
        )
        self.session_manager = SessionManager(config.MAX_HISTORY)

    def _load_profile(self):
        """Load profile JSON and convert to text context for Claude"""
        profile_path = self.config.PROFILE_PATH

        # Try multiple paths to find the profile
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'yuanyuan_li_profile.json'),
            profile_path,
            os.path.join(os.path.dirname(__file__), '..', 'yuanyuan_li_profile.json'),
            'yuanyuan_li_profile.json',
            '../yuanyuan_li_profile.json',
        ]

        actual_path = None
        for path in possible_paths:
            if os.path.exists(path):
                actual_path = path
                break

        if not actual_path:
            print(f"⚠️  Profile file not found. Tried: {possible_paths}")
            self.profile_data = {}
            self.profile_text = "No profile data available."
            return

        profile_path = actual_path

        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                self.profile_data = json.load(f)

            # Convert JSON to readable text for Claude
            self.profile_text = self._format_profile_for_claude(self.profile_data)

            print(
                f"✅ Loaded profile: {len(self.profile_text)} characters, {len(self.profile_text.split())} words"
            )

        except Exception as e:
            print(f"❌ Error loading profile: {e}")
            self.profile_data = {}
            self.profile_text = "Error loading profile data."

    def _format_profile_for_claude(self, data: dict) -> str:
        """
        Convert profile JSON to well-formatted text for Claude's context

        This creates a readable narrative that Claude can easily understand
        """
        lines = []

        # Header
        lines.append("# YUANYUAN LI - PROFESSIONAL PROFILE")
        lines.append("=" * 50)
        lines.append("")

        # Basic info
        profile = data.get("profile", {})
        if profile:
            lines.append(f"Name: {profile.get('name', 'Yuanyuan Li')}")
            lines.append(f"Also Known As: {', '.join(profile.get('also_known_as', []))}")
            lines.append(f"Headline: {profile.get('headline', '')}")
            lines.append(f"Location: {profile.get('location', '')}")
            lines.append("")
            lines.append(f"## Summary")
            lines.append(profile.get('summary', ''))
            lines.append("")
            lines.append(f"## Executive Summary")
            lines.append(profile.get('executive_summary', ''))
            lines.append("")

        # Canonical story
        canonical = data.get("canonical_story", {})
        if canonical:
            lines.append("## Professional Story")
            lines.append("-" * 50)
            lines.append(canonical.get("narrative", ""))
            lines.append("")

        # Work experience (roles)
        roles = data.get("roles", [])
        if roles:
            lines.append("## Work Experience")
            lines.append("-" * 50)
            for role in roles:
                lines.append(f"\n### {role.get('title', 'Role')} at {role.get('company', 'Company')}")
                lines.append(f"Duration: {role.get('duration', 'N/A')}")
                lines.append(f"Timeframe: {role.get('timeframe', 'N/A')}")
                lines.append(f"Location: {role.get('location', 'N/A')}")
                lines.append("")
                lines.append(role.get('description', ''))
                lines.append("")

                # Key achievements
                achievements = role.get('key_achievements', [])
                if achievements:
                    lines.append("**Key Achievements:**")
                    for achievement in achievements:
                        lines.append(f"- {achievement}")
                    lines.append("")

                # Technologies
                tech = role.get('technologies_used', [])
                if tech:
                    lines.append(f"**Technologies:** {', '.join(tech)}")
                    lines.append("")

        # Projects
        projects = data.get("projects", [])
        if projects:
            lines.append("\n## Key Projects")
            lines.append("-" * 50)
            for project in projects:
                lines.append(f"\n### {project.get('name', 'Project')}")
                lines.append(f"Company: {project.get('company', 'N/A')}")
                lines.append(f"Timeframe: {project.get('timeframe', 'N/A')}")
                lines.append(f"Role: {project.get('role', 'N/A')}")
                lines.append("")
                lines.append(project.get('description', ''))
                lines.append("")

                outcomes = project.get('outcomes', [])
                if outcomes:
                    lines.append("**Outcomes:**")
                    for outcome in outcomes:
                        lines.append(f"- {outcome}")
                    lines.append("")

                tech = project.get('technologies', [])
                if tech:
                    lines.append(f"**Technologies:** {', '.join(tech)}")
                    lines.append("")

        # Skills
        skills = data.get("skills", {})
        if skills:
            lines.append("\n## Skills & Expertise")
            lines.append("-" * 50)
            for category, skill_list in skills.items():
                if isinstance(skill_list, list):
                    lines.append(f"\n### {category}")
                    for skill in skill_list:
                        if isinstance(skill, dict):
                            name = skill.get('name', '')
                            proficiency = skill.get('proficiency', '')
                            lines.append(f"- **{name}** ({proficiency})")
                        else:
                            lines.append(f"- {skill}")
                    lines.append("")

        # Education
        education = data.get("education", [])
        if education:
            lines.append("\n## Education")
            lines.append("-" * 50)
            for edu in education:
                lines.append(f"\n### {edu.get('degree', 'Degree')}")
                lines.append(f"Institution: {edu.get('institution', 'N/A')}")
                lines.append(f"Year: {edu.get('year', 'N/A')}")
                field = edu.get('field_of_study')
                if field:
                    lines.append(f"Field: {field}")
                lines.append("")

        return "\n".join(lines)

    def query(
        self, query: str, session_id: Optional[str] = None
    ) -> Tuple[str, List[str], List[str]]:
        """
        Process a user query with full profile context

        Args:
            query: User's question
            session_id: Optional session ID for conversation history

        Returns:
            Tuple of (response, sources, source_links)
        """
        # Get conversation history if session exists
        history = None
        if session_id:
            history = self.session_manager.get_conversation_history(session_id)

        # Generate response with full profile context
        response = self.ai_generator.generate_response(
            query=query, conversation_history=history
        )

        # Update conversation history
        if session_id:
            self.session_manager.add_exchange(session_id, query, response)

        # Return response (no specific sources - all of profile is the source)
        sources = ["Yuanyuan Li's Professional Profile"]
        source_links = []

        return response, sources, source_links

    def get_profile_analytics(self) -> Dict:
        """Get analytics about the profile"""
        if not self.profile_data:
            return {
                "total_sections": 0,
                "section_types": [],
                "key_highlights": ["Profile not loaded"],
            }

        # Count sections
        role_count = len(self.profile_data.get("roles", []))
        project_count = len(self.profile_data.get("projects", []))
        skill_categories = len(self.profile_data.get("skills", {}))
        education_count = len(self.profile_data.get("education", []))

        highlights = []
        if role_count > 0:
            highlights.append(f"{role_count} work experience entries")
        if project_count > 0:
            highlights.append(f"{project_count} key projects")
        if skill_categories > 0:
            highlights.append(f"{skill_categories} skill categories")
        if education_count > 0:
            highlights.append(f"{education_count} education entries")

        return {
            "total_sections": role_count + project_count + skill_categories + education_count,
            "section_types": ["roles", "projects", "skills", "education"],
            "key_highlights": highlights,
        }
