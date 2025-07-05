from abc import ABC, abstractmethod
from typing import (
    Any,
    List,
    Dict,
)


def raise_(ex):
    raise ex


class BaseLLM(ABC):
    """LLM wrapper should take in a prompt and return a string."""

    @abstractmethod
    def generate(self, messages: List[Dict[str, str]]) -> str:
        """Recebe uma lista de mensagens (dicionários) e retorna uma string."""

    @abstractmethod
    async def generateStreaming(
        self, messages: List[Dict[str, str]], onTokenCallback
    ) -> List[Any]:
        """Recebe uma lista de mensagens (dicionários) e retorna uma lista de tokens."""

    @abstractmethod
    def num_tokens_from_string(
        self,
        string: str,
    ) -> int:
        """Given a string returns the number of tokens the given string consists of"""

    @abstractmethod
    def max_allowed_token_length(
        self,
    ) -> int:
        """Returns the maximum number of tokens the LLM can handle"""
