"""
Command-line interface for the semantic layer over graph database.
"""
import argparse
import os
from typing import Optional
from dotenv import load_dotenv

from graphsemantics.database import GraphDatabase
from graphsemantics.agent import SemanticAgent

def setup_environment(env_file: Optional[str] = None):
    """
    Load environment variables from .env file.

    Args:
        env_file: Optional path to .env file
    """
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()

    required_vars = ['OPENAI_API_KEY', 'NEO4J_URI', 'NEO4J_USERNAME', 'NEO4J_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            "Please set these in your .env file or environment."
        )

def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Semantic layer interface for Neo4j graph database"
    )
    parser.add_argument(
        "--env-file",
        help="Path to .env file containing configuration",
        default=None
    )
    parser.add_argument(
        "--import-data",
        action="store_true",
        help="Import sample movie data into the database"
    )
    parser.add_argument(
        "--query",
        help="Natural language query to run against the database"
    )
    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="OpenAI model to use (default: gpt-3.5-turbo)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0,
        help="Temperature for the model (default: 0)"
    )

    args = parser.parse_args()

    # Setup environment
    setup_environment(args.env_file)

    # Initialize database
    db = GraphDatabase()

    # Import data if requested
    if args.import_data:
        print("Importing sample movie data...")
        db.import_movie_data()
        print("Data import complete!")
        if not args.query:
            return

    # Handle query if provided
    if args.query:
        agent = SemanticAgent(
            model_name=args.model,
            temperature=args.temperature
        )
        print(f"\nQuery: {args.query}")
        response = agent.query(args.query)
        print(f"Response: {response}")

if __name__ == "__main__":
    main()
