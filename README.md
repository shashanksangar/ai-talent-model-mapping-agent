# AI Talent Model Mapping Agent

Intelligent agent that maps AI models to their technical specifications and researcher profiles. Discovers model capabilities, architecture details, and comprehensive author information from academic databases and online sources.

## 🎯 Purpose

The Model Mapping Agent addresses the challenge of understanding AI models and their creators by:

- **Model Discovery**: Automatically finds and analyzes AI model papers from academic databases
- **Technical Analysis**: Generates concise summaries of model capabilities and architecture
- **Author Profiling**: Maps researchers to their complete online presence (GitHub, Scholar, websites)
- **Researcher Intelligence**: Provides detailed profiles for talent identification and outreach

## ✨ Features

### Core Functionality
- 🔍 **Academic Search**: Queries arXiv and other databases for model papers
- 📊 **Technical Summarization**: AI-powered analysis of model capabilities and architecture
- 👥 **Author Mapping**: Comprehensive profiling of researchers and their online presence
- 🔗 **Profile Enrichment**: Links to GitHub, Google Scholar, personal websites, and academic profiles
- 📈 **Citation Tracking**: Publication counts and citation metrics where available

### User Interface
- 🖥️ **Interactive CLI**: Rich console interface with formatted output
- 📋 **Detailed Reports**: Structured display of model and author information
- 💾 **Export Options**: JSON and Markdown export capabilities
- 🔄 **Batch Processing**: Support for multiple model analysis

### Integration Ready
- 🤖 **Operations Orchestrator**: Integrated with main workflow system

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI
python model_mapping_cli.py

# Or use programmatically
from model_mapping_agent import ModelMappingAgent

agent = ModelMappingAgent()
result = agent.map_model("GPT-4")
```

## 📋 Usage Examples

### CLI Interface
```bash
# Interactive mapping
python model_mapping_cli.py

# Direct model mapping
python model_mapping_cli.py --model "GPT-4"
```

### Demo Script
```bash
python demo_model_mapping.py
```

## 🏗️ Architecture

- `model_mapping_agent.py` - Core mapping logic and arXiv integration
- `model_mapping_cli.py` - Command-line interface with rich formatting
- `model_mapping_config.yaml` - Configuration and API settings
- `test_model_mapping.py` - Comprehensive test suite

## 🔧 Configuration

Edit `model_mapping_config.yaml` to:
- Configure arXiv API settings
- Set up author profiling sources
- Customize output formats
- Configure mock data for testing

## 🧪 Testing

```bash
# Run all tests
python -m pytest test_model_mapping.py -v

# Run with coverage
python -m pytest test_model_mapping.py --cov=model_mapping_agent
```

## 📊 Test Coverage

- Model discovery and analysis
- Author profiling logic
- arXiv API integration
- Data validation and error handling
- CLI interface functionality

## 🤝 Integration

This agent integrates with the main [AI Talent Operations](https://github.com/shashanksangar/ai-talent-operations) orchestrator.

## 📄 License

MIT License
- 📚 **Academic APIs**: arXiv, Google Scholar, GitHub API support
- 🔗 **Web Scraping**: Intelligent homepage and profile discovery
- 📊 **Analytics**: Usage tracking and performance metrics

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Basic Usage
```python
from model_mapping_agent import ModelMappingAgent

# Initialize agent
agent = ModelMappingAgent()

# Map a model
result = agent.map_model("GPT-4")

if result:
    print(f"Model: {result.name}")
    print(f"Summary: {result.technical_summary}")
    print(f"First Author: {result.authors[0].name}")
    print(f"GitHub: {result.authors[0].github}")
    print(f"Scholar: {result.authors[0].scholar}")
```

### CLI Interface
```bash
cd workflows/model_mapping
python model_mapping_cli.py
```

## 📋 Menu Options

### Main Menu
- 🔍 **Map AI Model**: Interactive model search and analysis
- 👀 **View Previous Mappings**: Browse cached results
- 📤 **Export Results**: Export to various formats
- ℹ️ **About**: Agent information and capabilities

### Mapping Process
1. Enter model name (e.g., "GPT-4", "BERT", "LLaMA-2")
2. Agent searches academic databases for the paper
3. Extracts technical details and author information
4. Performs detailed profiling of the first author
5. Generates basic profiles for remaining authors
6. Displays comprehensive results with links

## 🔧 Configuration

### API Configuration
```yaml
arxiv:
  base_url: "http://export.arxiv.org/api/query"
  max_results: 5

