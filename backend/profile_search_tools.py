from typing import Any, Dict, Optional

from search_tools import Tool
from vector_store import SearchResults, VectorStore


class ProfileSearchTool(Tool):
    """Tool for searching profile content with filters (company, timeframe, section type)"""

    def __init__(self, vector_store: VectorStore):
        self.store = vector_store
        self.last_sources = []  # Track sources from last search
        self.last_source_links = []  # Track source links (for future use)

    def get_tool_definition(self) -> Dict[str, Any]:
        """Return Anthropic tool definition for this tool"""
        return {
            "name": "search_profile",
            "description": "Search Yuanyuan Li's professional profile with optional filters for company, timeframe, or section type",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for in Yuanyuan's profile (e.g., 'AWS experience', 'data platform projects', 'leadership style')",
                    },
                    "section_type": {
                        "type": "string",
                        "description": "Filter by section type: 'role', 'project', 'skill', 'education', 'background', 'leadership'",
                    },
                    "company": {
                        "type": "string",
                        "description": "Filter by company name (e.g., 'Two Sigma', 'Venn', 'Jet.com')",
                    },
                    "timeframe": {
                        "type": "string",
                        "description": "Filter by timeframe (e.g., '2024', 'Q4 2024', '2018-07 to Present')",
                    },
                },
                "required": ["query"],
            },
        }

    def execute(
        self,
        query: str,
        section_type: Optional[str] = None,
        company: Optional[str] = None,
        timeframe: Optional[str] = None,
    ) -> str:
        """
        Execute the search tool with given parameters.

        Args:
            query: What to search for
            section_type: Optional section type filter
            company: Optional company filter
            timeframe: Optional timeframe filter

        Returns:
            Formatted search results or error message
        """
        # Use the vector store's profile search interface
        results = self.store.search_profile(
            query=query,
            section_type=section_type,
            company=company,
            timeframe=timeframe,
        )

        # Handle errors
        if results.error:
            return results.error

        # Handle empty results
        if results.is_empty():
            filter_info = ""
            if section_type:
                filter_info += f" in {section_type} sections"
            if company:
                filter_info += f" at {company}"
            if timeframe:
                filter_info += f" during {timeframe}"
            return f"No relevant information found{filter_info}."

        # Format and return results
        return self._format_results(results)

    def _format_results(self, results: SearchResults) -> str:
        """Format search results with profile context"""
        formatted = []
        sources = []  # Track sources for the UI
        source_links = []  # Track links (placeholder for now)

        for doc, meta in zip(results.documents, results.metadata):
            section_title = meta.get("section_title", "Unknown Section")
            section_type = meta.get("section_type", "general")
            company = meta.get("company", "")
            timeframe = meta.get("timeframe", "")

            # Build context header
            header_parts = [section_title]
            if section_type:
                header_parts.append(f"({section_type})")
            if company:
                header_parts.append(f"at {company}")
            if timeframe:
                header_parts.append(f"[{timeframe}]")

            header = " ".join(header_parts)

            # Track source for the UI
            source = section_title
            if company:
                source += f" at {company}"
            if timeframe:
                source += f" ({timeframe})"
            sources.append(source)
            source_links.append(None)  # No links for profile content

            formatted.append(f"[{header}]\n{doc}")

        # Store sources and links for retrieval
        self.last_sources = sources
        self.last_source_links = source_links

        return "\n\n".join(formatted)


