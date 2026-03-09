"""
AI Talent Operations - AI Model Mapping Agent

Intelligent agent that maps AI models to their technical details and author information.
Provides comprehensive analysis of model capabilities and researcher profiles.
"""

import os
import re
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AuthorProfile:
    """Represents an author's online presence and information."""
    name: str
    affiliation: str = ""
    homepage: str = ""
    github: str = ""
    scholar: str = ""
    arxiv: str = ""
    linkedin: str = ""
    twitter: str = ""
    email: str = ""
    publications: int = 0
    citations: int = 0

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "affiliation": self.affiliation,
            "homepage": self.homepage,
            "github": self.github,
            "scholar": self.scholar,
            "arxiv": self.arxiv,
            "linkedin": self.linkedin,
            "twitter": self.twitter,
            "email": self.email,
            "publications": self.publications,
            "citations": self.citations
        }


@dataclass
class ModelInfo:
    """Represents AI model information and metadata."""
    name: str
    technical_summary: str
    paper_title: str
    paper_url: str
    publication_date: str
    authors: List[AuthorProfile]
    abstract: str
    categories: List[str]
    architecture: str = ""
    dataset: str = ""
    metrics: Dict[str, float] = None

    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "technical_summary": self.technical_summary,
            "paper_title": self.paper_title,
            "paper_url": self.paper_url,
            "publication_date": self.publication_date,
            "authors": [author.to_dict() for author in self.authors],
            "abstract": self.abstract,
            "categories": self.categories,
            "architecture": self.architecture,
            "dataset": self.dataset,
            "metrics": self.metrics
        }


