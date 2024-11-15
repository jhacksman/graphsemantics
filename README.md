# Graph Semantics Layer

A simplified implementation of a semantic layer over a Neo4j graph database using LangChain. This project enables natural language querying and reasoning over graph data structures.

## Overview

This project implements a semantic layer that allows users to interact with a Neo4j graph database using natural language. It leverages LangChain's capabilities to provide:

- Natural language queries over graph data
- Semantic reasoning capabilities
- Easy integration with existing Neo4j databases
- Simple API for common graph operations

## Documentation

- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [Usage Guide](docs/usage.md) - How to use the semantic layer
- [Architecture Guide](docs/architecture.md) - System design and extensibility

## Prerequisites

- Python 3.9+
- Neo4j Database (4.4+)
- OpenAI API key
- pip (Python package installer)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/jhacksman/graphsemantics.git
cd graphsemantics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials:
# OPENAI_API_KEY=your-api-key
# NEO4J_URI=your-neo4j-uri
# NEO4J_USERNAME=your-username
# NEO4J_PASSWORD=your-password
```

## Usage Examples

### Command Line Interface

```bash
# Import sample movie data
python -m graphsemantics.cli --import-data

# Query movies by director
python -m graphsemantics.cli --query "What movies did Christopher Nolan direct?"

# Get detailed movie information
python -m graphsemantics.cli --query "Tell me about Inception"
```

### Python API

```python
from graphsemantics.database import GraphDatabase
from graphsemantics.agent import SemanticAgent

# Initialize database and import data
db = GraphDatabase()
db.import_movie_data()

# Initialize semantic agent
agent = SemanticAgent()

# Run queries
response = agent.query("Who directed Inception?")
print(response)
# Expected output: "Christopher Nolan directed Inception..."

# Query with context
response = agent.query("What other movies did they direct?")
print(response)
# Expected output: "Christopher Nolan directed several acclaimed films..."
```

For more examples, check the [Usage Guide](docs/usage.md) or the `examples/` directory.

## Common Issues and Troubleshooting

### Connection Issues
- **Error**: Unable to connect to Neo4j
  - Verify Neo4j is running: `neo4j status`
  - Check credentials in `.env`
  - Ensure Neo4j port (7687) is accessible

### Authentication Issues
- **Error**: OpenAI API key invalid
  - Verify OPENAI_API_KEY in `.env`
  - Check API key validity at OpenAI dashboard

### Import Issues
- **Error**: Failed to import movie data
  - Ensure Neo4j has write permissions
  - Check available disk space
  - Verify network connectivity

For more troubleshooting tips, see the [Installation Guide](docs/installation.md).

## Project Structure

```
graphsemantics/
├── src/graphsemantics/    # Main package source code
│   ├── agent.py          # Semantic agent implementation
│   ├── database.py       # Neo4j database interface
│   ├── tools.py          # LangChain tools
│   └── cli.py           # Command-line interface
├── examples/             # Usage examples
├── docs/                 # Documentation
├── tests/               # Test suite
└── docker/              # Docker configurations
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. See our [Architecture Guide](docs/architecture.md) for details on extending the system.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
