from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import TypeVar, Any, Generic


@dataclass(frozen=True)
class BaseQuery(ABC): ...


QT = TypeVar("QT", bound=BaseQuery)
QR = TypeVar("QR", bound=Any)


@dataclass(frozen=True)
class BaseQueryHandler(ABC, Generic[QT, QR]):
    @abstractmethod
    def handle(self, query: QT) -> QR: ...
