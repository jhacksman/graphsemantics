"""
Database connection and setup module for graph semantics layer.
"""
from langchain_community.graphs import Neo4jGraph

class GraphDatabase:
    def __init__(self):
        """Initialize the graph database connection."""
        self.graph = Neo4jGraph()

    def import_movie_data(self):
        """Import sample movie data into the Neo4j database."""
        movies_query = """
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
        return self.graph.query(movies_query)

    def get_information(self, entity: str) -> str:
        """
        Retrieve information about a movie or person from the graph database.

        Args:
            entity: Name of the movie or person to search for

        Returns:
            str: Formatted information about the entity
        """
        description_query = """
        MATCH (m:Movie|Person)
        WHERE m.title CONTAINS $candidate OR m.name CONTAINS $candidate
        MATCH (m)-[r:ACTED_IN|HAS_GENRE]-(t)
        WITH m, type(r) as type, collect(coalesce(t.name, t.title)) as names
        WITH m, type+": "+reduce(s="", n IN names | s + n + ", ") as types
        WITH m, collect(types) as contexts
        WITH m, "type:" + labels(m)[0] + "\ntitle: "+ coalesce(m.title, m.name)
                + "\nyear: "+coalesce(m.released,"") +"\n" +
               reduce(s="", c in contexts | s + substring(c, 0, size(c)-2) +"\n") as context
        RETURN context LIMIT 1
        """
        try:
            data = self.graph.query(description_query, params={"candidate": entity})
            return data[0]["context"]
        except IndexError:
            return "No information was found"
