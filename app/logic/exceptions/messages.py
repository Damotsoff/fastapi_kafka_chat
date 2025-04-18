from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithThatTitleExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f"чат с таким названием '{self.title}' уже существует."