scholar:
  enabled: true
  api_key: "${GOOGLE_SCHOLAR_API_KEY}"

github:
  enabled: true
  api_token: "${GITHUB_API_TOKEN}"
```

### Model Categories
```yaml
model_categories:
  nlp: ["natural language", "text", "conversation"]
  computer_vision: ["vision", "image", "visual"]
  multimodal: ["multimodal", "vision-language"]
  transformers: ["transformer", "attention"]
```

### Known Models Database
Pre-configured data for popular models:
```yaml
known_models:
  "GPT-3":
    technical_summary: "Large language model with transformer architecture"
    first_author: "Tom B. Brown"
    categories: ["NLP", "Large Language Model"]
```

## 📊 Output Format

### Model Information
- **Technical Summary**: Concise description of capabilities
- **Paper Details**: Title, publication date, arXiv link
- **Categories**: AI/ML domains (NLP, Vision, etc.)
- **Abstract**: Paper abstract preview

### Author Profiles

#### First Author (Detailed)
- 🏠 **Homepage**: Personal/academic website
- 🎓 **Google Scholar**: Publications and citations
- 💻 **GitHub**: Code repositories and contributions
- 📄 **arXiv**: Research papers and preprints
- 💼 **LinkedIn**: Professional network (future)
- 🐦 **Twitter**: Social media presence (future)

#### Other Authors (Basic)
- 📄 **arXiv Link**: Search for author's publications

## 🔗 Integration Points

### With Other Agents
- **Sourcing Agent**: Model creators as candidate leads
- **Matching Agent**: Technical skill assessment for researchers
- **Outreach Agent**: Personalized messaging based on research interests
- **Scheduling Agent**: Interview coordination with model authors

### External APIs
- **arXiv API**: Academic paper search and metadata
- **Google Scholar**: Researcher profiles and citation metrics
- **GitHub API**: Code repositories and contributor information
- **Academic Websites**: University and research institution pages

## 🛠️ Development

### Project Structure
```
workflows/model_mapping/
├── model_mapping_agent.py      # Core mapping logic
├── model_mapping_cli.py        # Command-line interface
├── model_mapping_config.yaml   # Configuration file
├── test_model_mapping.py       # Unit tests
├── requirements.txt            # Dependencies
└── README.md                  # This file
```

### Key Classes

#### ModelMappingAgent
Main agent class handling model discovery and author profiling.

#### ModelInfo
Data structure containing complete model information and metadata.

#### AuthorProfile
Comprehensive author profile with online presence mapping.

## 🔒 Security & Compliance

- **Rate Limiting**: Respectful API usage with built-in delays
- **Data Privacy**: No personal data storage or sharing
- **Academic Ethics**: Proper attribution and citation practices
- **API Compliance**: Adherence to platform terms of service

## 📈 Future Enhancements

### Planned Features
- [ ] **Semantic Scholar Integration**: Enhanced academic search
- [ ] **ORCID Integration**: Researcher identifier linking
- [ ] **LinkedIn Profiles**: Professional network analysis
- [ ] **Twitter/X Analysis**: Research discussion tracking
- [ ] **Model Performance Metrics**: Benchmark result extraction
- [ ] **Citation Network Analysis**: Research collaboration mapping
- [ ] **GitHub Contribution Analysis**: Code activity metrics
- [ ] **Patent Search**: Commercial application tracking

### Advanced Features
- [ ] **Model Comparison**: Side-by-side analysis of similar models
- [ ] **Trend Analysis**: Research direction and popularity tracking
- [ ] **Collaboration Networks**: Researcher relationship mapping
- [ ] **Funding Source Analysis**: Grant and sponsorship tracking
- [ ] **Industry Partnerships**: Commercial collaboration identification

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check the [troubleshooting guide](#troubleshooting)
- Review [API configuration](#configuration)
- Open an issue on GitHub

## 📋 Troubleshooting

### Common Issues

**"Model not found"**
- Try alternative spellings (GPT-4 vs GPT4)
- Check if model has been published/accepted
- Verify arXiv availability

**"Author profiles incomplete"**
- Researcher may not have public profiles
- Check profile visibility settings
- Some platforms require API keys

**"API rate limits"**
- Configure API keys for higher limits
- Implement caching for repeated queries
- Add delays between requests

### Debug Mode
```bash
export MODEL_MAPPING_DEBUG=true
python model_mapping_cli.py
```

## 📄 License

This project is part of the AI Talent Operations ecosystem. See main project license for details.
