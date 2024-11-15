# Architecture Guide

This document explains the architecture of the Graph Semantics Layer and how to extend its functionality.

## System Overview

The Graph Semantics Layer consists of three main components:

1. **Database Layer** (`database.py`)
   - Handles Neo4j database connections
   - Manages Cypher queries
   - Provides data import functionality

2. **Tools Layer** (`tools.py`)
   - Implements LangChain tools
   - Provides semantic query capabilities
   - Handles query transformation

3. **Agent Layer** (`agent.py`)
   - Manages OpenAI model interaction
   - Handles conversation context
   - Coordinates tool usage

## Component Details

### Database Layer

```python
class GraphDatabase:
    def __init__(self)
    def import_movie_data()
    def get_information(entity: str)
```

The database layer provides:
- Database connection management
- Query execution
- Data import functionality
- Error handling for database operations

### Tools Layer

```python
class InformationTool(BaseTool):
    name = "Information"
    description = "..."
    args_schema = MovieEntityInput
```

The tools layer:
- Implements LangChain tool interfaces
- Validates input parameters
- Transforms natural language to structured queries
- Handles tool-specific error cases

### Agent Layer

```python
class SemanticAgent:
    def __init__(self, model_name: str, temperature: float)
    def query(self, input_text: str, chat_history: List[Tuple[str, str]])
```

The agent layer:
- Manages model configuration
- Handles conversation context
- Coordinates tool execution
- Processes model responses

## Data Flow

1. User input → Agent Layer
2. Agent Layer → OpenAI Model
3. Model → Tool Selection
4. Tool → Database Query
5. Database Response → Tool Processing
6. Processed Result → Agent
7. Agent → User Response

## Extending the System

### Adding New Tools

1. Create a new tool class in `tools.py`:
```python
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class CustomInput(BaseModel):
    parameter: str = Field(description="Parameter description")

class CustomTool(BaseTool):
    name = "CustomTool"
    description = "Tool description"
    args_schema = CustomInput

    def _run(self, parameter: str) -> str:
        # Implement tool logic
        pass
```

2. Add the tool to the agent:
```python
tools = [InformationTool(), CustomTool()]
```

### Adding New Queries

1. Add Cypher query to `database.py`:
```python
def custom_query(self, params: dict) -> List[dict]:
    query = """
    MATCH (n:Node)
    WHERE n.property = $param
    RETURN n
    """
    return self.graph.query(query, params=params)
```

2. Create a tool that uses the query:
```python
def _run(self, parameter: str) -> str:
    result = self.db.custom_query({"param": parameter})
    return self.format_result(result)
```

### Customizing Agent Behavior

1. Modify system prompt:
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Custom system prompt..."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
```

2. Adjust model parameters:
```python
agent = SemanticAgent(
    model_name="gpt-4",
    temperature=0.7
)
```

## Best Practices

1. **Error Handling**
   - Always catch and handle database exceptions
   - Provide meaningful error messages
   - Log errors appropriately

2. **Input Validation**
   - Use Pydantic models for tool inputs
   - Validate parameters before execution
   - Handle edge cases gracefully

3. **Performance**
   - Cache frequently used queries
   - Use efficient Cypher patterns
   - Batch database operations when possible

4. **Testing**
   - Write unit tests for new tools
   - Test edge cases and error conditions
   - Use mock objects for external dependencies

## Common Extension Scenarios

1. **Adding New Entity Types**
   - Add Cypher queries for new entities
   - Create specific tools for entity interaction
   - Update system prompt for new capabilities

2. **Custom Query Processing**
   - Implement custom result formatting
   - Add query optimization logic
   - Handle special case responses

3. **Enhanced Context Management**
   - Implement custom chat history handling
   - Add context-aware query processing
   - Manage conversation state

## Security Considerations

1. **Input Sanitization**
   - Validate all user inputs
   - Escape special characters
   - Prevent injection attacks

2. **Authentication**
   - Use environment variables for credentials
   - Implement proper error handling
   - Manage connection lifecycle

3. **Data Access**
   - Implement proper access controls
   - Limit query scope
   - Log sensitive operations
