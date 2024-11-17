"""
Database connection and management module for the Graph Semantics Layer.

This module provides a high-level interface for interacting with a Neo4j graph database,
specifically designed for movie-related queries and information retrieval. It handles
connection management, data import, and query execution.

Example:
    ```python
    db = GraphDatabase()
    db.import_movie_data()  # Import sample movie dataset
    info = db.get_information("Inception")  # Get movie information
    ```

Attributes:
    MOVIE_IMPORT_QUERY (str): Cypher query template for importing movie data
    MOVIE_INFO_QUERY (str): Cypher query template for retrieving movie information
    PERSON_INFO_QUERY (str): Cypher query template for retrieving person information
"""
import os
from typing import Dict, List, Optional, Union
from langchain_community.graphs import Neo4jGraph

# Query templates for database operations
MOVIE_IMPORT_QUERY = """
LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies_small.csv' AS row
MERGE (m:Movie {id:row.movieId})
SET m.released = date(row.released),
    m.title = row.title,
    m.imdbRating = toFloat(row.imdbRating)
FOREACH (director in split(row.director, '|') |
    MERGE (p:Person {name:trim(director)})
    MERGE (p)-[:DIRECTED]->(m))
FOREACH (actor in split(row.actors, '|') |
    MERGE (p:Person {name:trim(actor)})
    MERGE (p)-[:ACTED_IN]->(m))
FOREACH (genre in split(row.genres, '|') |
    MERGE (g:Genre {name:trim(genre)})
    MERGE (m)-[:IN_GENRE]->(g))
"""

MOVIE_INFO_QUERY = """
MATCH (m:Movie {title: $candidate})
OPTIONAL MATCH (p:Person)-[r]->(m)
RETURN m.title as title, m.released as released,
       collect(DISTINCT {name: p.name, role: type(r)}) as people
"""

PERSON_INFO_QUERY = """
MATCH (p:Person {name: $candidate})
OPTIONAL MATCH (p)-[r]->(m:Movie)
RETURN p.name as name, p.born as born,
       collect(DISTINCT {title: m.title, role: type(r)}) as movies
"""

class GraphDatabase:
    """
    A class to manage Neo4j graph database connections and operations.

    This class provides methods for connecting to a Neo4j database, importing
    sample movie data, and retrieving information about movies and people.

    Attributes:
        graph (Neo4jGraph): The Neo4j graph connection instance

    Raises:
        EnvironmentError: If required environment variables are not set
        ConnectionError: If unable to connect to the Neo4j database
    """

    def __init__(self) -> None:
        """
        Initialize the graph database connection using environment variables.

        Raises:
            EnvironmentError: If required environment variables are not set
            ConnectionError: If unable to connect to the Neo4j database
        """
        required_vars = ['NEO4J_URI', 'NEO4J_USERNAME', 'NEO4J_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        try:
            self.graph = Neo4jGraph(
                url=os.getenv("NEO4J_URI"),
                username=os.getenv("NEO4J_USERNAME"),
                password=os.getenv("NEO4J_PASSWORD")
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Neo4j: {str(e)}")

    def import_movie_data(self) -> None:
        try:
            self.graph.query(MOVIE_IMPORT_QUERY)
        except Exception as e:
            raise Exception(f"Failed to import movie data: {str(e)}")

    def get_information(self, candidate: str) -> str:
        movie_result = self.graph.query(
            MOVIE_INFO_QUERY,
            {"candidate": candidate}
        )

        if movie_result and movie_result[0]["title"]:
            movie = movie_result[0]
            people_info = []
            for person in movie["people"]:
                people_info.append(f"{person['name']} ({person['role']})")

            return (
                f"Movie: {movie['title']} ({movie['released'].year})\n"
                f"People involved:\n- " + "\n- ".join(people_info)
            )

        person_result = self.graph.query(
            PERSON_INFO_QUERY,
            {"candidate": candidate}
        )

        if person_result and person_result[0]["name"]:
            person = person_result[0]
            movies_info = []
            for movie in person["movies"]:
                movies_info.append(f"{movie['title']} ({movie['role']})")

            birth_info = f" (born {person['born']})" if person["born"] else ""
            return (
                f"Person: {person['name']}{birth_info}\n"
                f"Filmography:\n- " + "\n- ".join(movies_info)
            )

        raise ValueError(f"No information found for '{candidate}'")

    def refresh_connection(self) -> None:
        try:
            self.graph = Neo4jGraph(
                url=os.getenv("NEO4J_URI"),
                username=os.getenv("NEO4J_USERNAME"),
                password=os.getenv("NEO4J_PASSWORD")
            )
        except Exception as e:
            raise ConnectionError(f"Failed to refresh Neo4j connection: {str(e)}")
