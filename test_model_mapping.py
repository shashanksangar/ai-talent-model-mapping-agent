"""
AI Talent Operations - Model Mapping Agent Tests

Basic tests to validate model mapping agent functionality.
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from model_mapping_agent import ModelMappingAgent, AuthorProfile, ModelInfo


class TestModelMappingAgent(unittest.TestCase):
    """Test cases for ModelMappingAgent."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        self.temp_config.write("""
arxiv:
  base_url: "http://export.arxiv.org/api/query"
  max_results: 5
timeout: 10
""")
        self.temp_config.close()

        # Create agent with temp config
        self.agent = ModelMappingAgent(self.temp_config.name)

    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_config.name)
        # Clean up any created files
        for filename in ["model_mapping_test.json"]:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_agent_initialization(self):
        """Test agent initializes correctly."""
        self.assertIsInstance(self.agent, ModelMappingAgent)
        self.assertIsNotNone(self.agent.config)
        self.assertIn('arxiv', self.agent.config)

    def test_clean_model_name_for_search(self):
        """Test model name cleaning for search."""
        # Test basic cleaning
        self.assertEqual(self.agent._clean_model_name_for_search("GPT-3"), "3")
        self.assertEqual(self.agent._clean_model_name_for_search("BERT-base"), "bert")

        # Test specific mappings
        self.assertEqual(self.agent._clean_model_name_for_search("ChatGPT"), "chat gpt")
        self.assertEqual(self.agent._clean_model_name_for_search("LLaMA-2"), "llama 2")

    def test_extract_categories(self):
        """Test category extraction from abstract."""
        abstract = "This paper presents a large language model based on transformer architecture for natural language processing tasks."

        categories = self.agent._extract_categories(abstract)

        self.assertIn("NLP", categories)
        self.assertIn("Transformer", categories)
        self.assertIn("Large Language Model", categories)

    def test_generate_technical_summary(self):
        """Test technical summary generation."""
        model_info = ModelInfo(
            name="Test Model",
            technical_summary="",
            paper_title="Test Paper",
            paper_url="https://arxiv.org/abs/test",
            publication_date="2023-01-01",
            authors=[],
            abstract="A transformer-based language model for natural language processing.",
            categories=["NLP", "Transformer"]
        )

        summary = self.agent._generate_technical_summary(model_info)

        self.assertIn("transformer", summary.lower())
        self.assertTrue(summary.endswith("."))

    def test_author_profile_creation(self):
        """Test author profile creation."""
        profile = AuthorProfile(
            name="Test Author",
            affiliation="Test University",
            homepage="https://test.edu",
            github="https://github.com/test",
            scholar="https://scholar.google.com/test",
            publications=10,
            citations=100
        )

        self.assertEqual(profile.name, "Test Author")
        self.assertEqual(profile.publications, 10)
        self.assertEqual(profile.citations, 100)

        # Test to_dict
        data = profile.to_dict()
        self.assertEqual(data["name"], "Test Author")
        self.assertEqual(data["publications"], 10)

    def test_model_info_creation(self):
        """Test model info creation."""
        authors = [AuthorProfile(name="Author 1"), AuthorProfile(name="Author 2")]
        metrics = {"accuracy": 0.95, "f1_score": 0.92}

        model_info = ModelInfo(
            name="Test Model",
            technical_summary="A test model",
            paper_title="Test Paper",
            paper_url="https://arxiv.org/abs/test",
            publication_date="2023-01-01",
            authors=authors,
            abstract="Test abstract",
            categories=["NLP"],
            architecture="Transformer",
            dataset="Test Dataset",
            metrics=metrics
        )

        self.assertEqual(model_info.name, "Test Model")
        self.assertEqual(len(model_info.authors), 2)
        self.assertEqual(model_info.metrics["accuracy"], 0.95)

        # Test to_dict
        data = model_info.to_dict()
        self.assertEqual(data["name"], "Test Model")
        self.assertEqual(len(data["authors"]), 2)

    @patch('model_mapping_agent.requests.Session.get')
    def test_find_paper_on_arxiv_success(self, mock_get):
        """Test successful arXiv paper finding."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Test Paper Title</title>
    <summary>Test abstract content</summary>
    <name>Author One</name>
    <name>Author Two</name>
    <published>2023-01-01T00:00:00Z</published>
    <id>http://arxiv.org/abs/1234.5678</id>
  </entry>
