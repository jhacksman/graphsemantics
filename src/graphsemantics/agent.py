"""
Agent implementation for semantic layer over graph database.
"""
from typing import List, Tuple
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI

from graphsemantics.tools import InformationTool

class SemanticAgent:
    """Agent that provides a semantic layer over the graph database."""

    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0):
        """
        Initialize the semantic agent.

        Args:
            model_name: Name of the OpenAI model to use
            temperature: Temperature parameter for the model
        """
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.tools = [InformationTool()]
        self.llm_with_tools = self.llm.bind(
            functions=[convert_to_openai_function(t) for t in self.tools]
        )

        # Define the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a helpful assistant that finds information about movies "
                "and recommends them. If tools require follow up questions, "
                "make sure to ask the user for clarification. Make sure to include any "
                "available options that need to be clarified in the follow up questions "
                "Do only the things the user specifically requested. "
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Set up the agent
        self.agent = (
            {
                "input": lambda x: x["input"],
                "chat_history": lambda x: self._format_chat_history(x["chat_history"])
                if x.get("chat_history")
                else [],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
            }
            | self.prompt
            | self.llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )

        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )

    def _format_chat_history(self, chat_history: List[Tuple[str, str]]):
        """
        Format chat history into message objects.

        Args:
            chat_history: List of tuples containing (human_message, ai_message)

        Returns:
            List of formatted message objects
        """
        buffer = []
        for human, ai in chat_history:
            buffer.append(HumanMessage(content=human))
            buffer.append(AIMessage(content=ai))
        return buffer

    def query(self, input_text: str, chat_history: List[Tuple[str, str]] = None) -> str:
        """
        Query the semantic layer with natural language.

        Args:
            input_text: Natural language query
            chat_history: Optional chat history for context

        Returns:
            str: Response from the agent
        """
        result = self.agent_executor.invoke({
            "input": input_text,
            "chat_history": chat_history or []
        })
        return result["output"]
