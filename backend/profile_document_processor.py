import json
import os
import re
from typing import Dict, List, Tuple

from models import ProfileChunk, ProfileSection


class ProfileDocumentProcessor:
    """Processes profile documents (Markdown and JSON) and extracts structured information"""

    def __init__(self, chunk_size: int = 700, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_profile_document(
        self, file_path: str
    ) -> Tuple[List[ProfileSection], List[ProfileChunk]]:
        """
        Process a profile document (Markdown or JSON).

        Args:
            file_path: Path to the profile document

        Returns:
            Tuple of (list of ProfileSections, list of ProfileChunks)
        """
        if file_path.endswith(".json"):
            return self.process_json_profile(file_path)
        elif file_path.endswith(".md"):
            return self.process_markdown_profile(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

    def process_json_profile(
        self, file_path: str
    ) -> Tuple[List[ProfileSection], List[ProfileChunk]]:
        """
        Process JSON profile document with structured data.

        Expected structure:
        {
          "roles": [...],
          "projects": [...],
          "skills": {...},
          "canonical_story": {...},
          "education": [...]
        }
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        sections = []
        chunks = []
        chunk_counter = 0

        # Process canonical story / tell me about yourself
        if "canonical_story" in data and "tell_me_about_yourself" in data["canonical_story"]:
            narrative = data["canonical_story"]["tell_me_about_yourself"]
            section = ProfileSection(
                section_type="background",
                title="Tell Me About Yourself",
                metadata={
                    "visibility": "public",
                    "source": "canonical_story",
                },
            )
            sections.append(section)

            # Create chunks for narrative
            narrative_chunks = self.chunk_text(narrative)
            for idx, chunk_text in enumerate(narrative_chunks):
                chunk = ProfileChunk(
                    content=chunk_text,
                    section_type="background",
                    section_title="Tell Me About Yourself",
                    metadata={"visibility": "public", "source": "canonical_story"},
                    chunk_index=chunk_counter,
                )
                chunks.append(chunk)
                chunk_counter += 1

        # Process short bio
        if "canonical_story" in data and "short_bio" in data["canonical_story"]:
            bio = data["canonical_story"]["short_bio"]
            section = ProfileSection(
                section_type="background",
                title="Short Bio",
                metadata={
                    "visibility": "public",
                    "source": "canonical_story",
                },
            )
            sections.append(section)

            chunk = ProfileChunk(
                content=bio,
                section_type="background",
                section_title="Short Bio",
                metadata={"visibility": "public", "source": "canonical_story"},
                chunk_index=chunk_counter,
            )
            chunks.append(chunk)
            chunk_counter += 1

        # Process roles
        if "roles" in data:
            for role in data["roles"]:
                title = role.get("title", "Unknown Role")
                company = role.get("company", "")
                dates = role.get("dates", "")
                highlights = role.get("highlights", [])
                skills = role.get("skills", [])

                section = ProfileSection(
                    section_type="role",
                    title=title,
                    metadata={
                        "company": company,
                        "timeframe": dates,
                        "highlights": highlights,
                        "skills": skills,
                        "visibility": "public",
                    },
                )
                sections.append(section)

                # Create content text for role
                role_text = f"Role: {title} at {company} ({dates})\n\n"
                if highlights:
                    role_text += "Highlights:\n" + "\n".join(
                        [f"- {h}" for h in highlights]
                    )

                # Chunk the role content
                role_chunks = self.chunk_text(role_text)
                for idx, chunk_text in enumerate(role_chunks):
                    chunk = ProfileChunk(
                        content=chunk_text,
                        section_type="role",
                        section_title=title,
                        metadata={
                            "company": company,
                            "timeframe": dates,
                            "visibility": "public",
                        },
                        chunk_index=chunk_counter,
                    )
                    chunks.append(chunk)
                    chunk_counter += 1

        # Process projects
        if "projects" in data:
            for project in data["projects"]:
                name = project.get("name", "Unknown Project")
                timeframe = project.get("timeframe", "")
                category = project.get("category", "")
                summary = project.get("summary", "")
                problems_solved = project.get("problems_solved", [])
                technologies = project.get("technologies", [])
                outcomes = project.get("outcomes", [])

                section = ProfileSection(
                    section_type="project",
                    title=name,
                    metadata={
                        "timeframe": timeframe,
                        "category": category,
                        "technologies": technologies,
                        "visibility": "public",
                    },
                )
                sections.append(section)

                # Create content text for project
                project_text = f"Project: {name} ({timeframe})\n"
                project_text += f"Category: {category}\n\n"
                project_text += f"Summary: {summary}\n\n"

                if problems_solved:
                    project_text += "Problems Solved:\n" + "\n".join(
                        [f"- {p}" for p in problems_solved]
                    ) + "\n\n"

                if technologies:
                    project_text += "Technologies: " + ", ".join(technologies) + "\n\n"

                if outcomes:
                    project_text += "Outcomes:\n" + "\n".join(
                        [f"- {o}" for o in outcomes]
                    )

                # Chunk the project content
                project_chunks = self.chunk_text(project_text)
                for idx, chunk_text in enumerate(project_chunks):
                    chunk = ProfileChunk(
                        content=chunk_text,
                        section_type="project",
                        section_title=name,
                        metadata={
                            "timeframe": timeframe,
                            "category": category,
                            "technologies": technologies,
                            "visibility": "public",
                        },
                        chunk_index=chunk_counter,
                    )
                    chunks.append(chunk)
                    chunk_counter += 1

        # Process skills
        if "skills" in data:
            for skill_category, skill_list in data["skills"].items():
                if isinstance(skill_list, list):
                    section = ProfileSection(
                        section_type="skill",
                        title=skill_category.replace("_", " ").title(),
                        metadata={
                            "category": skill_category,
                            "skills": skill_list,
                            "visibility": "public",
                        },
                    )
                    sections.append(section)

                    # Create content text for skills
                    skills_text = f"{skill_category.replace('_', ' ').title()}: {', '.join(skill_list)}"

                    chunk = ProfileChunk(
                        content=skills_text,
                        section_type="skill",
                        section_title=skill_category.replace("_", " ").title(),
                        metadata={
                            "category": skill_category,
                            "visibility": "public",
                        },
                        chunk_index=chunk_counter,
                    )
                    chunks.append(chunk)
                    chunk_counter += 1

        # Process education
        if "education" in data:
            for edu in data["education"]:
                school = edu.get("school", "")
                degree = edu.get("degree", "")
                field = edu.get("field", "")

                title = f"{degree} in {field}" if field else degree

                section = ProfileSection(
                    section_type="education",
                    title=title,
                    metadata={
                        "school": school,
                        "degree": degree,
                        "field": field,
                        "visibility": "public",
                    },
                )
                sections.append(section)

                # Create content text for education
                edu_text = f"Education: {degree} in {field} from {school}"

                chunk = ProfileChunk(
                    content=edu_text,
                    section_type="education",
                    section_title=title,
                    metadata={
                        "school": school,
                        "visibility": "public",
                    },
                    chunk_index=chunk_counter,
                )
                chunks.append(chunk)
                chunk_counter += 1

        return sections, chunks

    def process_markdown_profile(
        self, file_path: str
    ) -> Tuple[List[ProfileSection], List[ProfileChunk]]:
        """
        Process Markdown profile document.

        Expected structure:
        # Header 1
        ## Header 2
        ### Header 3

        Content with paragraphs, lists, etc.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        sections = []
        chunks = []
        chunk_counter = 0

        # Split by major headers (## level 2)
        header_pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
        section_splits = []

        matches = list(header_pattern.finditer(content))
        for i, match in enumerate(matches):
            section_title = match.group(1).strip()
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)

            section_content = content[start_pos:end_pos].strip()

            # Determine section type based on title keywords
            section_type = self._infer_section_type(section_title)

            # Extract metadata from content
            metadata = self._extract_metadata_from_markdown(
                section_title, section_content
            )
            metadata["visibility"] = "public"  # Default visibility

            section = ProfileSection(
                section_type=section_type, title=section_title, metadata=metadata
            )
            sections.append(section)

            # Create chunks for this section
            section_chunks = self.chunk_text(section_content)
            for idx, chunk_text in enumerate(section_chunks):
                # Add section context to first chunk
                if idx == 0:
                    chunk_text = f"[{section_title}]\n{chunk_text}"

                chunk = ProfileChunk(
                    content=chunk_text,
                    section_type=section_type,
                    section_title=section_title,
                    metadata=metadata,
                    chunk_index=chunk_counter,
                )
                chunks.append(chunk)
                chunk_counter += 1

        return sections, chunks

    def _infer_section_type(self, title: str) -> str:
        """Infer section type from title"""
        title_lower = title.lower()

        if any(
            keyword in title_lower
            for keyword in [
                "background",
                "professional background",
                "identity",
                "summary",
                "story",
                "bio",
            ]
        ):
            return "background"
        elif any(
            keyword in title_lower
            for keyword in ["role", "experience", "work history", "employment"]
        ):
            return "role"
        elif any(keyword in title_lower for keyword in ["project", "accomplishment"]):
            return "project"
        elif any(
            keyword in title_lower for keyword in ["skill", "technical", "expertise"]
        ):
            return "skill"
        elif any(keyword in title_lower for keyword in ["education", "school"]):
            return "education"
        elif any(
            keyword in title_lower
            for keyword in ["leadership", "management", "working style"]
        ):
            return "leadership"
        else:
            return "general"

    def _extract_metadata_from_markdown(
        self, title: str, content: str
    ) -> Dict[str, str]:
        """Extract metadata from markdown content"""
        metadata = {}

        # Try to extract company names
        company_match = re.search(
            r"\b(Two Sigma|Venn|Jet\.com|Walmart|SupplyHouse|Cornell)\b", content
        )
        if company_match:
            metadata["company"] = company_match.group(1)

        # Try to extract timeframes (years or Q patterns)
        timeframe_match = re.search(r"\b(20\d{2}|Q[1-4]\s*20\d{2})\b", content)
        if timeframe_match:
            metadata["timeframe"] = timeframe_match.group(1)

        # Try to extract technologies
        tech_keywords = [
            "AWS",
            "Python",
            "React",
            "JavaScript",
            "TypeScript",
            "Java",
            "SQL",
            "Lambda",
            "S3",
            "Athena",
            "Glue",
            "Step Functions",
        ]
        found_tech = [tech for tech in tech_keywords if tech in content]
        if found_tech:
            metadata["technologies"] = ", ".join(found_tech[:5])  # Limit to top 5

        return metadata

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into sentence-based chunks with overlap.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        # Clean up the text
        text = re.sub(r"\s+", " ", text.strip())  # Normalize whitespace

        # Better sentence splitting that handles abbreviations
        sentence_endings = re.compile(
            r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\!|\?)\s+(?=[A-Z])"
        )
        sentences = sentence_endings.split(text)

        # Clean sentences
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        i = 0

        while i < len(sentences):
            current_chunk = []
            current_size = 0

            # Build chunk starting from sentence i
            for j in range(i, len(sentences)):
                sentence = sentences[j]

                # Calculate size with space
                space_size = 1 if current_chunk else 0
                total_addition = len(sentence) + space_size

                # Check if adding this sentence would exceed chunk size
                if current_size + total_addition > self.chunk_size and current_chunk:
                    break

                current_chunk.append(sentence)
                current_size += total_addition

            # Add chunk if we have content
            if current_chunk:
                chunks.append(" ".join(current_chunk))

                # Calculate overlap for next chunk
                if self.chunk_overlap > 0:
                    # Find how many sentences to overlap
                    overlap_size = 0
                    overlap_sentences = 0

                    # Count backwards from end of current chunk
                    for k in range(len(current_chunk) - 1, -1, -1):
                        sentence_len = len(current_chunk[k]) + (
                            1 if k < len(current_chunk) - 1 else 0
                        )
                        if overlap_size + sentence_len <= self.chunk_overlap:
                            overlap_size += sentence_len
                            overlap_sentences += 1
                        else:
                            break

                    # Move start position considering overlap
                    next_start = i + len(current_chunk) - overlap_sentences
                    i = max(next_start, i + 1)  # Ensure we make progress
                else:
                    # No overlap - move to next sentence after current chunk
                    i += len(current_chunk)
            else:
                # No sentences fit, move to next
                i += 1

        return chunks
