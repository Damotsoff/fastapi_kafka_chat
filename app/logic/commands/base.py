from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Any


@dataclass(frozen=True)
class BaseCommand(ABC): ...


CT = TypeVar("CT", bound=BaseCommand)
CR = TypeVar("CR", bound=Any)


@dataclass(frozen=True)
class CommandHadler(ABC, Generic[CT, CR]):
    @abstractmethod
    async def handle(self, command: CT) -> CR: ...
