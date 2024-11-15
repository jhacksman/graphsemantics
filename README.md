# Graph Semantics Layer

A simplified implementation of a semantic layer over a Neo4j graph database using LangChain. This project enables natural language querying and reasoning over graph data structures.

## Overview

This project implements a semantic layer that allows users to interact with a Neo4j graph database using natural language. It leverages LangChain's capabilities to provide:

- Natural language queries over graph data
- Semantic reasoning capabilities
- Easy integration with existing Neo4j databases
- Simple API for common graph operations

## Prerequisites

- Python 3.9+
- Neo4j Database
- OpenAI API key

## Installation

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
export OPENAI_API_KEY='your-api-key'
export NEO4J_URI='your-neo4j-uri'
export NEO4J_USERNAME='your-username'
export NEO4J_PASSWORD='your-password'
```

## Usage

Basic usage example:

```python
from graphsemantics import GraphSemanticLayer

# Initialize the semantic layer
semantic_layer = GraphSemanticLayer()

# Query the graph using natural language
result = semantic_layer.query("Find all movies directed by Christopher Nolan")
```

For more examples, check the `examples/` directory.

## Project Structure

```
graphsemantics/
├── src/graphsemantics/    # Main package source code
├── examples/              # Usage examples
├── docs/                  # Documentation
├── tests/                # Test suite
└── docker/               # Docker configurations
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
