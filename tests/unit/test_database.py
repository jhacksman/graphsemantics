"""
Unit tests for the database module.

These tests verify the functionality of the GraphDatabase class
and its methods for managing Neo4j connections and queries.
"""
import os
import pytest
from unittest.mock import MagicMock, patch
from graphsemantics.database import GraphDatabase


@pytest.fixture
def mock_neo4j():
    """Create a mock Neo4j graph instance."""
    with patch('graphsemantics.database.Neo4jGraph') as mock:
        yield mock


@pytest.fixture
def mock_db(mock_neo4j):
    """Create a mock database instance with environment variables set."""
    os.environ.update({
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USERNAME': 'neo4j',
        'NEO4J_PASSWORD': 'password'
    })
    return GraphDatabase()


def test_init_missing_env_vars():
    """Test initialization fails when environment variables are missing."""
    # Clear environment variables
    for var in ['NEO4J_URI', 'NEO4J_USERNAME', 'NEO4J_PASSWORD']:
        os.environ.pop(var, None)

    with pytest.raises(EnvironmentError) as exc_info:
        GraphDatabase()
    assert "Missing required environment variables" in str(exc_info.value)


def test_init_connection_error(mock_neo4j):
    """Test initialization fails when Neo4j connection fails."""
    os.environ.update({
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USERNAME': 'neo4j',
        'NEO4J_PASSWORD': 'password'
    })
    mock_neo4j.side_effect = Exception("Connection failed")

    with pytest.raises(ConnectionError) as exc_info:
        GraphDatabase()
    assert "Failed to connect to Neo4j" in str(exc_info.value)


def test_init_successful(mock_neo4j):
    """Test successful initialization of GraphDatabase."""
    os.environ.update({
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USERNAME': 'neo4j',
        'NEO4J_PASSWORD': 'password'
    })
    db = GraphDatabase()
    mock_neo4j.assert_called_once_with(
        url=os.getenv('NEO4J_URI'),
        username=os.getenv('NEO4J_USERNAME'),
        password=os.getenv('NEO4J_PASSWORD')
    )


def test_import_movie_data(mock_db):
    """Test movie data import functionality."""
    mock_db.graph.query = MagicMock()
    mock_db.import_movie_data()
    mock_db.graph.query.assert_called_once()


def test_get_information_movie_found(mock_db):
    """Test retrieving movie information when movie exists."""
    mock_movie_data = {
        "title": "The Matrix",
        "released": 1999,
        "people": [
            {"name": "Keanu Reeves", "role": "ACTED_IN"},
            {"name": "Lana Wachowski", "role": "DIRECTED"}
        ]
    }
    mock_db.graph.query = MagicMock(return_value=[mock_movie_data])

    result = mock_db.get_information("The Matrix")
    assert "The Matrix (1999)" in result
    assert "Keanu Reeves" in result
    assert "Lana Wachowski" in result


def test_get_information_person_found(mock_db):
    """Test retrieving person information when person exists."""
    mock_person_data = {
        "name": "Keanu Reeves",
        "born": 1964,
        "movies": [
            {"title": "The Matrix", "role": "ACTED_IN"},
            {"title": "John Wick", "role": "ACTED_IN"}
        ]
    }
    mock_db.graph.query = MagicMock(side_effect=[[], [mock_person_data]])

    result = mock_db.get_information("Keanu Reeves")
    assert "Keanu Reeves (born 1964)" in result
    assert "The Matrix" in result
    assert "John Wick" in result


def test_get_information_not_found(mock_db):
    """Test retrieving information for non-existent entity."""
    mock_db.graph.query = MagicMock(return_value=[{"title": None, "name": None}])

    with pytest.raises(ValueError) as exc_info:
        mock_db.get_information("NonExistent")
    assert "No information found" in str(exc_info.value)