class ProfileSummaryTool(Tool):
    """Tool for getting structured summaries of profile sections"""

    def __init__(self, vector_store: VectorStore):
        self.store = vector_store

    def get_tool_definition(self) -> Dict[str, Any]:
        """Return Anthropic tool definition for this tool"""
        return {
            "name": "get_profile_summary",
            "description": "Get structured overview of Yuanyuan Li's profile sections (roles, projects, skills, education)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "section_type": {
                        "type": "string",
                        "description": "Type of summary to get: 'all' (overview of everything), 'roles' (work experience), 'projects' (key projects), 'skills' (technical skills), 'education'",
                    }
                },
                "required": ["section_type"],
            },
        }

    def execute(self, section_type: str = "all") -> str:
        """
        Execute the summary tool to get profile overview.

        Args:
            section_type: Type of summary to retrieve

        Returns:
            Formatted profile summary
        """
        try:
            # Get all profile sections metadata
            all_sections = self.store.get_all_profile_sections()

            if not all_sections:
                return "No profile information available."

            # Filter by section type if not "all"
            if section_type != "all":
                filtered_sections = [
                    s for s in all_sections if s.get("section_type") == section_type
                ]
            else:
                filtered_sections = all_sections

            if not filtered_sections:
                return f"No {section_type} sections found in profile."

            # Format summary based on section type
            if section_type == "all":
                return self._format_all_summary(all_sections)
            elif section_type == "roles":
                return self._format_roles_summary(filtered_sections)
            elif section_type == "projects":
                return self._format_projects_summary(filtered_sections)
            elif section_type == "skills":
                return self._format_skills_summary(filtered_sections)
            elif section_type == "education":
                return self._format_education_summary(filtered_sections)
            else:
                return self._format_generic_summary(filtered_sections, section_type)

        except Exception as e:
            return f"Error retrieving profile summary: {str(e)}"

    def _format_all_summary(self, sections: list) -> str:
        """Format overview of all profile sections"""
        summary = ["**Yuanyuan Li - Professional Profile Overview**\n"]

        # Count sections by type
        section_counts = {}
        for section in sections:
            stype = section.get("section_type", "general")
            section_counts[stype] = section_counts.get(stype, 0) + 1

        summary.append("**Profile Sections:**")
        for stype, count in sorted(section_counts.items()):
            summary.append(f"- {stype.title()}: {count} section(s)")

        # List key roles
        roles = [s for s in sections if s.get("section_type") == "role"]
        if roles:
            summary.append("\n**Key Roles:**")
            for role in roles[:3]:  # Top 3 roles
                title = role.get("title", "Unknown")
                company = role.get("company", "")
                timeframe = role.get("timeframe", "")
                summary.append(f"- {title} at {company} ({timeframe})")

        # List key projects
        projects = [s for s in sections if s.get("section_type") == "project"]
        if projects:
            summary.append(f"\n**Key Projects:** {len(projects)} total")
            for proj in projects[:3]:  # Top 3 projects
                title = proj.get("title", "Unknown")
                summary.append(f"- {title}")

        return "\n".join(summary)

    def _format_roles_summary(self, sections: list) -> str:
        """Format roles/experience summary"""
        summary = ["**Work Experience:**\n"]

        for section in sections:
            title = section.get("title", "Unknown Role")
            company = section.get("company", "")
            timeframe = section.get("timeframe", "")

            summary.append(f"**{title}**")
            if company:
                summary.append(f"Company: {company}")
            if timeframe:
                summary.append(f"Duration: {timeframe}")

            # Add highlights if available
            metadata = section.get("metadata", {})
            if isinstance(metadata, dict) and "highlights" in metadata:
                highlights = metadata["highlights"]
                if isinstance(highlights, list) and highlights:
                    summary.append("Key Highlights:")
                    for highlight in highlights[:3]:  # Top 3 highlights
                        summary.append(f"- {highlight}")

            summary.append("")  # Blank line

        return "\n".join(summary)

    def _format_projects_summary(self, sections: list) -> str:
        """Format projects summary"""
        summary = ["**Key Projects:**\n"]

        for section in sections:
            title = section.get("title", "Unknown Project")
            timeframe = section.get("timeframe", "")
            category = section.get("category", "")

            summary.append(f"**{title}**")
            if timeframe:
                summary.append(f"Timeframe: {timeframe}")
            if category:
                summary.append(f"Category: {category}")

            # Add technologies if available
            metadata = section.get("metadata", {})
            if isinstance(metadata, dict) and "technologies" in metadata:
                technologies = metadata["technologies"]
                if technologies:
                    if isinstance(technologies, list):
                        summary.append(f"Technologies: {', '.join(technologies)}")
                    else:
                        summary.append(f"Technologies: {technologies}")

            summary.append("")  # Blank line

        return "\n".join(summary)

    def _format_skills_summary(self, sections: list) -> str:
        """Format skills summary"""
        summary = ["**Technical Skills:**\n"]

        for section in sections:
            title = section.get("title", "Unknown Category")
            metadata = section.get("metadata", {})

            summary.append(f"**{title}:**")

            if isinstance(metadata, dict) and "skills" in metadata:
                skills = metadata["skills"]
                if isinstance(skills, list):
                    summary.append(", ".join(skills))
                else:
                    summary.append(str(skills))

            summary.append("")  # Blank line

        return "\n".join(summary)

    def _format_education_summary(self, sections: list) -> str:
        """Format education summary"""
        summary = ["**Education:**\n"]

        for section in sections:
            title = section.get("title", "Unknown Degree")
            school = section.get("school", "")

            summary.append(f"- {title}")
            if school:
                summary.append(f"  School: {school}")

        return "\n".join(summary)

    def _format_generic_summary(self, sections: list, section_type: str) -> str:
        """Format generic summary for other section types"""
        summary = [f"**{section_type.title()} Sections:**\n"]

        for section in sections:
            title = section.get("title", "Unknown")
            summary.append(f"- {title}")

        return "\n".join(summary)
