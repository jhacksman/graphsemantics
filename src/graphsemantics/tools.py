"""
Custom tools implementation for the semantic layer.
"""
from typing import Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from graphsemantics.database import GraphDatabase

class MovieEntityInput(BaseModel):
    """Input model for the Information tool."""
    entity: str = Field(description="The name of the movie or person to search for")

class InformationTool(BaseTool):
    """Tool for retrieving information about movies and people from the graph database."""
    name = "Information"
    description = "Use this tool to get information about movies or people in the movie database"
    args_schema = MovieEntityInput

    def __init__(self):
        """Initialize the tool with a database connection."""
        super().__init__()
        self.db = GraphDatabase()

    def _run(
        self,
        entity: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """
        Execute the tool to retrieve information about a movie or person.

        Args:
            entity: Name of the movie or person to search for
            run_manager: Callback manager for the tool run

        Returns:
            str: Information about the requested entity
        """
        return self.db.get_information(entity)
