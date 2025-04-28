from dataclasses import dataclass
from abc import ABC, abstractmethod

from domain.entities.messages import Chat


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None: ...