</feed>"""
        mock_get.return_value = mock_response

        result = self.agent._find_paper_on_arxiv("Test Model")

        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Test Paper Title")
        self.assertEqual(result["authors"], ["Author One", "Author Two"])
        self.assertEqual(result["arxiv_id"], "1234.5678")

    @patch('model_mapping_agent.requests.Session.get')
    def test_find_paper_on_arxiv_failure(self, mock_get):
        """Test arXiv paper finding failure."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.agent._find_paper_on_arxiv("Nonexistent Model")

        self.assertIsNone(result)

    def test_detailed_author_mapping(self):
        """Test detailed author mapping."""
        # Test with known author (mock data)
        profile = self.agent._detailed_author_mapping("Yann LeCun")

        self.assertEqual(profile.name, "Yann LeCun")
        self.assertIn("scholar.google.com", profile.scholar)
        self.assertIn("github.com", profile.github)
        self.assertIn("lecun.com", profile.homepage)

    def test_basic_author_mapping(self):
        """Test basic author mapping."""
        profile = self.agent._basic_author_mapping("Unknown Author")

        self.assertEqual(profile.name, "Unknown Author")
        self.assertIn("arxiv.org", profile.arxiv)
        self.assertIn("Unknown+Author", profile.arxiv)

    def test_save_mapping(self):
        """Test saving model mapping to file."""
        authors = [AuthorProfile(name="Test Author")]
        model_info = ModelInfo(
            name="Test Model",
            technical_summary="Test summary",
            paper_title="Test Paper",
            paper_url="https://arxiv.org/abs/test",
            publication_date="2023-01-01",
            authors=authors,
            abstract="Test abstract",
            categories=["Test"]
        )

        self.agent.save_mapping(model_info, "model_mapping_test.json")

        self.assertTrue(os.path.exists("model_mapping_test.json"))

        # Verify content
        import json
        with open("model_mapping_test.json", 'r') as f:
            data = json.load(f)

        self.assertEqual(data["name"], "Test Model")
        self.assertEqual(data["technical_summary"], "Test summary")


class TestAuthorProfile(unittest.TestCase):
    """Test cases for AuthorProfile class."""

    def test_author_profile_initialization(self):
        """Test author profile initialization."""
        profile = AuthorProfile(
            name="Test Author",
            affiliation="Test University",
            homepage="https://test.edu",
            github="https://github.com/test",
            scholar="https://scholar.google.com/test",
            arxiv="https://arxiv.org/search/?searchtype=author&query=Test+Author",
            linkedin="https://linkedin.com/in/test",
            twitter="https://twitter.com/test",
            email="test@test.edu",
            publications=50,
            citations=1000
        )

        self.assertEqual(profile.name, "Test Author")
        self.assertEqual(profile.affiliation, "Test University")
        self.assertEqual(profile.publications, 50)
        self.assertEqual(profile.citations, 1000)

    def test_author_profile_to_dict(self):
        """Test author profile serialization."""
        profile = AuthorProfile(name="Test Author", publications=10)

        data = profile.to_dict()

        expected_keys = ["name", "affiliation", "homepage", "github", "scholar",
                        "arxiv", "linkedin", "twitter", "email", "publications", "citations"]

        for key in expected_keys:
            self.assertIn(key, data)

        self.assertEqual(data["name"], "Test Author")
        self.assertEqual(data["publications"], 10)


class TestModelInfo(unittest.TestCase):
    """Test cases for ModelInfo class."""

    def test_model_info_initialization(self):
        """Test model info initialization."""
        authors = [AuthorProfile(name="Author 1"), AuthorProfile(name="Author 2")]
        metrics = {"accuracy": 0.95}

        model_info = ModelInfo(
            name="Test Model",
            technical_summary="Test summary",
            paper_title="Test Paper Title",
            paper_url="https://arxiv.org/abs/1234.5678",
            publication_date="2023-01-01",
            authors=authors,
            abstract="Test abstract content",
            categories=["NLP", "Transformer"],
            architecture="Transformer",
            dataset="Test Dataset",
            metrics=metrics
        )

        self.assertEqual(model_info.name, "Test Model")
        self.assertEqual(model_info.paper_title, "Test Paper Title")
        self.assertEqual(len(model_info.authors), 2)
        self.assertEqual(model_info.categories, ["NLP", "Transformer"])
        self.assertEqual(model_info.metrics["accuracy"], 0.95)

    def test_model_info_to_dict(self):
        """Test model info serialization."""
        model_info = ModelInfo(
            name="Test Model",
            technical_summary="Test summary",
            paper_title="Test Paper",
            paper_url="https://arxiv.org/abs/test",
            publication_date="2023-01-01",
            authors=[AuthorProfile(name="Test Author")],
            abstract="Test abstract",
            categories=["Test"]
        )

        data = model_info.to_dict()

        expected_keys = ["name", "technical_summary", "paper_title", "paper_url",
                        "publication_date", "authors", "abstract", "categories",
                        "architecture", "dataset", "metrics"]

        for key in expected_keys:
            self.assertIn(key, data)

        self.assertEqual(data["name"], "Test Model")
        self.assertEqual(len(data["authors"]), 1)


def run_tests():
    """Run all tests."""
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests()
