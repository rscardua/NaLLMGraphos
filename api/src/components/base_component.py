from abc import ABC, abstractmethod
from typing import Any


class BaseComponent(ABC):
    """Base class for all components, allows flexible run signatures."""

    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """Run the component with flexible arguments."""
        pass

    def run_async(self, *args, **kwargs) -> Any:
        """Async run with flexible arguments."""
        pass
