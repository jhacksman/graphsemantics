"""
Example script demonstrating how to use the semantic layer over a graph database.
"""
import os
from dotenv import load_dotenv

from graphsemantics.database import GraphDatabase
from graphsemantics.agent import SemanticAgent

def setup_environment():
    """Load environment variables from .env file."""
    load_dotenv()

    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY', 'NEO4J_URI', 'NEO4J_USERNAME', 'NEO4J_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            "Please set these in your .env file or environment."
        )

def main():
    """Main function demonstrating the semantic layer functionality."""
    # Setup environment
    setup_environment()

    # Initialize database and import sample data
    print("Initializing database connection...")
    db = GraphDatabase()

    print("Importing sample movie data...")
    db.import_movie_data()

    # Initialize the semantic agent
    print("Setting up semantic agent...")
    agent = SemanticAgent()

    # Example queries
    example_queries = [
        "Who played in Casino?",
        "What movies did Christopher Nolan direct?",
        "Tell me about The Matrix",
    ]

    print("\nRunning example queries:")
    for query in example_queries:
        print(f"\nQuery: {query}")
        response = agent.query(query)
        print(f"Response: {response}")

if __name__ == "__main__":
    main()
