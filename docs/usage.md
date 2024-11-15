# Usage Guide

This guide explains how to use the Graph Semantics Layer to interact with your Neo4j database using natural language queries.

## Basic Usage

### Command Line Interface

The simplest way to use the semantic layer is through the CLI:

```bash
# Basic query
python -m graphsemantics.cli --query "Who played in The Matrix?"

# Query with custom model
python -m graphsemantics.cli --model "gpt-4" --query "What movies did Christopher Nolan direct?"

# Import data and run query
python -m graphsemantics.cli --import-data --query "Tell me about Inception"
```

### Python API

You can also use the semantic layer in your Python code:

```python
from graphsemantics.database import GraphDatabase
from graphsemantics.agent import SemanticAgent

# Initialize database and import data
db = GraphDatabase()
db.import_movie_data()  # Only needed once

# Initialize semantic agent
agent = SemanticAgent()

# Run queries
response = agent.query("Who directed Inception?")
print(response)

# Use with chat history
chat_history = [
    ("Who directed Inception?", "Christopher Nolan directed Inception."),
    ("What other movies did they direct?", "Christopher Nolan directed several acclaimed films including The Dark Knight trilogy, Interstellar, and Dunkirk.")
]
response = agent.query("When was their latest movie released?", chat_history)
print(response)
```

## Query Examples

Here are some example queries you can try:

1. Finding movie information:
   - "Who starred in The Dark Knight?"
   - "What movies were released in 2010?"
   - "Tell me about Christopher Nolan's movies"

2. Finding actor information:
   - "What movies did Tom Hanks star in?"
   - "Who has acted with Morgan Freeman?"
   - "Which actors appeared in both Inception and The Dark Knight?"

3. Complex queries:
   - "What are the highest-rated movies from the 1990s?"
   - "Which directors have worked with Leonardo DiCaprio multiple times?"
   - "Find movies that are both action and science fiction"

## Advanced Usage

### Customizing the Agent

You can customize the OpenAI model and parameters:

```python
agent = SemanticAgent(
    model_name="gpt-4",  # Use a more capable model
    temperature=0.7      # Increase creativity in responses
)
```

### Error Handling

The semantic layer includes built-in error handling:

```python
try:
    response = agent.query("Tell me about a non-existent movie")
except Exception as e:
    print(f"Error: {e}")
```

## Performance Tips

1. **Chat History**: Use chat history for context-aware queries
2. **Model Selection**: Use gpt-3.5-turbo for speed, gpt-4 for accuracy
3. **Query Optimization**: Be specific in your queries for better results

## Extending the Functionality

You can extend the semantic layer by:

1. Adding new Cypher templates in database.py
2. Creating custom tools in the tools module
3. Modifying the agent's system prompt

See the [Architecture Guide](architecture.md) for details on extending the system.
