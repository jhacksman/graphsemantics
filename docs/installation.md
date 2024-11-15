# Installation Guide

This guide will walk you through the process of setting up the Graph Semantics Layer project.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or higher
- Neo4j Database (version 4.4 or higher)
- pip (Python package installer)

## Installation Steps

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
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file with your credentials:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `NEO4J_URI`: Your Neo4j database URI (e.g., bolt://localhost:7687)
     - `NEO4J_USERNAME`: Your Neo4j username (default: neo4j)
     - `NEO4J_PASSWORD`: Your Neo4j password

4. Verify installation:
```bash
python -m graphsemantics.cli --help
```

## Neo4j Setup

1. Install Neo4j:
   - Follow the [official Neo4j installation guide](https://neo4j.com/docs/operations-manual/current/installation/)
   - Create a new database or use an existing one

2. Import sample data:
```bash
python -m graphsemantics.cli --import-data
```

## Common Issues

### Connection Issues
- Ensure Neo4j is running and accessible
- Verify your Neo4j credentials in the `.env` file
- Check if the Neo4j URI is correct and the port is accessible

### Authentication Issues
- Verify your OpenAI API key is valid and properly set in `.env`
- Ensure your Neo4j credentials have write permissions if using --import-data

### Import Data Issues
- If data import fails, check Neo4j logs for detailed error messages
- Ensure your Neo4j instance has enough disk space
- Verify network connectivity to GitHub (for sample data CSV)

## Next Steps

After installation, proceed to the [Usage Guide](usage.md) for examples and detailed instructions on using the semantic layer.