class ModelMappingAgent:
    """
    AI-powered agent for mapping and analyzing AI models.

    Searches academic databases and online sources to provide comprehensive
    technical analysis and author profiling for AI models.
    """

    def __init__(self, config_path: str = "model_mapping_config.yaml"):
        """
        Initialize the Model Mapping Agent.

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AI Talent Operations Model Mapping Agent/1.0'
        })

        logger.info("Model Mapping Agent initialized")

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        try:
            import yaml
            config_file = os.path.join(os.path.dirname(__file__), config_path)
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(f"Config file not found: {config_file}, using defaults")
                return self._get_default_config()
        except Exception as e:
            logger.warning(f"Could not load config: {e}, using defaults")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            "arxiv": {
                "base_url": "http://export.arxiv.org/api/query",
                "max_results": 5
            },
            "scholar": {
                "enabled": True,
                "max_retries": 3
            },
            "github": {
                "enabled": True,
                "search_users": True
            },
            "timeout": 10,
            "cache_enabled": True
        }

    def map_model(self, model_name: str) -> Optional[ModelInfo]:
        """
        Map an AI model to its technical details and author information.

        Args:
            model_name: Name of the AI model to map

        Returns:
            ModelInfo object with complete mapping or None if not found
        """
        logger.info(f"Starting model mapping for: {model_name}")

        try:
            # Step 1: Find the paper on arXiv
            paper_data = self._find_paper_on_arxiv(model_name)
            if not paper_data:
                logger.warning(f"No paper found for model: {model_name}")
                return None

            # Step 2: Extract basic model information
            model_info = self._extract_model_info(model_name, paper_data)

            # Step 3: Generate technical summary
            model_info.technical_summary = self._generate_technical_summary(model_info)

            # Step 4: Map author profiles
            model_info.authors = self._map_authors(paper_data['authors'])

            logger.info(f"Successfully mapped model: {model_name}")
            return model_info

        except Exception as e:
            logger.error(f"Failed to map model {model_name}: {e}")
            return None

    def _find_paper_on_arxiv(self, model_name: str) -> Optional[Dict]:
        """
        Search for the model paper on arXiv.

        Args:
            model_name: Name of the model to search for

        Returns:
            Paper data dictionary or None if not found
        """
        try:
            # Clean model name for search
            search_terms = self._clean_model_name_for_search(model_name)

            # Query arXiv API
            params = {
                'search_query': f'ti:{search_terms}',
                'start': 0,
                'max_results': self.config.get('arxiv', {}).get('max_results', 5),
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }

            response = self.session.get(
                self.config.get('arxiv', {}).get('base_url', 'http://export.arxiv.org/api/query'),
                params=params,
                timeout=self.config.get('timeout', 10)
            )

            if response.status_code != 200:
                logger.error(f"arXiv API error: {response.status_code}")
                return None

            # Parse XML response (simplified - in practice would use proper XML parsing)
            content = response.text

            # Extract paper information
            paper_data = self._parse_arxiv_response(content)
            if paper_data:
                logger.info(f"Found paper on arXiv: {paper_data.get('title', 'Unknown')}")
                return paper_data

        except Exception as e:
            logger.error(f"Error searching arXiv: {e}")

        return None

    def _clean_model_name_for_search(self, model_name: str) -> str:
        """Clean model name for arXiv search."""
        # Handle specific model names first
        model_mappings = {
            'chatgpt': 'chat gpt',
            'gpt-4': 'gpt 4',
            'llama-2': 'llama 2',
            'bert-base': 'bert',
            'vit-b': 'vision transformer',
        }

        # Check for exact matches first
        lower_name = model_name.lower()
        for key, value in model_mappings.items():
            if key in lower_name:
                return value

        # Remove common prefixes/suffixes
        cleaned = re.sub(r'^(GPT|BERT|LLaMA|CLIP|T5|ViT)\s*[-]?\s*', '', model_name, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s+(model|transformer|network)$', '', cleaned, flags=re.IGNORECASE)

        return cleaned.strip()

    def _parse_arxiv_response(self, xml_content: str) -> Optional[Dict]:
        """Parse arXiv XML response (simplified implementation)."""
        # This is a simplified parser - in production would use proper XML parsing
        try:
            # Extract basic information using regex (not ideal but works for demo)
            title_match = re.search(r'<title>(.*?)</title>', xml_content, re.DOTALL)
            abstract_match = re.search(r'<summary>(.*?)</summary>', xml_content, re.DOTALL)
            authors_match = re.findall(r'<name>(.*?)</name>', xml_content)
            published_match = re.search(r'<published>(.*?)</published>', xml_content)
            id_match = re.search(r'<id>http://arxiv.org/abs/(.*?)</id>', xml_content)

            if not title_match:
                return None

            return {
                'title': title_match.group(1).strip(),
                'abstract': abstract_match.group(1).strip() if abstract_match else '',
                'authors': authors_match,
                'published': published_match.group(1)[:10] if published_match else '',
                'arxiv_id': id_match.group(1) if id_match else '',
                'url': f"https://arxiv.org/abs/{id_match.group(1)}" if id_match else ''
            }

        except Exception as e:
            logger.error(f"Error parsing arXiv response: {e}")
            return None

    def _extract_model_info(self, model_name: str, paper_data: Dict) -> ModelInfo:
        """Extract basic model information from paper data."""
        # Extract categories from abstract/title
        categories = self._extract_categories(paper_data.get('abstract', ''))

        return ModelInfo(
            name=model_name,
            technical_summary="",  # Will be generated later
            paper_title=paper_data.get('title', ''),
            paper_url=paper_data.get('url', ''),
            publication_date=paper_data.get('published', ''),
            authors=[],  # Will be populated later
            abstract=paper_data.get('abstract', ''),
            categories=categories
        )

    def _extract_categories(self, abstract: str) -> List[str]:
        """Extract AI/ML categories from abstract."""
        categories = []

        # Common AI/ML keywords
        category_keywords = {
            'NLP': ['natural language', 'language model', 'text', 'conversation', 'chat'],
            'Computer Vision': ['vision', 'image', 'visual', 'object detection', 'segmentation'],
            'Multimodal': ['multimodal', 'vision-language', 'image-text'],
            'Reinforcement Learning': ['reinforcement', 'rl ', 'policy', 'agent'],
            'Generative AI': ['generative', 'diffusion', 'gan', 'vae'],
            'Transformer': ['transformer', 'attention', 'self-attention'],
            'Large Language Model': ['large language model', 'llm', 'foundation model'],
            'Fine-tuning': ['fine-tun', 'instruction tun', 'parameter efficient'],
        }

        abstract_lower = abstract.lower()
        for category, keywords in category_keywords.items():
            if any(keyword in abstract_lower for keyword in keywords):
                categories.append(category)

        return categories[:3]  # Limit to top 3 categories

    def _generate_technical_summary(self, model_info: ModelInfo) -> str:
        """Generate a technical summary of the model."""
        summary_parts = []

        # Basic description
        if model_info.categories:
            summary_parts.append(f"A {', '.join(model_info.categories).lower()} model")

        # Architecture hints from title/abstract
        if 'transformer' in model_info.abstract.lower():
            summary_parts.append("based on transformer architecture")
        elif 'convolutional' in model_info.abstract.lower():
            summary_parts.append("using convolutional neural networks")

        # Scale indicators
        if any(term in model_info.abstract.lower() for term in ['billion', 'million parameters', 'large scale']):
            summary_parts.append("trained on massive datasets")

        # Capabilities
        if 'generation' in model_info.abstract.lower():
            summary_parts.append("capable of content generation")
        if 'understanding' in model_info.abstract.lower():
            summary_parts.append("focused on comprehension tasks")

        if not summary_parts:
            summary_parts.append("An advanced AI model with state-of-the-art capabilities")

        return ". ".join(summary_parts) + "."

    def _map_authors(self, author_names: List[str]) -> List[AuthorProfile]:
        """Map author names to detailed profiles."""
        author_profiles = []

        for i, author_name in enumerate(author_names):
            logger.info(f"Mapping author {i+1}/{len(author_names)}: {author_name}")

            profile = AuthorProfile(name=author_name)

            # For the first author, do detailed mapping
            if i == 0:
                profile = self._detailed_author_mapping(author_name)
            else:
                # For other authors, basic mapping
                profile = self._basic_author_mapping(author_name)

            author_profiles.append(profile)

        return author_profiles

    def _detailed_author_mapping(self, author_name: str) -> AuthorProfile:
        """Perform detailed mapping for the first author."""
        profile = AuthorProfile(name=author_name)

        try:
            # Try to find Google Scholar profile
            scholar_info = self._find_google_scholar_profile(author_name)
            if scholar_info:
                profile.scholar = scholar_info.get('url', '')
                profile.publications = scholar_info.get('publications', 0)
                profile.citations = scholar_info.get('citations', 0)

            # Try to find GitHub profile
            github_info = self._find_github_profile(author_name)
            if github_info:
                profile.github = github_info.get('url', '')

            # Try to find personal homepage
            homepage = self._find_personal_homepage(author_name)
            if homepage:
                profile.homepage = homepage

            # Generate arXiv author link
            profile.arxiv = f"https://arxiv.org/search/?searchtype=author&query={author_name.replace(' ', '+')}"

        except Exception as e:
            logger.warning(f"Error in detailed mapping for {author_name}: {e}")

        return profile

    def _basic_author_mapping(self, author_name: str) -> AuthorProfile:
        """Perform basic mapping for other authors."""
        profile = AuthorProfile(name=author_name)

        # Basic arXiv link for all authors
        profile.arxiv = f"https://arxiv.org/search/?searchtype=author&query={author_name.replace(' ', '+')}"

        return profile

    def _find_google_scholar_profile(self, author_name: str) -> Optional[Dict]:
        """Find Google Scholar profile (placeholder - would need Scholar API)."""
        # This is a placeholder - in practice would use Scholar API or scraping
        # For demo purposes, return mock data for well-known authors
        mock_scholar_data = {
            "Yann LeCun": {
                "url": "https://scholar.google.com/citations?user=WLN3QrAAAAAJ",
                "publications": 450,
                "citations": 280000
            },
            "Ian Goodfellow": {
                "url": "https://scholar.google.com/citations?user=iYin3kIAAAAJ",
                "publications": 120,
                "citations": 95000
            },
            "Yoshua Bengio": {
                "url": "https://scholar.google.com/citations?user=kukA0LcAAAAJ",
                "publications": 600,
                "citations": 350000
            }
        }

        return mock_scholar_data.get(author_name)

    def _find_github_profile(self, author_name: str) -> Optional[Dict]:
        """Find GitHub profile (placeholder)."""
        # This is a placeholder - would use GitHub API
        mock_github_data = {
            "Yann LeCun": {"url": "https://github.com/yannlecun"},
            "Ian Goodfellow": {"url": "https://github.com/goodfeli"},
            "Yoshua Bengio": {"url": "https://github.com/yoshuabengio"}
        }

        return mock_github_data.get(author_name)

    def _find_personal_homepage(self, author_name: str) -> str:
        """Find personal homepage (placeholder)."""
        # This is a placeholder - would search academic websites
        mock_homepages = {
            "Yann LeCun": "https://yann.lecun.com/",
            "Ian Goodfellow": "https://www.iangoodfellow.com/",
            "Yoshua Bengio": "https://yoshuabengio.com/"
        }

        return mock_homepages.get(author_name, "")

    def save_mapping(self, model_info: ModelInfo, output_file: str = None):
        """Save model mapping to JSON file."""
        if not output_file:
            output_file = f"model_mapping_{model_info.name.replace(' ', '_').lower()}.json"

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(model_info.to_dict(), f, indent=2, ensure_ascii=False)

            logger.info(f"Model mapping saved to: {output_file}")

        except Exception as e:
            logger.error(f"Failed to save mapping: {e}")


def main():
    """Main entry point for model mapping agent."""
    agent = ModelMappingAgent()

    # Example usage
    print("🤖 AI Model Mapping Agent")
    print("=" * 40)

    # Test with a well-known model
    model_name = "GPT-3"
    print(f"🔍 Mapping model: {model_name}")

    result = agent.map_model(model_name)

    if result:
        print("✅ Mapping successful!")
        print(f"📄 Paper: {result.paper_title}")
        print(f"👥 Authors: {len(result.authors)}")
        print(f"📊 Technical Summary: {result.technical_summary}")

        if result.authors:
            print(f"\n🔍 First Author Details ({result.authors[0].name}):")
            author = result.authors[0]
            if author.scholar:
                print(f"   • Google Scholar: {author.scholar}")
            if author.github:
                print(f"   • GitHub: {author.github}")
            if author.homepage:
                print(f"   • Homepage: {author.homepage}")
            if author.arxiv:
                print(f"   • arXiv: {author.arxiv}")

        agent.save_mapping(result)
    else:
        print("❌ Model not found or mapping failed")


if __name__ == "__main__":
    main()
